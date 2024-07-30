"""Midea local device."""

import logging
import socket
import threading
import time
from collections.abc import Callable
from enum import IntEnum, StrEnum
from typing import Any

from .exceptions import CannotConnect, SocketException
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
RESPONSE_TIMEOUT = 120

_LOGGER = logging.getLogger(__name__)


class DeviceType(IntEnum):
    """Device Type."""

    A0 = 0xA0
    A1 = 0xA1
    AC = 0xAC
    B0 = 0xB0
    B1 = 0xB1
    B3 = 0xB3
    B4 = 0xB4
    B6 = 0xB6
    BF = 0xBF
    C2 = 0xC2
    C3 = 0xC3
    CA = 0xCA
    CC = 0xCC
    CD = 0xCD
    CE = 0xCE
    CF = 0xCF
    DA = 0xDA
    DB = 0xDB
    DC = 0xDC
    E1 = 0xE1
    E2 = 0xE2
    E3 = 0xE3
    E6 = 0xE6
    E8 = 0xE8
    EA = 0xEA
    EC = 0xEC
    ED = 0xED
    FA = 0xFA
    FB = 0xFB
    FC = 0xFC
    FD = 0xFD
    X13 = 0x13
    X26 = 0x26
    X34 = 0x34
    X40 = 0x40


class AuthException(Exception):
    """Authentication exception."""


class ResponseException(Exception):
    """Response exception."""


class RefreshFailed(Exception):
    """Refresh failed exception."""


class DeviceAttributes(StrEnum):
    """Device attributes."""


class ProtocolVersion(IntEnum):
    """Protocol version."""

    V1 = 1
    V2 = 2
    V3 = 3


class ParseMessageResult(IntEnum):
    """Parse message result."""

    SUCCESS = 0
    PADDING = 1
    ERROR = 99


class MideaDevice(threading.Thread):
    """Midea device."""

    def __init__(
        self,
        name: str,
        device_id: int,
        device_type: int,
        ip_address: str,
        port: int,
        token: str,
        key: str,
        protocol: int,
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
        self._protocol = protocol
        self._model = model
        self._subtype = subtype
        self._protocol_version = 0
        self._updates: list[Callable[[dict[str, Any]], None]] = []
        self._unsupported_protocol: list[str] = []
        self._is_run = False
        self._available = False
        self._appliance_query = True
        self._refresh_interval = 30
        self._heartbeat_interval = 10
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
    def device_type(self) -> int:
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

    def _authenticate_refresh_capabilities(self) -> None:
        if self._protocol == ProtocolVersion.V3:
            self.authenticate()
        self.refresh_status(wait_response=True)
        self.get_capabilities()

    def connect(self) -> bool:
        """Connect to device."""
        connected = False
        for _ in range(3):
            try:
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._socket.settimeout(10)
                _LOGGER.debug(
                    "[%s] Connecting to %s:%s",
                    self._device_id,
                    self._ip_address,
                    self._port,
                )
                self._socket.connect((self._ip_address, self._port))
                _LOGGER.debug("[%s] Connected", self._device_id)
                connected = True
                break
            except TimeoutError:
                _LOGGER.debug("[%s] Connection timed out", self._device_id)
            except OSError:
                _LOGGER.debug("[%s] Connection error", self._device_id)
            except AuthException:
                _LOGGER.debug("[%s] Authentication failed", self._device_id)
            except RefreshFailed:
                _LOGGER.debug("[%s] Refresh status is timed out", self._device_id)
            except Exception as e:
                file = None
                lineno = None
                if e.__traceback__:
                    file = e.__traceback__.tb_frame.f_globals["__file__"]  # pylint: disable=E1101
                    lineno = e.__traceback__.tb_lineno
                _LOGGER.exception(
                    "[%s] Unknown error : %s, %s",
                    self._device_id,
                    file,
                    lineno,
                )
        self.enable_device(connected)
        return connected

    def authenticate(self) -> None:
        """Authenticate to device. V3 only."""
        request = self._security.encode_8370(self._token, MSGTYPE_HANDSHAKE_REQUEST)
        _LOGGER.debug("[%s] Authentication handshaking", self._device_id)
        if not self._socket:
            self.enable_device(False)
            raise SocketException
        self._socket.send(request)
        response = self._socket.recv(512)
        if len(response) < MIN_AUTH_RESPONSE:
            self.enable_device(False)
            raise AuthException
        response = response[8:72]
        self._security.tcp_key(response, self._key)
        _LOGGER.debug("[%s] Authentication success", self._device_id)

    def send_message(self, data: bytes) -> None:
        """Send message."""
        if self._protocol == ProtocolVersion.V3:
            self.send_message_v3(data, msg_type=MSGTYPE_ENCRYPTED_REQUEST)
        else:
            self.send_message_v2(data)

    def send_message_v2(self, data: bytes) -> None:
        """Send message V2."""
        if self._socket is not None:
            self._socket.send(data)
        else:
            _LOGGER.debug(
                "[%s] Send failure, device disconnected, data: %s",
                self._device_id,
                data.hex(),
            )

    def send_message_v3(
        self,
        data: bytes,
        msg_type: int = MSGTYPE_ENCRYPTED_REQUEST,
    ) -> None:
        """Send message V3."""
        data = self._security.encode_8370(data, msg_type)
        self.send_message_v2(data)

    def build_send(self, cmd: MessageRequest) -> None:
        """Serialize and send."""
        data = cmd.serialize()
        _LOGGER.debug("[%s] Sending: %s", self._device_id, cmd)
        msg = PacketBuilder(self._device_id, data).finalize()
        self.send_message(msg)

    def get_capabilities(self) -> None:
        """Get device capabilities."""
        cmds: list = self.capabilities_query()
        for cmd in cmds:
            self.build_send(cmd)

    def refresh_status(self, wait_response: bool = False) -> None:
        """Refresh device status."""
        cmds: list = self.build_query()
        if self._appliance_query:
            cmds = [MessageQueryAppliance(self.device_type), *cmds]
        error_count = 0
        for cmd in cmds:
            if cmd.__class__.__name__ not in self._unsupported_protocol:
                self.build_send(cmd)
                if wait_response:
                    try:
                        while True:
                            if not self._socket:
                                raise SocketException
                            msg = self._socket.recv(512)
                            if len(msg) == 0:
                                raise OSError("Empty message received.")
                            result = self.parse_message(msg)
                            if result == ParseMessageResult.SUCCESS:
                                break
                            if result == ParseMessageResult.PADDING:
                                continue
                            error_count += 1
                    except TimeoutError:
                        error_count += 1
                        self._unsupported_protocol.append(cmd.__class__.__name__)
                        _LOGGER.debug(
                            "[%s] Does not supports the protocol %s, ignored",
                            self._device_id,
                            cmd.__class__.__name__,
                        )
            else:
                error_count += 1
        if error_count == len(cmds):
            raise RefreshFailed

    def pre_process_message(self, msg: bytearray) -> bool:
        """Pre process message."""
        if msg[9] == MessageType.query_appliance:
            message = MessageApplianceResponse(msg)
            self._appliance_query = False
            _LOGGER.debug("[%s] Received: %s", self._device_id, message)
            self._protocol_version = message.protocol_version
            _LOGGER.debug(
                "[%s] Device protocol version: %s",
                self._device_id,
                self._protocol_version,
            )
            return False
        return True

    def parse_message(self, msg: bytes) -> ParseMessageResult:
        """Parse message."""
        if self._protocol == ProtocolVersion.V3:
            messages, self._buffer = self._security.decode_8370(self._buffer + msg)
        else:
            messages, self._buffer = self.fetch_v2_message(self._buffer + msg)
        if len(messages) == 0:
            return ParseMessageResult.PADDING
        for message in messages:
            if message == b"ERROR":
                return ParseMessageResult.ERROR
            payload_len = message[4] + (message[5] << 8) - 56
            payload_type = message[2] + (message[3] << 8)
            if payload_type in [0x1001, 0x0001]:
                # Heartbeat detected
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
        return ParseMessageResult.SUCCESS

    def build_query(self) -> list:
        """Build query."""
        raise NotImplementedError

    def capabilities_query(self) -> list:
        """Capabilities query."""
        return []

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Process message."""
        raise NotImplementedError

    def send_command(self, cmd_type: int, cmd_body: bytearray) -> None:
        """Send command."""
        cmd = MessageQuestCustom(
            self._device_type,
            self._protocol_version,
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

    def enable_device(self, available: bool = True) -> None:
        """Enable device."""
        _LOGGER.debug("[%s] Enabling device", self._device_id)
        self._available = available
        status = {"available": available}
        self.update_all(status)

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
            self._socket.close()
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

    def run(self) -> None:
        """Run loop."""
        while self._is_run:
            if not self.connect():
                raise CannotConnect
            if not self._socket:
                raise SocketException
            self._authenticate_refresh_capabilities()
            timeout_counter = 0
            start = time.time()
            self._previous_refresh = self._previous_heartbeat = start
            self._socket.settimeout(1)
            while True:
                try:
                    now = time.time()
                    self._check_refresh(now)
                    self._check_heartbeat(now)
                    msg = self._socket.recv(512)
                    if len(msg) == 0:
                        if self._is_run:
                            _LOGGER.error(
                                "[%s] Socket error - Connection closed by peer",
                                self._device_id,
                            )
                            self.close_socket()
                        break
                    result = self.parse_message(msg)
                    if result == ParseMessageResult.ERROR:
                        _LOGGER.debug("[%s] Message 'ERROR' received", self._device_id)
                        self.close_socket()
                        break
                    if result == ParseMessageResult.SUCCESS:
                        timeout_counter = 0
                except TimeoutError:
                    timeout_counter = timeout_counter + 1
                    if timeout_counter >= RESPONSE_TIMEOUT:
                        _LOGGER.debug("[%s] Heartbeat timed out", self._device_id)
                        self.close_socket()
                        break
                except OSError as e:
                    if self._is_run:
                        _LOGGER.debug("[%s] Socket error %s", self._device_id, repr(e))
                        self.close_socket()
                    break
                except Exception as e:
                    file = None
                    lineno = None
                    if e.__traceback__:
                        file = e.__traceback__.tb_frame.f_globals["__file__"]  # pylint: disable=E1101
                        lineno = e.__traceback__.tb_lineno
                    _LOGGER.exception(
                        "[%s] Unknown error : %s, %s",
                        self._device_id,
                        file,
                        lineno,
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
