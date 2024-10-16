"""Test da Device."""

from unittest.mock import patch

import pytest

from midealocal.const import ProtocolVersion
from midealocal.devices.da import DeviceAttributes, MideaDADevice
from midealocal.devices.da.message import MessageQuery
from midealocal.exceptions import ValueWrongType


class TestMideaDADevice:
    """Test Midea DA Device."""

    device: MideaDADevice

    @pytest.fixture(autouse=True)
    def _setup_device(self) -> None:
        """Midea DA Device setup."""
        self.device = MideaDADevice(
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
        assert not self.device.attributes[DeviceAttributes.start]
        assert self.device.attributes[DeviceAttributes.error_code] is None
        assert self.device.attributes[DeviceAttributes.washing_data] == bytearray([])
        assert self.device.attributes[DeviceAttributes.program] is None
        assert self.device.attributes[DeviceAttributes.progress] == "Unknown"
        assert self.device.attributes[DeviceAttributes.time_remaining] is None
        assert self.device.attributes[DeviceAttributes.wash_time] is None
        assert self.device.attributes[DeviceAttributes.soak_time] is None
        assert self.device.attributes[DeviceAttributes.dehydration_time] is None
        assert self.device.attributes[DeviceAttributes.dehydration_speed] is None
        assert self.device.attributes[DeviceAttributes.rinse_count] is None
        assert self.device.attributes[DeviceAttributes.rinse_level] is None
        assert self.device.attributes[DeviceAttributes.wash_level] is None
        assert self.device.attributes[DeviceAttributes.wash_strength] is None
        assert self.device.attributes[DeviceAttributes.softener] is None
        assert self.device.attributes[DeviceAttributes.detergent] is None

    def test_process_message(self) -> None:
        """Test process message."""
        with patch("midealocal.devices.da.MessageDAResponse") as mock_message_response:
            mock_message = mock_message_response.return_value
            mock_message.protocol_version = ProtocolVersion.V3
            mock_message.power = True
            mock_message.start = True
            mock_message.error_code = 10
            mock_message.program = 5
            mock_message.wash_time = 30
            mock_message.soak_time = 10
            mock_message.dehydration_time = 2
            mock_message.dehydration_speed = 3
            mock_message.rinse_count = 3
            mock_message.rinse_level = 4
            mock_message.wash_level = 1
            mock_message.wash_strength = 2
            mock_message.softener = 5
            mock_message.detergent = 4
            mock_message.progress = 2
            mock_message.time_remaining = 15 + 60
            new_status = self.device.process_message(b"")
            assert new_status[DeviceAttributes.power.value]
            assert new_status[DeviceAttributes.start.value]
            assert new_status[DeviceAttributes.error_code.value] == 10
            assert new_status[DeviceAttributes.program.value] == "Memory"
            assert new_status[DeviceAttributes.progress.value] == "Rinse"
            assert new_status[DeviceAttributes.time_remaining.value] == 75
            assert new_status[DeviceAttributes.wash_time.value] == 30
            assert new_status[DeviceAttributes.soak_time.value] == 10
            assert new_status[DeviceAttributes.dehydration_time.value] == 2
            assert new_status[DeviceAttributes.dehydration_speed.value] == "High"
            assert new_status[DeviceAttributes.rinse_count.value] == 3
            assert new_status[DeviceAttributes.rinse_level.value] == 4
            assert new_status[DeviceAttributes.wash_level.value] == 1
            assert new_status[DeviceAttributes.wash_strength.value] == "Medium"
            assert new_status[DeviceAttributes.softener.value] == "5"
            assert new_status[DeviceAttributes.detergent.value] == "4"

            mock_message.progress = 15
            mock_message.program = 15
            mock_message.rinse_level = 15
            mock_message.dehydration_speed = 15
            mock_message.detergent = 15
            mock_message.softener = 15
            mock_message.wash_strength = 15
            new_status = self.device.process_message(b"")
            assert new_status[DeviceAttributes.program.value] is None
            assert new_status[DeviceAttributes.progress.value] is None
            assert new_status[DeviceAttributes.rinse_level.value] == "-"
            assert new_status[DeviceAttributes.dehydration_speed.value] is None
            assert new_status[DeviceAttributes.softener.value] is None
            assert new_status[DeviceAttributes.detergent.value] is None
            assert new_status[DeviceAttributes.wash_strength.value] is None

    def test_build_query(self) -> None:
        """Test build query."""
        queries = self.device.build_query()
        assert len(queries) == 1
        assert isinstance(queries[0], MessageQuery)

    def test_set_attribute(self) -> None:
        """Test set attribute."""
        with patch.object(self.device, "build_send") as mock_build_send:
            self.device.set_attribute(DeviceAttributes.power, True)
            mock_build_send.assert_called_once()

            self.device.set_attribute(DeviceAttributes.start, True)
            mock_build_send.assert_called()

            with pytest.raises(ValueWrongType):
                self.device.set_attribute(DeviceAttributes.start, "On")
