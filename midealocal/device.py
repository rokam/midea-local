"""Midea local device."""

import logging
import socket
import threading
import time
from collections.abc import Callable
from enum import IntEnum, StrEnum
from typing import Any

from typing_extensions import deprecated

from .const import DeviceType, ProtocolVersion
from .exceptions import SocketException
from .message import (
    MessageApplianceResponse,
    MessageQueryAppliance,
    MessageQuestCustom,
    MessageRequest,
    MessageType,
)
from .packet_builder import PacketBuilder
from .security import (
    MSGTYPE_ENCRYPTED_REQUEST,
    MSGTYPE_HANDSHAKE_REQUEST,
    LocalSecurity,
)

MIN_AUTH_RESPONSE = 20
MIN_MSG_LENGTH = 56
MIN_V2_FACTUAL_MSG_LENGTH = 6
RESPONSE_TIMEOUT = 12  # main loop socket recv timeout, 12 * 10s = 120s
SOCKET_TIMEOUT = 10  # socket connection default timeout
QUERY_TIMEOUT = 2  # query response in 1s, 0xAC have more queries, set to 2s


_LOGGER = logging.getLogger(__name__)


class AuthException(Exception):
    """Authentication exception."""


class ResponseException(Exception):
    """Response exception."""


class NoSupportedProtocol(Exception):
    """Query device failed exception."""


class DeviceAttributes(StrEnum):
    """Device attributes."""


class MessageResult(IntEnum):
    """Parse message result."""

    PADDING = 0
    SUCCESS = 1
    UNKNOWN = 96
    UNEXPECTED = 97
    TIMEOUT = 98
    ERROR = 99


class MideaDevice(threading.Thread):
    """Midea device."""

    def __init__(
        self,
        name: str,
        device_id: int,
        device_type: DeviceType,
        ip_address: str,
        port: int,
        token: str,
        key: str,
        device_protocol: ProtocolVersion,
        model: str,
        subtype: int,
        attributes: dict,
    ) -> None:
        """Midea device initialization."""
        threading.Thread.__init__(self)
        self._attributes = attributes or {}
        self._socket: socket.socket | None = None
        self._ip_address = ip_address
        self._port = port
        self._security = LocalSecurity()
        self._token = bytes.fromhex(token)
        self._key = bytes.fromhex(key)
        self._buffer = b""
        self._device_name = name
        self._device_id = device_id
        self._device_type = device_type
        self._device_protocol_version = device_protocol
        self._model = model
        self._subtype = subtype
        self._message_protocol_version: int = 0
        self._updates: list[Callable[[dict[str, Any]], None]] = []
        self._unsupported_protocol: list[str] = []
        self._is_run = False
        self._available = False
        self._appliance_query = True
        self._refresh_interval = 30
        self._heartbeat_interval = SOCKET_TIMEOUT
        self._default_refresh_interval = 30
        self._previous_refresh = 0.0
        self._previous_heartbeat = 0.0
        self.name = self._device_name

    @property
    def available(self) -> bool:
        """Device available."""
        return self._available

    @property
    def device_id(self) -> int:
        """Device ID."""
        return self._device_id

    @property
    def device_type(self) -> DeviceType:
        """Device type."""
        return self._device_type

    @property
    def model(self) -> str:
        """Device model."""
        return self._model

    @property
    def subtype(self) -> int:
        """Device subtype."""
        return self._subtype

    @staticmethod
    def fetch_v2_message(msg: bytes) -> tuple[list, bytes]:
        """Fetch V2 message."""
        result = []
        while len(msg) > 0:
            factual_msg_len = len(msg)
            if factual_msg_len < MIN_V2_FACTUAL_MSG_LENGTH:
                break
            alleged_msg_len = msg[4] + (msg[5] << 8)
            if factual_msg_len >= alleged_msg_len:
                result.append(msg[:alleged_msg_len])
                msg = msg[alleged_msg_len:]
            else:
                break
        return result, msg

    def connect(self, check_protocol: bool = False) -> bool:
        """Connect to device."""
        connected = False
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(SOCKET_TIMEOUT)
            _LOGGER.debug(
                "[%s] Connecting to %s:%s",
                self._device_id,
                self._ip_address,
                self._port,
            )
            self._socket.connect((self._ip_address, self._port))
            _LOGGER.debug("[%s] Connected", self._device_id)
            if self._device_protocol_version == ProtocolVersion.V3:
                self.authenticate()
            # 1. midea_ac_lan add device verify token with connect and auth
            # 2. init connection, check_protocol
            if check_protocol:
                self.refresh_status(check_protocol=check_protocol)
                self.get_capabilities()
            connected = True
        except TimeoutError:
            _LOGGER.debug("[%s] Connection timed out", self._device_id)
            self._socket = None
        except OSError:  # refresh_status exception
            _LOGGER.debug("[%s] Connection error", self._device_id)
            self._socket = None
        except AuthException:  # authenticate exception
            _LOGGER.debug("[%s] Authentication failed", self._device_id)
        except SocketException:  # refresh_status exception
            _LOGGER.debug("[%s] Connect socket exception", self._device_id)
            self._socket = None
        except NoSupportedProtocol:  # refresh_status exception
            _LOGGER.debug("[%s] No supported query protocol", self._device_id)
        except Exception as e:
            _LOGGER.exception(
                "[%s] Unknown error during connect device",
                self._device_id,
                exc_info=e,
            )
            self._socket = None
        # enable/disable device in init connection
        if check_protocol:
            self.set_available(connected)
        return connected

    def authenticate(self) -> None:
        """Authenticate to device. V3 only."""
        request = self._security.encode_8370(self._token, MSGTYPE_HANDSHAKE_REQUEST)
        if not self._socket:
            _LOGGER.debug(
                "[%s] authenticate failure, device socket is none",
                self._device_id,
            )
            # raise exception to connect loop
            raise SocketException
        _LOGGER.debug("[%s] Authentication handshaking", self._device_id)
        self._socket.send(request)
        response = self._socket.recv(512)
        _LOGGER.debug(
            "[%s] Received auth response with %d bytes: %s",
            self._device_id,
            len(response),
            response.hex(),
        )
        if len(response) < MIN_AUTH_RESPONSE:
            _LOGGER.debug(
                "[%s] Received auth response len %d error, bytes: %s",
                self._device_id,
                len(response),
                response.hex(),
            )
            raise AuthException
        response = response[8:72]
        self._security.tcp_key(response, self._key)
        _LOGGER.debug("[%s] Authentication success", self._device_id)

    def send_message(self, data: bytes, query: bool = False) -> None:
        """Send message."""
        if self._device_protocol_version == ProtocolVersion.V3:
            self.send_message_v3(data, msg_type=MSGTYPE_ENCRYPTED_REQUEST, query=query)
        else:
            self.send_message_v2(data, query=query)

    def send_message_v2(self, data: bytes, query: bool = False) -> None:
        """Send message V2."""
        if not self._socket:
            _LOGGER.debug(
                "[%s] send_message_v2 failure, device socket is none, data: %s",
                self._device_id,
                data.hex(),
            )
            # raise exception to main loop
            raise SocketException
        try:
            # query msg, set timeout to QUERY_TIMEOUT
            if query:
                self._socket.settimeout(QUERY_TIMEOUT)
            self._socket.send(data)
        except TimeoutError:
            _LOGGER.debug(
                "[%s] send_message_v2 timed out",
                self._device_id,
            )
            # raise exception to main loop
            raise
        except ConnectionResetError as e:
            _LOGGER.debug(
                "[%s] send_message_v2 ConnectionResetError: %s",
                self._device_id,
                e,
            )
            # raise exception to main loop
            raise
        except OSError as e:
            _LOGGER.debug(
                "[%s] send_message_v2 OSError: %s",
                self._device_id,
                e,
            )
            # raise exception to main loop
            raise
        except Exception as e:
            _LOGGER.exception(
                "[%s] send_message_v2 Unexpected socket error",
                self._device_id,
                exc_info=e,
            )
            # raise exception to main loop
            raise

    def send_message_v3(
        self,
        data: bytes,
        msg_type: int = MSGTYPE_ENCRYPTED_REQUEST,
        query: bool = False,
    ) -> None:
        """Send message V3."""
        data = self._security.encode_8370(data, msg_type)
        self.send_message_v2(data, query=query)

    def build_send(self, cmd: MessageRequest, query: bool = False) -> None:
        """Serialize and send."""
        data = cmd.serialize()
        _LOGGER.debug("[%s] Sending: %s, query is %s", self._device_id, cmd, query)
        msg = PacketBuilder(self._device_id, data).finalize()
        self.send_message(msg, query=query)

    def get_capabilities(self) -> None:
        """Get device capabilities."""
        cmds: list = self.capabilities_query()
        for cmd in cmds:
            self.build_send(cmd)

    def refresh_status(self, check_protocol: bool = False) -> None:
        """Refresh device status."""
        cmds: list = self.build_query()
        if self._appliance_query:
            cmds = [MessageQueryAppliance(self.device_type), *cmds]
        error_count = 0
        _LOGGER.debug(
            "[%s] refresh_status with cmds: %s, check_protocol %s",
            self._device_id,
            cmds,
            check_protocol,
        )
        for cmd in cmds:
            if cmd.__class__.__name__ not in self._unsupported_protocol:
                # set socket QUERY_TIMEOUT for query msg
                # build_send exception should be catch by connect/run
                self.build_send(cmd, query=True)
                # init check_protocol, skip timeout exception
                if check_protocol:
                    try:
                        while True:
                            if not self._socket:
                                _LOGGER.debug(
                                    "[%s] device socket is none",
                                    self._device_id,
                                )
                                # raise exception to connect/main loop
                                raise SocketException
                            msg = self._socket.recv(512)
                            if len(msg) == 0:
                                raise ConnectionResetError("Connection closed by peer.")
                            result = self.parse_message(msg)
                            # Prevent infinite loop
                            if result == MessageResult.SUCCESS:
                                break
                            elif result == MessageResult.PADDING:  # noqa: RET508
                                continue
                            else:
                                raise ResponseException  # noqa: TRY301
                        # recovery SOCKET_TIMEOUT after recv msg
                        self._socket.settimeout(SOCKET_TIMEOUT)
                    # only catch TimoutError for check_protocol
                    # unexpected exception in recv/settimeout, catch by main loop
                    except TimeoutError:
                        error_count += 1
                        self._unsupported_protocol.append(cmd.__class__.__name__)
                        _LOGGER.debug(
                            "[%s] Does not supports the protocol %s, cmd %s, ignored",
                            self._device_id,
                            cmd.__class__.__name__,
                            cmd,
                        )
                    except ResponseException:
                        # parse msg error
                        error_count += 1
                        _LOGGER.debug(
                            "[%s] refresh_status ResponseException %s, cmd %s",
                            self._device_id,
                            cmd.__class__.__name__,
                            cmd,
                        )
            else:
                _LOGGER.debug(
                    "[%s] refresh_status with cmd: %s, unsupported protocol, SKIP",
                    self._device_id,
                    cmd,
                )
                error_count += 1
            # all the query failed
            if error_count == len(cmds):
                _LOGGER.debug(
                    "[%s] all the query cmds failed %s, please report bug",
                    self._device_id,
                    cmds,
                )
                raise NoSupportedProtocol

    def pre_process_message(self, msg: bytearray) -> bool:
        """Pre process message."""
        if msg[9] == MessageType.query_appliance:
            message = MessageApplianceResponse(msg)
            self._appliance_query = False
            _LOGGER.debug("[%s] Appliance query Received: %s", self._device_id, message)
            self._message_protocol_version = message.protocol_version
            _LOGGER.debug(
                "[%s] Device protocol version: %s",
                self._device_id,
                self._message_protocol_version,
            )
            return False
        return True

    def parse_message(self, msg: bytes) -> MessageResult:
        """Parse message."""
        if self._device_protocol_version == ProtocolVersion.V3:
            messages, self._buffer = self._security.decode_8370(self._buffer + msg)
        else:
            messages, self._buffer = self.fetch_v2_message(self._buffer + msg)
        if len(messages) == 0:
            return MessageResult.PADDING
        for message in messages:
            if message == b"ERROR":
                return MessageResult.ERROR
            payload_len = message[4] + (message[5] << 8) - 56
            payload_type = message[2] + (message[3] << 8)
            if payload_type in [0x1001, 0x0001]:
                pass
            elif len(message) > MIN_MSG_LENGTH:
                cryptographic = bytes(message[40:-16])
                if payload_len % 16 == 0:
                    decrypted: bytearray = self._security.aes_decrypt(cryptographic)
                    try:
                        cont = True
                        if self._appliance_query:
                            cont = self.pre_process_message(decrypted)
                        if cont:
                            status = self.process_message(bytes(decrypted))
                            if len(status) > 0:
                                self.update_all(status)
                            else:
                                _LOGGER.debug(
                                    "[%s] Unidentified protocol",
                                    self._device_id,
                                )
                    except Exception:
                        _LOGGER.exception(
                            "[%s] Error in process message, msg = %s",
                            self._device_id,
                            decrypted.hex(),
                        )
                else:
                    _LOGGER.warning(
                        "[%s] Illegal payload, "
                        "original message = %s, buffer = %s, "
                        "8370 decoded = %s, payload type = %s, "
                        "alleged payload length = %s, factual payload length = %s, ",
                        self._device_id,
                        msg.hex(),
                        self._buffer.hex(),
                        message.hex(),
                        payload_type,
                        payload_len,
                        len(cryptographic),
                    )
            else:
                _LOGGER.warning(
                    "[%s] Illegal message, "
                    "original message = %s, buffer = %s, "
                    "8370 decoded = %s, payload type = %s, "
                    "alleged payload length = %s, message length = %s, ",
                    self._device_id,
                    msg.hex(),
                    self._buffer.hex(),
                    message.hex(),
                    payload_type,
                    payload_len,
                    len(message),
                )
        return MessageResult.SUCCESS

    def build_query(self) -> list:
        """Build query."""
        raise NotImplementedError

    def capabilities_query(self) -> list:
        """Capabilities query."""
        return []

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Process message."""
        raise NotImplementedError

    def send_command(self, cmd_type: MessageType, cmd_body: bytearray) -> None:
        """Send command."""
        cmd = MessageQuestCustom(
            self._device_type,
            self._message_protocol_version,
            cmd_type,
            cmd_body,
        )
        try:
            self.build_send(cmd)
        except OSError as e:
            _LOGGER.debug(
                "[{%s] Interface send_command failure, %s, "
                "cmd_type: %s, cmd_body: %s",
                self._device_id,
                repr(e),
                cmd_type,
                cmd_body.hex(),
            )

    def send_heartbeat(self) -> None:
        """Send heartbeat."""
        msg = PacketBuilder(self._device_id, bytearray([0x00])).finalize(msg_type=0)
        self.send_message(msg)

    def register_update(self, update: Callable[[dict[str, Any]], None]) -> None:
        """Register update."""
        self._updates.append(update)

    def update_all(self, status: dict[str, Any]) -> None:
        """Update all."""
        _LOGGER.debug("[%s] Status update: %s", self._device_id, status)
        for update in self._updates:
            update(status)

    def set_available(self, available: bool = True) -> None:
        """Set available value."""
        _LOGGER.debug(
            "[%s] %s device",
            self._device_id,
            "Enabling" if available else "Disabling",
        )
        self._available = available
        status = {"available": available}
        self.update_all(status)

    @deprecated("enable_device is replaced by set_available")
    def enable_device(self, available: bool = True) -> None:
        """Enable device."""
        self.set_available(available)

    def open(self) -> None:
        """Open thread."""
        if not self._is_run:
            self._is_run = True
            threading.Thread.start(self)

    def close(self) -> None:
        """Close thread."""
        if self._is_run:
            self._is_run = False
            self.close_socket()

    def close_socket(self) -> None:
        """Close socket."""
        self._unsupported_protocol = []
        self._buffer = b""
        if self._socket:
            try:
                self._socket.shutdown(socket.SHUT_RDWR)
                self._socket.close()
                _LOGGER.debug("[%s] Socket closed", self._device_id)
            except OSError as e:
                _LOGGER.debug("[%s] Error while closing socket: %s", self._device_id, e)
            finally:
                self._socket = None

    def set_ip_address(self, ip_address: str) -> None:
        """Set IP address."""
        if self._ip_address != ip_address:
            _LOGGER.debug("[%s] Update IP address to %s", self._device_id, ip_address)
            self._ip_address = ip_address
            self.close_socket()

    def set_refresh_interval(self, refresh_interval: int) -> None:
        """Set refresh interval."""
        self._refresh_interval = refresh_interval

    def _check_refresh(self, now: float) -> None:
        if 0 < self._refresh_interval <= now - self._previous_refresh:
            self.refresh_status()
            self._previous_refresh = now

    def _check_heartbeat(self, now: float) -> None:
        if now - self._previous_heartbeat >= self._heartbeat_interval:
            self.send_heartbeat()
            self._previous_heartbeat = now

    def _connect_loop(self) -> None:
        """Connect loop until device online."""
        # connect loop until online
        connection_retries = 0
        while self._socket is None:
            _LOGGER.debug("[%s] Socket is None, try to connect", self._device_id)
            if self.connect(check_protocol=True) is False:
                self.close_socket()
                connection_retries += 1
                # Sleep time with exponential backoff, maximum 600 seconds
                sleep_time = min(5 * (2 ** (connection_retries - 1)), 600)
                _LOGGER.warning(
                    "[%s] Unable to connect, sleep %s seconds and retry",
                    self._device_id,
                    sleep_time,
                )
                # sleep and reconnect loop until device online
                time.sleep(sleep_time)

    def run(self) -> None:  # noqa: PLR0915
        """Run loop brief description.

        1. first/init connection, self._socket is None
            1.1 connect() device loop, pass, enable device
            1.2 auth for v3 device, MUST pass for v3 device
            1.3 init refresh_status, send query and check supported protocol
                1.3.1 set socket timeout to QUERY_TIMEOUT before send query
                1.3.2 get response and add timeout query cmd to not supported
                1.3.1 parse recv response/status for supported protocol
            1.4 get_capabilities()
        2. after socket/device connected, check for heartbeat/refresh_status
        3. job1: check refresh_interval
            3.1 socket/device connection should exist
            3.2 send only supported query and refresh status in main loop recv
            3.3 set socket timeout before socket recv
        4. job2: check heartbeat interval
            4.1 socket/device connection should exist
            4.2 send heartbeat packet to keep alive

        scenario/bug fix:
        1. while True loop should sleep 0.1 second to prevent cpu usage issue
        2. device running and power off become offline, status update
        3. device disconnected and power on, become online, status update
        4. set command call build_send, main loop recv socket msg and refresh

        """
        # service loop
        while self._is_run:
            # connect loop until device online
            self._connect_loop()
            # socket recv msg timeout counter
            timeout_counter = 0
            start = time.time()
            self._previous_refresh = self._previous_heartbeat = start
            # refresh/recv msg loop after connected
            while True:
                try:
                    if not self._socket:
                        _LOGGER.debug("[%s] Socket is none", self._device_id)
                        raise SocketException  # noqa: TRY301
                    now = time.time()
                    # refresh_status only send supported query msg
                    self._check_refresh(now)
                    self._check_heartbeat(now)
                    # set SOCKET_TIMEOUT before recv socket msg
                    self._socket.settimeout(SOCKET_TIMEOUT)
                    # refresh status after set/query
                    msg = self._socket.recv(512)
                    if len(msg) == 0:
                        raise ConnectionResetError("Connection closed by peer")  # noqa: TRY301
                    # parse msg and update latest status
                    result = self.parse_message(msg)
                    if result == MessageResult.SUCCESS:
                        timeout_counter = 0
                    if result == MessageResult.ERROR:
                        _LOGGER.debug("[%s] Message 'ERROR' received", self._device_id)
                        self.close_socket()
                        break
                except TimeoutError:
                    timeout_counter += 1
                    if timeout_counter >= RESPONSE_TIMEOUT:
                        _LOGGER.debug("[%s] Heartbeat timed out", self._device_id)
                        self.close_socket()
                        break
                except SocketException:  # refresh_status
                    _LOGGER.debug("[%s] Socket Exception", self._device_id)
                    self.close_socket()
                    break
                except NoSupportedProtocol:
                    _LOGGER.debug("[%s] No Supported protocol", self._device_id)
                    # ignore and continue loop
                    continue
                except ConnectionResetError:  # refresh_status -> build_send exception
                    _LOGGER.debug("[%s] Connection reset by peer", self._device_id)
                    self.close_socket()
                    break
                except OSError:  # refresh_status
                    _LOGGER.debug("[%s] OS error", self._device_id)
                    self.close_socket()
                    break
                except Exception as e:
                    _LOGGER.exception(
                        "[%s] Unexpected error",
                        self._device_id,
                        exc_info=e,
                    )
                    self.close_socket()
                    break

    def set_attribute(self, attr: str, value: bool | int | str) -> None:
        """Set attribute."""
        raise NotImplementedError

    def get_attribute(self, attr: str) -> bool | int | str | list[int] | None:
        """Get attribute."""
        return self._attributes.get(attr)

    def set_customize(self, customize: str) -> None:
        """Set customize."""

    @property
    def attributes(self) -> dict[str, Any]:
        """Attributes."""
        ret = {}
        for status in self._attributes:
            ret[str(status)] = self._attributes[status]
        return ret
