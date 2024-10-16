"""Test B8 Device."""

from unittest.mock import patch

import pytest

from midealocal.const import ProtocolVersion
from midealocal.devices.b8 import MideaB8Device
from midealocal.devices.b8.const import (
    B8CleanMode,
    B8ControlType,
    B8DeviceAttributes,
    B8ErrorCanFixDescription,
    B8ErrorRebootDescription,
    B8ErrorType,
    B8ErrorWarningDescription,
    B8FanLevel,
    B8FunctionType,
    B8MopState,
    B8Moviment,
    B8Speed,
    B8WaterLevel,
    B8WorkMode,
    B8WorkStatus,
)
from midealocal.devices.b8.message import (
    MessageQuery,
)
from midealocal.message import MessageType


class TestMideaB8Device:
    """Test Midea B8 Device."""

    device: MideaB8Device

    @pytest.fixture(autouse=True)
    def _setup_device(self) -> None:
        """Midea B8 Device setup."""
        self.device = MideaB8Device(
            name="Test Device",
            device_id=1,
            ip_address="192.168.1.1",
            port=12345,
            token="AA",
            key="BB",
            device_protocol=ProtocolVersion.V1,
            model="test_model",
            subtype=1,
            customize="",
        )

    def test_initial_attributes(self) -> None:
        """Test initial attributes."""
        assert (
            self.device.attributes[B8DeviceAttributes.WORK_STATUS]
            == B8WorkStatus.NONE.name.lower()
        )
        assert (
            self.device.attributes[B8DeviceAttributes.FUNCTION_TYPE]
            == B8FunctionType.NONE.name.lower()
        )
        assert (
            self.device.attributes[B8DeviceAttributes.CONTROL_TYPE]
            == B8ControlType.NONE.name.lower()
        )
        assert (
            self.device.attributes[B8DeviceAttributes.MOVE_DIRECTION]
            == B8Moviment.NONE.name.lower()
        )
        assert (
            self.device.attributes[B8DeviceAttributes.CLEAN_MODE]
            == B8CleanMode.NONE.name.lower()
        )
        assert (
            self.device.attributes[B8DeviceAttributes.FAN_LEVEL]
            == B8FanLevel.OFF.name.lower()
        )
        assert self.device.attributes[B8DeviceAttributes.AREA] == 0
        assert (
            self.device.attributes[B8DeviceAttributes.WATER_LEVEL]
            == B8WaterLevel.OFF.name.lower()
        )
        assert self.device.attributes[B8DeviceAttributes.VOICE_VOLUME] == 0
        assert (
            self.device.attributes[B8DeviceAttributes.MOP]
            == B8MopState.OFF.name.lower()
        )
        assert self.device.attributes[B8DeviceAttributes.CARPET_SWITCH] is False
        assert (
            self.device.attributes[B8DeviceAttributes.SPEED]
            == B8Speed.HIGH.name.lower()
        )
        assert self.device.attributes[B8DeviceAttributes.HAVE_RESERVE_TASK] is False
        assert self.device.attributes[B8DeviceAttributes.BATTERY_PERCENT] == 0
        assert self.device.attributes[B8DeviceAttributes.WORK_TIME] == 0
        assert self.device.attributes[B8DeviceAttributes.UV_SWITCH] is False
        assert self.device.attributes[B8DeviceAttributes.WIFI_SWITCH] is False
        assert self.device.attributes[B8DeviceAttributes.VOICE_SWITCH] is False
        assert self.device.attributes[B8DeviceAttributes.COMMAND_SOURCE] is False
        assert (
            self.device.attributes[B8DeviceAttributes.ERROR_TYPE]
            == B8ErrorType.NO.name.lower()
        )
        assert self.device.attributes[B8DeviceAttributes.ERROR_DESC] == "no"
        assert self.device.attributes[B8DeviceAttributes.DEVICE_ERROR] is False
        assert (
            self.device.attributes[B8DeviceAttributes.BOARD_COMMUNICATION_ERROR]
            is False
        )
        assert self.device.attributes[B8DeviceAttributes.LASER_SENSOR_SHELTER] is False
        assert self.device.attributes[B8DeviceAttributes.LASER_SENSOR_ERROR] is False

    def test_set_attribute(self) -> None:
        """Test set attribute."""
        with patch.object(self.device, "send_message_v2") as mock_build_send:
            self.device.set_attribute(B8DeviceAttributes.CLEAN_MODE.value, "area")
            mock_build_send.assert_called_once()
            mock_build_send.reset_mock()

            self.device.set_attribute(B8DeviceAttributes.FAN_LEVEL.value, "normal")
            mock_build_send.assert_called_once()
            mock_build_send.reset_mock()

            self.device.set_attribute(B8DeviceAttributes.WATER_LEVEL.value, "normal")
            mock_build_send.assert_called_once()
            mock_build_send.reset_mock()

            self.device.set_attribute(B8DeviceAttributes.VOICE_VOLUME.value, 10)
            mock_build_send.assert_called_once()
            mock_build_send.reset_mock()

            self.device.set_attribute(B8DeviceAttributes.WATER_LEVEL.value, "invalid")
            mock_build_send.assert_not_called()

    def test_set_work_mode(self) -> None:
        """Test set work mode."""
        with patch.object(self.device, "send_message_v2") as mock_build_send:
            self.device.set_work_mode(B8WorkMode.CHARGE)
            mock_build_send.assert_called_once()
            mock_build_send.reset_mock()

            self.device.set_work_mode(B8WorkMode.WORK)
            mock_build_send.assert_called_once()

    def test_build_query(self) -> None:
        """Test build query."""
        queries = self.device.build_query()
        assert len(queries) == 1
        assert isinstance(queries[0], MessageQuery)

    def test_query_response(self) -> None:
        """Test query response."""
        header = bytearray(
            [0xAA] + ([0x0] * 7) + [ProtocolVersion.V1] + [MessageType.query],
        )
        body = bytearray(
            [
                0x32,
                0x1,
                B8WorkStatus.CHARGING_WITH_WIRE,
                B8FunctionType.NONE,
                B8ControlType.AUTO,
                B8Moviment.NONE,
                B8CleanMode.AUTO,
                B8FanLevel.NORMAL,
                0,
                B8WaterLevel.NORMAL,
                40,
                0,
                80,
                20,
                0xC7,
                B8ErrorType.CAN_FIX,
                B8ErrorCanFixDescription.FIX_DUST,
                B8MopState.ON,
                0x01,
                0x07,
                B8Speed.HIGH,
                0x0,  # CRC
            ],
        )
        self.device.process_message(bytearray(header + body))
        assert (
            self.device.attributes[B8DeviceAttributes.WORK_STATUS]
            == "charging_with_wire"
        )
        assert self.device.attributes[B8DeviceAttributes.FUNCTION_TYPE] == "none"
        assert self.device.attributes[B8DeviceAttributes.CONTROL_TYPE] == "auto"
        assert self.device.attributes[B8DeviceAttributes.MOVE_DIRECTION] == "none"
        assert self.device.attributes[B8DeviceAttributes.CLEAN_MODE] == "auto"
        assert self.device.attributes[B8DeviceAttributes.FAN_LEVEL] == "normal"
        assert self.device.attributes[B8DeviceAttributes.AREA] == 0
        assert self.device.attributes[B8DeviceAttributes.WATER_LEVEL] == "normal"
        assert self.device.attributes[B8DeviceAttributes.VOICE_VOLUME] == 40
        assert self.device.attributes[B8DeviceAttributes.HAVE_RESERVE_TASK] is False
        assert self.device.attributes[B8DeviceAttributes.BATTERY_PERCENT] == 80
        assert self.device.attributes[B8DeviceAttributes.WORK_TIME] == 20
        assert self.device.attributes[B8DeviceAttributes.UV_SWITCH] is True
        assert self.device.attributes[B8DeviceAttributes.WIFI_SWITCH] is True
        assert self.device.attributes[B8DeviceAttributes.VOICE_SWITCH] is True
        assert self.device.attributes[B8DeviceAttributes.COMMAND_SOURCE] is True
        assert self.device.attributes[B8DeviceAttributes.DEVICE_ERROR] is True
        assert self.device.attributes[B8DeviceAttributes.ERROR_TYPE] == "can_fix"
        assert self.device.attributes[B8DeviceAttributes.ERROR_DESC] == "fix_dust"
        assert self.device.attributes[B8DeviceAttributes.MOP] == "on"
        assert self.device.attributes[B8DeviceAttributes.CARPET_SWITCH] is True
        assert self.device.attributes[B8DeviceAttributes.LASER_SENSOR_ERROR] is True
        assert self.device.attributes[B8DeviceAttributes.LASER_SENSOR_SHELTER] is True
        assert (
            self.device.attributes[B8DeviceAttributes.BOARD_COMMUNICATION_ERROR] is True
        )
        assert self.device.attributes[B8DeviceAttributes.SPEED] == "high"

    def test_notify_response(self) -> None:
        """Test notify response."""
        header = bytearray(
            [0xAA] + ([0x0] * 7) + [ProtocolVersion.V1] + [MessageType.notify1],
        )
        body = bytearray(
            [
                0x42,
                B8WorkStatus.WORK,
                B8FunctionType.DUST_BOX_CLEANING,
                B8ControlType.MANUAL,
                B8Moviment.LEFT,
                B8CleanMode.PATH,
                B8FanLevel.HIGH,
                1,
                B8WaterLevel.LOW,
                90,
                1,
                40,
                15,
                0x86,
                B8ErrorType.WARNING,
                B8ErrorWarningDescription.WARN_FULL_DUST,
                B8MopState.LACK_WATER,
                0x00,
                0x06,
                B8Speed.LOW,
                0x0,  # CRC
            ],
        )
        self.device.process_message(bytearray(header + body))
        assert self.device.attributes[B8DeviceAttributes.WORK_STATUS] == "work"
        assert (
            self.device.attributes[B8DeviceAttributes.FUNCTION_TYPE]
            == "dust_box_cleaning"
        )
        assert self.device.attributes[B8DeviceAttributes.CONTROL_TYPE] == "manual"
        assert self.device.attributes[B8DeviceAttributes.MOVE_DIRECTION] == "left"
        assert self.device.attributes[B8DeviceAttributes.CLEAN_MODE] == "path"
        assert self.device.attributes[B8DeviceAttributes.FAN_LEVEL] == "high"
        assert self.device.attributes[B8DeviceAttributes.AREA] == 1
        assert self.device.attributes[B8DeviceAttributes.WATER_LEVEL] == "low"
        assert self.device.attributes[B8DeviceAttributes.VOICE_VOLUME] == 90
        assert self.device.attributes[B8DeviceAttributes.HAVE_RESERVE_TASK] is True
        assert self.device.attributes[B8DeviceAttributes.BATTERY_PERCENT] == 40
        assert self.device.attributes[B8DeviceAttributes.WORK_TIME] == 15
        assert self.device.attributes[B8DeviceAttributes.UV_SWITCH] is False
        assert self.device.attributes[B8DeviceAttributes.WIFI_SWITCH] is True
        assert self.device.attributes[B8DeviceAttributes.VOICE_SWITCH] is True
        assert self.device.attributes[B8DeviceAttributes.COMMAND_SOURCE] is False
        assert self.device.attributes[B8DeviceAttributes.DEVICE_ERROR] is True
        assert self.device.attributes[B8DeviceAttributes.ERROR_TYPE] == "warning"
        assert self.device.attributes[B8DeviceAttributes.ERROR_DESC] == "warn_full_dust"
        assert self.device.attributes[B8DeviceAttributes.MOP] == "lack_water"
        assert self.device.attributes[B8DeviceAttributes.CARPET_SWITCH] is False
        assert self.device.attributes[B8DeviceAttributes.LASER_SENSOR_ERROR] is False
        assert self.device.attributes[B8DeviceAttributes.LASER_SENSOR_SHELTER] is True
        assert (
            self.device.attributes[B8DeviceAttributes.BOARD_COMMUNICATION_ERROR] is True
        )
        assert self.device.attributes[B8DeviceAttributes.SPEED] == "low"

    def test_query_response_reboot_error(self) -> None:
        """Test query response."""
        header = bytearray(
            [0xAA] + ([0x0] * 7) + [ProtocolVersion.V1] + [MessageType.query],
        )
        body = bytearray(
            [
                0x32,
                0x1,
                B8WorkStatus.UPDATING,
                B8FunctionType.WATER_TANK_CLEANING,
                B8ControlType.NONE,
                B8Moviment.NONE,
                B8CleanMode.NONE,
                B8FanLevel.OFF,
                0,
                B8WaterLevel.OFF,
                0,
                0,
                0,
                0,
                0,
                B8ErrorType.REBOOT,
                B8ErrorRebootDescription.REBOOT_LASER_COMM_FAIL,
                B8MopState.OFF,
                0x0,
                0x0,
                B8Speed.LOW,
                0x0,  # CRC
            ],
        )
        self.device.process_message(bytearray(header + body))
        assert self.device.attributes[B8DeviceAttributes.WORK_STATUS] == "updating"
        assert (
            self.device.attributes[B8DeviceAttributes.FUNCTION_TYPE]
            == "water_tank_cleaning"
        )
        assert self.device.attributes[B8DeviceAttributes.CONTROL_TYPE] == "none"
        assert self.device.attributes[B8DeviceAttributes.MOVE_DIRECTION] == "none"
        assert self.device.attributes[B8DeviceAttributes.CLEAN_MODE] == "none"
        assert self.device.attributes[B8DeviceAttributes.FAN_LEVEL] == "off"
        assert self.device.attributes[B8DeviceAttributes.AREA] == 0
        assert self.device.attributes[B8DeviceAttributes.WATER_LEVEL] == "off"
        assert self.device.attributes[B8DeviceAttributes.VOICE_VOLUME] == 0
        assert self.device.attributes[B8DeviceAttributes.HAVE_RESERVE_TASK] is False
        assert self.device.attributes[B8DeviceAttributes.BATTERY_PERCENT] == 0
        assert self.device.attributes[B8DeviceAttributes.WORK_TIME] == 0
        assert self.device.attributes[B8DeviceAttributes.UV_SWITCH] is False
        assert self.device.attributes[B8DeviceAttributes.WIFI_SWITCH] is False
        assert self.device.attributes[B8DeviceAttributes.VOICE_SWITCH] is False
        assert self.device.attributes[B8DeviceAttributes.COMMAND_SOURCE] is False
        assert self.device.attributes[B8DeviceAttributes.DEVICE_ERROR] is False
        assert self.device.attributes[B8DeviceAttributes.ERROR_TYPE] == "reboot"
        assert (
            self.device.attributes[B8DeviceAttributes.ERROR_DESC]
            == "reboot_laser_comm_fail"
        )
        assert self.device.attributes[B8DeviceAttributes.MOP] == "off"
        assert self.device.attributes[B8DeviceAttributes.CARPET_SWITCH] is False
        assert self.device.attributes[B8DeviceAttributes.LASER_SENSOR_ERROR] is False
        assert self.device.attributes[B8DeviceAttributes.LASER_SENSOR_SHELTER] is False
        assert (
            self.device.attributes[B8DeviceAttributes.BOARD_COMMUNICATION_ERROR]
            is False
        )
        assert self.device.attributes[B8DeviceAttributes.SPEED] == "low"

    def test_query_response_no_error(self) -> None:
        """Test query response."""
        header = bytearray(
            [0xAA] + ([0x0] * 7) + [ProtocolVersion.V1] + [MessageType.query],
        )
        body = bytearray(
            [
                0x32,
                0x1,
                B8WorkStatus.NONE,
                B8FunctionType.NONE,
                B8ControlType.NONE,
                B8Moviment.NONE,
                B8CleanMode.NONE,
                B8FanLevel.OFF,
                0,
                B8WaterLevel.OFF,
                0,
                0,
                0,
                0,
                0,
                B8ErrorType.NO,
                B8ErrorRebootDescription.REBOOT_LASER_COMM_FAIL,
                B8MopState.OFF,
                0x0,
                0x0,
                B8Speed.LOW,
                0x0,  # CRC
            ],
        )
        self.device.process_message(bytearray(header + body))
        assert self.device.attributes[B8DeviceAttributes.WORK_STATUS] == "none"
        assert self.device.attributes[B8DeviceAttributes.FUNCTION_TYPE] == "none"
        assert self.device.attributes[B8DeviceAttributes.CONTROL_TYPE] == "none"
        assert self.device.attributes[B8DeviceAttributes.MOVE_DIRECTION] == "none"
        assert self.device.attributes[B8DeviceAttributes.CLEAN_MODE] == "none"
        assert self.device.attributes[B8DeviceAttributes.FAN_LEVEL] == "off"
        assert self.device.attributes[B8DeviceAttributes.AREA] == 0
        assert self.device.attributes[B8DeviceAttributes.WATER_LEVEL] == "off"
        assert self.device.attributes[B8DeviceAttributes.VOICE_VOLUME] == 0
        assert self.device.attributes[B8DeviceAttributes.HAVE_RESERVE_TASK] is False
        assert self.device.attributes[B8DeviceAttributes.BATTERY_PERCENT] == 0
        assert self.device.attributes[B8DeviceAttributes.WORK_TIME] == 0
        assert self.device.attributes[B8DeviceAttributes.UV_SWITCH] is False
        assert self.device.attributes[B8DeviceAttributes.WIFI_SWITCH] is False
        assert self.device.attributes[B8DeviceAttributes.VOICE_SWITCH] is False
        assert self.device.attributes[B8DeviceAttributes.COMMAND_SOURCE] is False
        assert self.device.attributes[B8DeviceAttributes.DEVICE_ERROR] is False
        assert self.device.attributes[B8DeviceAttributes.ERROR_TYPE] == "no"
        assert self.device.attributes[B8DeviceAttributes.ERROR_DESC] == "no"
        assert self.device.attributes[B8DeviceAttributes.MOP] == "off"
        assert self.device.attributes[B8DeviceAttributes.CARPET_SWITCH] is False
        assert self.device.attributes[B8DeviceAttributes.LASER_SENSOR_ERROR] is False
        assert self.device.attributes[B8DeviceAttributes.LASER_SENSOR_SHELTER] is False
        assert (
            self.device.attributes[B8DeviceAttributes.BOARD_COMMUNICATION_ERROR]
            is False
        )
        assert self.device.attributes[B8DeviceAttributes.SPEED] == "low"

    def test_unexpected_response(self) -> None:
        """Test unexpected response."""
        header = bytearray(
            [0xAA] + ([0x0] * 7) + [ProtocolVersion.V1] + [MessageType.query],
        )
        body = bytearray(
            [
                0x32,
                0x2,
            ]
            + [0x0] * 20,
        )

        with patch("midealocal.message.MessageResponse.set_attr") as mock_set_attr:
            self.device.process_message(bytearray(header + body))

            body = bytearray(
                [
                    0x42,
                    0x1,
                ]
                + [0x0] * 20,
            )
            self.device.process_message(bytearray(header + body))
            header[-1] = MessageType.notify1
            body = bytearray([0x32] + [0x0] * 20)
            self.device.process_message(bytearray(header + body))
            header[-1] = MessageType.set
            self.device.process_message(bytearray(header + body))
            mock_set_attr.assert_not_called()
