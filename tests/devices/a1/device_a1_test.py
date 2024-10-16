"""Test a1 Device."""

from unittest.mock import patch

import pytest

from midealocal.const import ProtocolVersion
from midealocal.devices.a1 import DeviceAttributes, MideaA1Device
from midealocal.devices.a1.message import MessageQuery, MessageSet


class TestMideaA1Device:
    """Test Midea A1 Device."""

    @pytest.fixture(autouse=True)
    def _setup_device(self) -> None:
        """Midea A1 Device setup."""
        self.device = MideaA1Device(
            name="Test Device",
            device_id=1,
            ip_address="192.168.1.100",
            port=6444,
            token="AA",
            key="BB",
            device_protocol=ProtocolVersion.V3,
            model="test_model",
            subtype=1,
            customize="test_customize",
        )

    def test_initial_attributes(self) -> None:
        """Test initial attributes."""
        assert not self.device.attributes[DeviceAttributes.power]
        assert self.device.attributes[DeviceAttributes.prompt_tone]
        assert self.device.attributes[DeviceAttributes.fan_speed] == "Medium"
        assert self.device.attributes[DeviceAttributes.target_humidity] == 35

    def test_modes(self) -> None:
        """Test modes."""
        assert self.device.modes == [
            "Manual",
            "Continuous",
            "Auto",
            "Clothes-Dry",
            "Shoes-Dry",
        ]

    def test_fan_speeds(self) -> None:
        """Test fan speeds."""
        assert self.device.fan_speeds == [
            "Lowest",
            "Low",
            "Medium",
            "High",
            "Auto",
            "Off",
        ]

    def test_water_level_sets(self) -> None:
        """Test water level sets."""
        assert self.device.water_level_sets == ["25", "50", "75", "100"]

    def test_process_message(self) -> None:
        """Test process message."""
        with patch("midealocal.devices.a1.MessageA1Response") as mock_message_response:
            mock_message = mock_message_response.return_value
            mock_message.protocol_version = ProtocolVersion.V3
            mock_message.power = True
            mock_message.prompt_tone = False
            mock_message.fan_speed = 40
            mock_message.target_humidity = 40
            mock_message.mode = 1
            mock_message.tank = 60
            mock_message.water_level_set = "50"
            new_status = self.device.process_message(b"")
            assert new_status[DeviceAttributes.power.value]
            assert not new_status[DeviceAttributes.prompt_tone.value]
            assert new_status[DeviceAttributes.fan_speed.value] == "Low"
            assert new_status[DeviceAttributes.target_humidity.value] == 40
            assert new_status[DeviceAttributes.tank_full.value]
            assert new_status[DeviceAttributes.mode.value] == "Manual"

            mock_message.mode = 10
            mock_message.fan_speed = 99
            mock_message.tank = 30
            new_status = self.device.process_message(b"")
            assert new_status[DeviceAttributes.mode.value] is None
            assert new_status[DeviceAttributes.fan_speed.value] is None
            assert not new_status[DeviceAttributes.tank_full.value]

    def test_build_query(self) -> None:
        """Test build query."""
        queries = self.device.build_query()
        assert len(queries) == 1
        assert isinstance(queries[0], MessageQuery)

    def test_make_message_set(self) -> None:
        """Test make message set."""
        with patch("midealocal.devices.a1.MessageA1Response") as mock_message_response:
            mock_message = mock_message_response.return_value
            mock_message.protocol_version = ProtocolVersion.V3
            mock_message.power = True
            mock_message.prompt_tone = False
            mock_message.fan_speed = 40
            mock_message.target_humidity = 40
            mock_message.mode = 1
            mock_message.tank = 60
            mock_message.water_level_set = "50"
            self.device.process_message(b"")

        message_set = self.device.make_message_set()
        assert isinstance(message_set, MessageSet)
        assert message_set.power
        assert not message_set.prompt_tone
        assert message_set.fan_speed == 40
        assert message_set.mode == 1

    def test_set_attribute(self) -> None:
        """Test set attribute."""
        with patch.object(self.device, "build_send") as mock_build_send:
            self.device.set_attribute(DeviceAttributes.mode, "Continuous")
            mock_build_send.assert_called_once()

            self.device.set_attribute(DeviceAttributes.fan_speed, "Medium")
            mock_build_send.assert_called()

            self.device.set_attribute(DeviceAttributes.water_level_set, "75")
            mock_build_send.assert_called()

            self.device.set_attribute(DeviceAttributes.prompt_tone, True)
            mock_build_send.assert_called()

            self.device.set_attribute(DeviceAttributes.swing, True)
            mock_build_send.assert_called()
