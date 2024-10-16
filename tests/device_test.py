"""Midea Local device test."""

from unittest.mock import MagicMock, patch

import pytest

from midealocal.cloud import DEFAULT_KEYS
from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import (
    AuthException,
    MessageResult,
    MideaDevice,
    NoSupportedProtocol,
)
from midealocal.devices.ac.message import MessageCapabilitiesQuery
from midealocal.exceptions import SocketException
from midealocal.message import MessageType


def test_fetch_v2_message() -> None:
    """Test fetch v2 message."""
    assert MideaDevice.fetch_v2_message(bytearray([])) == ([], bytearray([]))
    assert MideaDevice.fetch_v2_message(bytearray([0x1])) == ([], bytearray([0x1]))
    assert MideaDevice.fetch_v2_message(bytearray([0x1] * 5 + [0x0] + [0x1] * 7)) == (
        [bytearray([0x1])],
        bytearray([0x1] * 4 + [0x0] + [0x1] * 7),
    )


class MideaDeviceTest:
    """Midea device test case."""

    device: MideaDevice

    @pytest.fixture(autouse=True)
    def _setup_device(self) -> None:
        """Midea A1 Device setup."""
        self.device = MideaDevice(
            name="Test Device",
            device_id=1,
            device_type=DeviceType.AC,
            ip_address="192.168.1.100",
            port=6444,
            token=DEFAULT_KEYS[99]["token"],
            key=DEFAULT_KEYS[99]["key"],
            device_protocol=ProtocolVersion.V3,
            model="test_model",
            subtype=1,
            attributes={},
        )

    def test_initial_attributes(self) -> None:
        """Test initial attributes."""
        assert len(self.device.attributes) == 0
        assert self.device.name == "Test Device"
        assert self.device.device_id == 1
        assert self.device.device_type == 0xAC
        assert self.device.model == "test_model"
        assert self.device.subtype == 1

    @pytest.mark.parametrize(
        ("exc", "result"),
        [
            (TimeoutError, False),
            (OSError, False),
            (AuthException, False),
            (NoSupportedProtocol, False),
            (None, True),
        ],
    )
    def test_connect(self, exc: Exception, result: bool) -> None:
        """Test connect."""
        with patch("socket.socket.connect", side_effect=exc):
            assert self.device.connect() is result
            assert self.device.available is result

    def test_connect_generic_exception(self) -> None:
        """Test connect with generic exception."""
        with patch("socket.socket.connect") as connect_mock:
            connect_mock.side_effect = Exception()

            assert self.device.connect() is False
            assert self.device.available is False

    def test_authenticate(self) -> None:
        """Test authenticate."""
        socket_mock = MagicMock()
        with patch.object(
            socket_mock,
            "recv",
            side_effect=[
                bytearray(),
                bytearray(
                    [0x00] * (8 + 32)
                    + [
                        0xCE,
                        0x8C,
                        0xFB,
                        0xF1,
                        0x65,
                        0x90,
                        0xD1,
                        0x07,
                        0x6D,
                        0xF8,
                        0x3A,
                        0x3B,
                        0x67,
                        0xCC,
                        0x6B,
                        0xB6,
                        0x80,
                        0xF6,
                        0x0E,
                        0x3D,
                        0xFF,
                        0xE7,
                        0x74,
                        0x92,
                        0x14,
                        0x4D,
                        0xE9,
                        0xD2,
                        0xD5,
                        0x74,
                        0x7E,
                        0x6F,
                    ],
                ),
            ],
        ):
            self.device._socket = None
            with pytest.raises(SocketException):
                self.device.authenticate()

            self.device._socket = socket_mock
            with pytest.raises(AuthException):
                self.device.authenticate()

            self.device.authenticate()

    def test_send_message(self) -> None:
        """Test send message."""
        socket_mock = MagicMock()
        with patch.object(
            socket_mock,
            "recv",
            side_effect=[
                bytearray(
                    [0x00] * (8 + 32)
                    + [
                        0xCE,
                        0x8C,
                        0xFB,
                        0xF1,
                        0x65,
                        0x90,
                        0xD1,
                        0x07,
                        0x6D,
                        0xF8,
                        0x3A,
                        0x3B,
                        0x67,
                        0xCC,
                        0x6B,
                        0xB6,
                        0x80,
                        0xF6,
                        0x0E,
                        0x3D,
                        0xFF,
                        0xE7,
                        0x74,
                        0x92,
                        0x14,
                        0x4D,
                        0xE9,
                        0xD2,
                        0xD5,
                        0x74,
                        0x7E,
                        0x6F,
                    ],
                ),
            ],
        ):
            self.device._socket = socket_mock
            self.device.authenticate()
            self.device.send_message(bytearray([0x0] * 20))
            self.device._socket = None
            self.device._device_protocol_version = ProtocolVersion.V2
            self.device.send_message(bytearray([0x0] * 20))

    def test_get_capabilities(self) -> None:
        """Test get capabilities."""
        self.device.get_capabilities()  # Empty capabilities
        with (
            patch.object(self.device, "build_send", return_value=None),
            patch.object(
                self.device,
                "capabilities_query",
                return_value=[MessageCapabilitiesQuery(ProtocolVersion.V2, False)],
            ),
        ):
            self.device.get_capabilities()

    def test_refresh_status(self) -> None:
        """Test refresh status."""
        with pytest.raises(NotImplementedError):
            self.device.refresh_status()  # build_query not implemented

        socket_mock = MagicMock()
        with (
            patch.object(self.device, "build_query", return_value=[]),
            patch.object(
                socket_mock,
                "recv",
                side_effect=[
                    bytearray([]),
                    bytearray([0x0]),
                    bytearray([0x0]),
                    bytearray([0x0]),
                    TimeoutError(),
                ],
            ),
            patch.object(self.device, "build_send", return_value=None),
            patch.object(
                self.device,
                "parse_message",
                side_effect=[
                    MessageResult.SUCCESS,
                    MessageResult.PADDING,
                    MessageResult.ERROR,
                ],
            ),
        ):
            self.device._socket = None
            with pytest.raises(SocketException):
                self.device.refresh_status(True)

            self.device._socket = socket_mock
            with pytest.raises(OSError, match="Empty message received."):
                self.device.refresh_status(True)

            self.device.refresh_status(True)  # SUCCESS
            self.device.refresh_status(True)  # PADDING

            with pytest.raises(NoSupportedProtocol):
                self.device.refresh_status(True)  # ERROR
            with pytest.raises(NoSupportedProtocol):
                self.device.refresh_status(True)  # Timeout
            with pytest.raises(NoSupportedProtocol):
                self.device.refresh_status(True)  # Unsupported protocol

    def test_parse_message(self) -> None:
        """Test parse message."""
        with (
            patch.object(self.device._security, "decode_8370", return_value=([], b"")),
            patch.object(
                self.device._security,
                "aes_decrypt",
                return_value=bytearray([0x1] * 16),
            ),
            patch.object(
                self.device,
                "fetch_v2_message",
                side_effect=[
                    ([b"ERROR"], b""),
                    (
                        [
                            bytearray([0x0, 0x0, 0x01, 0x10, 0x0, 0x0]),
                            bytearray([0x0] * 4 + [0x8, 0x1] + [0x1] * 56),
                            bytearray([0x0] * 4 + [0x8, 0x1] + [0x1] * 56),
                            bytearray([0x0] * 4 + [0x8, 0x1] + [0x1] * 56),
                            bytearray([0x0] * 4 + [0x2, 0x1] + [0x1] * 56),
                            bytearray([0x1] * 50),
                        ],
                        b"",
                    ),
                ],
            ),
        ):
            assert self.device.parse_message(bytearray([])) == MessageResult.PADDING
            self.device._device_protocol_version = ProtocolVersion.V2
            assert self.device.parse_message(bytearray([])) == MessageResult.ERROR
            with patch.object(
                self.device,
                "process_message",
                side_effect=[{"power": True}, {}, NotImplementedError()],
            ):
                assert self.device.parse_message(bytearray([])) == MessageResult.SUCCESS

    def test_pre_process_message(self) -> None:
        """Test pre process message."""
        assert self.device.pre_process_message(bytearray([0x0] * 10)) is True
        assert (
            self.device.pre_process_message(
                bytearray([0x0] * 9 + [MessageType.query_appliance] + [0x1] * 10),
            )
            is False
        )
        assert self.device._appliance_query is False

    def test_process_message(self) -> None:
        """Test process message."""
        with pytest.raises(NotImplementedError):
            self.device.process_message(bytearray([]))

    def test_send_command(self) -> None:
        """Test send command."""
        with patch.object(self.device, "build_send", side_effect=[None, OSError()]):
            self.device.send_command(MessageType.query, bytearray([0x1] * 10))
            self.device.send_command(MessageType.query, bytearray([0x1] * 10))

    def test_send_heartbeat(self) -> None:
        """Test send heartbeat."""
        with patch.object(self.device, "send_message"):
            self.device.send_heartbeat()

    def test_register_update(self) -> None:
        """Test register update."""
        upd = MagicMock()
        assert len(self.device._updates) == 0
        self.device.register_update(upd)
        assert len(self.device._updates) == 1
        self.device.update_all({"status": True})
        upd.assert_called()

    def test_open(self) -> None:
        """Test open."""
        with (
            patch.object(self.device, "connect", return_value=False),
            patch.object(self.device, "run"),
        ):
            self.device.open()
            assert self.device._is_run is True

    def test_close(self) -> None:
        """Test close."""
        with patch.object(self.device, "_socket") as socket_mock:
            self.device._is_run = True
            self.device.close()
            assert self.device._is_run is False
            socket_mock.close.assert_called()

    def test_set_ip(self) -> None:
        """Test set ip."""
        with patch.object(self.device, "_socket") as socket_mock:
            assert self.device._ip_address == "192.168.1.100"
            self.device.set_ip_address("10.0.0.1")
            socket_mock.close.assert_called()
            assert self.device._ip_address == "10.0.0.1"
