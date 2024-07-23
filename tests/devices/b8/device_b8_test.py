"""Test B8 Device."""

from unittest.mock import patch

import pytest

from midealocal.devices.b8 import MideaB8Device
from midealocal.devices.b8.const import (
    B8CleanMode,
    B8ControlType,
    B8DeviceAttributes,
    B8ErrorType,
    B8FanLevel,
    B8FunctionType,
    B8MopState,
    B8Moviment,
    B8Speed,
    B8WaterLevel,
    B8WorkStatus,
)
from midealocal.devices.b8.message import (
    MessageQuery,
)


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
            protocol=1,
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

    def test_build_query(self) -> None:
        """Test build query."""
        queries = self.device.build_query()
        assert len(queries) == 1
        assert isinstance(queries[0], MessageQuery)
