"""Test 40 Device."""

from unittest.mock import patch

import pytest

from midealocal.const import ProtocolVersion
from midealocal.devices.x40 import DeviceAttributes, MideaX40Device


class TestMideaX40Device:
    """Test Midea 40 Device."""

    device: MideaX40Device

    @pytest.fixture(autouse=True)
    def _setup_device(self) -> None:
        """Midea DA Device setup."""
        self.device = MideaX40Device(
            name="Test Device",
            device_id=1,
            ip_address="192.168.1.100",
            port=6444,
            token="AA",
            key="BB",
            device_protocol=ProtocolVersion.V3,
            model="test_model",
            subtype=1,
            customize="",
        )

    def test_customize(self) -> None:
        """Test precision halves."""
        with patch(
            "midealocal.devices.x40.MessageX40Response",
        ) as mock_message_response:
            mock_message = mock_message_response.return_value
            mock_message.light = True
            mock_message.ventilation = True
            mock_message.fan_speed = 1
            mock_message.direction = 5
            mock_message.smelly_sensor = True

            mock_message.current_temperature = 53
            new_status = self.device.process_message(b"")
            assert new_status[DeviceAttributes.current_temperature] == 53

            self.device.set_customize('{"precision_halves": true}')
            assert self.device.precision_halves is True
            mock_message.current_temperature = 53
            new_status = self.device.process_message(b"")
            assert new_status[DeviceAttributes.current_temperature] == 26.5

            self.device.set_customize("{")  # Test invalid json
            assert self.device.precision_halves is False
