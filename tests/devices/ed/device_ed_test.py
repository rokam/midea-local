"""Test ED Device."""

from unittest.mock import patch

import pytest

from midealocal.const import ProtocolVersion
from midealocal.devices.ed import DeviceAttributes, MideaEDDevice
from midealocal.devices.ed.message import MessageQuery, MessageQuery01


class TestMideaEDDevice:
    """Test Midea ED Device."""

    device: MideaEDDevice

    @pytest.fixture(autouse=True)
    def _setup_device(self) -> None:
        """Midea ed Device setup."""
        self.device = MideaEDDevice(
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
        assert self.device.attributes[DeviceAttributes.water_consumption] is None
        assert self.device.attributes[DeviceAttributes.in_tds] is None
        assert self.device.attributes[DeviceAttributes.out_tds] is None
        assert self.device.attributes[DeviceAttributes.filter1] is None
        assert self.device.attributes[DeviceAttributes.filter2] is None
        assert self.device.attributes[DeviceAttributes.filter3] is None
        assert self.device.attributes[DeviceAttributes.life1] is None
        assert self.device.attributes[DeviceAttributes.life2] is None
        assert self.device.attributes[DeviceAttributes.life3] is None
        assert not self.device.attributes[DeviceAttributes.child_lock]

    def test_process_message(self) -> None:
        """Test process message."""
        with patch("midealocal.devices.ed.MessageEDResponse") as mock_message_response:
            mock_message = mock_message_response.return_value
            mock_message.protocol_version = ProtocolVersion.V3
            mock_message.power = True
            mock_message.water_consumption = 123
            mock_message.in_tds = 200
            mock_message.out_tds = 5
            mock_message.filter1 = 30
            mock_message.filter2 = 20
            mock_message.filter3 = 10
            mock_message.life1 = 2
            mock_message.life2 = 3
            mock_message.life3 = 4
            mock_message.child_lock = True
            new_status = self.device.process_message(b"")
            assert new_status[DeviceAttributes.power.value]
            assert new_status[DeviceAttributes.water_consumption.value] == 123
            assert new_status[DeviceAttributes.in_tds.value] == 200
            assert new_status[DeviceAttributes.out_tds.value] == 5
            assert new_status[DeviceAttributes.filter1.value] == 30
            assert new_status[DeviceAttributes.filter2.value] == 20
            assert new_status[DeviceAttributes.filter3.value] == 10
            assert new_status[DeviceAttributes.life1.value] == 2
            assert new_status[DeviceAttributes.life2.value] == 3
            assert new_status[DeviceAttributes.life3.value] == 4

            mock_message.child_lock = False
            mock_message.water_consumption = 456
            mock_message.in_tds = 300
            mock_message.out_tds = 15
            mock_message.filter1 = 15
            mock_message.life3 = 15
            new_status = self.device.process_message(b"")
            assert not new_status[DeviceAttributes.child_lock.value]
            assert new_status[DeviceAttributes.water_consumption.value] == 456
            assert new_status[DeviceAttributes.in_tds.value] == 300
            assert new_status[DeviceAttributes.out_tds.value] == 15
            assert new_status[DeviceAttributes.filter1.value] == 15
            assert new_status[DeviceAttributes.life3.value] == 15

    def test_build_query(self) -> None:
        """Test build query."""
        queries = self.device.build_query()
        assert len(queries) == 2
        assert isinstance(queries[0], MessageQuery)
        assert isinstance(queries[1], MessageQuery01)

    def test_set_attribute(self) -> None:
        """Test set attribute."""
        with patch.object(self.device, "build_send") as mock_build_send:
            self.device.set_attribute(DeviceAttributes.power, True)
            mock_build_send.assert_called_once()

            self.device.set_attribute(DeviceAttributes.child_lock, True)
            mock_build_send.assert_called()
