"""Test AC Device."""

from unittest.mock import patch

import pytest

from midealocal.const import ProtocolVersion
from midealocal.devices.ac import DeviceAttributes, MideaACDevice
from midealocal.devices.ac.message import (
    MessageCapabilitiesQuery,
    MessageNewProtocolQuery,
    MessagePowerQuery,
    MessageQuery,
    MessageSubProtocolQuery,
)


class TestMideaACDevice:
    """Test Midea AC Device."""

    device: MideaACDevice

    @pytest.fixture(autouse=True)
    def _setup_device(self) -> None:
        """Midea AC Device setup."""
        self.device = MideaACDevice(
            name="Test Device",
            device_id=1,
            ip_address="192.168.1.1",
            port=12345,
            token="AA",
            key="BB",
            device_protocol=ProtocolVersion.V1,
            model="test_model",
            subtype=1,
            customize='{"temperature_step": 1, "power_analysis_method": 2}',
        )

    def test_initial_attributes(self) -> None:
        """Test initial attributes."""
        assert self.device.attributes[DeviceAttributes.prompt_tone]
        assert not self.device.attributes[DeviceAttributes.power]
        assert self.device.attributes[DeviceAttributes.mode] == 0
        assert self.device.attributes[DeviceAttributes.target_temperature] == 24.0
        assert self.device.attributes[DeviceAttributes.fan_speed] == 102
        assert not self.device.attributes[DeviceAttributes.swing_vertical]
        assert not self.device.attributes[DeviceAttributes.swing_horizontal]
        assert self.device.temperature_step == 1
        assert self.device.fresh_air_fan_speeds is not None

    def test_set_attribute(self) -> None:
        """Test set attribute."""
        with (
            patch.object(self.device, "send_message_v2") as mock_build_send,
            patch(
                "midealocal.devices.ac.MessageACResponse",
            ) as mock_message_response,
        ):
            self.device.set_attribute(DeviceAttributes.power.value, True)
            mock_build_send.assert_called()

            self.device.set_attribute(DeviceAttributes.power.value, False)
            mock_build_send.assert_called()

            self.device.set_attribute(DeviceAttributes.mode.value, 2)
            mock_build_send.assert_called()

            self.device.set_target_temperature(26, 2)
            mock_build_send.assert_called()

            self.device.set_attribute(DeviceAttributes.prompt_tone.value, False)
            mock_build_send.assert_called()

            self.device.set_attribute(DeviceAttributes.screen_display.value, False)
            mock_build_send.assert_called()

            self.device.set_attribute(DeviceAttributes.breezeless.value, False)
            mock_build_send.assert_called()

            self.device.set_attribute(DeviceAttributes.indirect_wind.value, False)
            mock_build_send.assert_called()

            self.device.set_attribute(
                DeviceAttributes.screen_display_alternate.value,
                False,
            )
            mock_build_send.assert_called()

            mock_message = mock_message_response.return_value
            mock_message.used_subprotocol = True
            mock_message.timer = 30
            mock_message.fresh_air_power = False
            mock_message.fresh_air_1 = 1

            self.device.process_message(bytearray())

            self.device.set_attribute(DeviceAttributes.fresh_air_power.value, True)
            mock_build_send.assert_called()

            mock_message.fresh_air_1 = None
            mock_message.fresh_air_2 = 1
            self.device.process_message(bytearray())

            self.device.set_attribute(DeviceAttributes.fresh_air_mode.value, "Medium")
            mock_build_send.assert_called()

            self.device.set_attribute(DeviceAttributes.fresh_air_fan_speed.value, 50)
            mock_build_send.assert_called()

            self.device.set_attribute(DeviceAttributes.comfort_mode.value, True)
            mock_build_send.assert_called()

            self.device.set_attribute(DeviceAttributes.fresh_air_mode.value, False)
            mock_build_send.assert_called()

    def test_capabilities_query(self) -> None:
        """Test capabilities query."""
        queries = self.device.capabilities_query()
        assert len(queries) == 2
        assert isinstance(queries[0], MessageCapabilitiesQuery)
        assert isinstance(queries[1], MessageCapabilitiesQuery)

    def test_build_query(self) -> None:
        """Test build query."""
        self.device._used_subprotocol = True
        queries = self.device.build_query()
        assert len(queries) == 3
        assert isinstance(queries[0], MessageSubProtocolQuery)
        assert isinstance(queries[1], MessageSubProtocolQuery)
        assert isinstance(queries[2], MessageSubProtocolQuery)

        self.device._used_subprotocol = False
        queries = self.device.build_query()
        assert len(queries) == 3
        assert isinstance(queries[0], MessageQuery)
        assert isinstance(queries[1], MessageNewProtocolQuery)
        assert isinstance(queries[2], MessagePowerQuery)

    def test_process_message(self) -> None:
        """Test process message."""
        with patch("midealocal.devices.ac.MessageACResponse") as mock_message_response:
            mock_message = mock_message_response.return_value
            mock_message.used_subprotocol = False
            mock_message.prompt_tone = False
            mock_message.power = True
            mock_message.mode = 1
            mock_message.target_temperature = 25.0
            mock_message.fan_speed = 102
            mock_message.swing_vertical = True
            mock_message.swing_horizontal = True
            mock_message.smart_eye = True
            mock_message.dry = True
            mock_message.aux_heating = True
            mock_message.boost_mode = True
            mock_message.sleep_mode = True
            mock_message.frost_protect = True
            mock_message.comfort_mode = True
            mock_message.eco_mode = True
            mock_message.natural_wind = True
            mock_message.temp_fahrenheit = True
            mock_message.screen_display = True
            mock_message.screen_display_alternate = True
            mock_message.full_dust = True
            mock_message.indoor_temperature = None
            mock_message.outdoor_temperature = None
            mock_message.indoor_humidity = None
            mock_message.breezeless = True
            mock_message.total_energy_consumption = None
            mock_message.current_energy_consumption = None
            mock_message.realtime_power = None
            mock_message.fresh_air_power = True
            mock_message.fresh_air_fan_speed = 0
            mock_message.fresh_air_1 = 1
            mock_message.fresh_air_2 = 1

            result = self.device.process_message(bytearray())
            assert result[DeviceAttributes.power.value]
            assert not result[DeviceAttributes.prompt_tone.value]
            assert result[DeviceAttributes.mode.value] == 1
            assert result[DeviceAttributes.target_temperature.value] == 25.0
            assert result[DeviceAttributes.fan_speed.value] == 102
            assert result[DeviceAttributes.swing_vertical.value]
            assert result[DeviceAttributes.swing_horizontal.value]
            assert result[DeviceAttributes.smart_eye.value]
            assert result[DeviceAttributes.dry.value]
            assert result[DeviceAttributes.aux_heating.value]
            assert result[DeviceAttributes.boost_mode.value]
            assert result[DeviceAttributes.sleep_mode.value]
            assert result[DeviceAttributes.frost_protect.value]
            assert result[DeviceAttributes.comfort_mode.value]
            assert result[DeviceAttributes.eco_mode.value]
            assert result[DeviceAttributes.natural_wind.value]
            assert result[DeviceAttributes.temp_fahrenheit.value]
            assert result[DeviceAttributes.screen_display.value]
            assert result[DeviceAttributes.screen_display_alternate.value]
            assert result[DeviceAttributes.full_dust.value]
            assert result[DeviceAttributes.indoor_temperature.value] is None
            assert result[DeviceAttributes.outdoor_temperature.value] is None
            assert result[DeviceAttributes.indoor_humidity.value] is None
            assert result[DeviceAttributes.breezeless.value]
            assert result[DeviceAttributes.total_energy_consumption.value] is None
            assert result[DeviceAttributes.current_energy_consumption.value] is None
            assert result[DeviceAttributes.realtime_power.value] is None
            assert result[DeviceAttributes.fresh_air_power.value]
            assert result[DeviceAttributes.fresh_air_mode.value] == "Off"
            assert result[DeviceAttributes.fresh_air_1.value] == 1
            assert result[DeviceAttributes.fresh_air_2.value] == 1

            mock_message.fresh_air_fan_speed = 55
            mock_message.fresh_air_1 = None
            result = self.device.process_message(bytearray())
            assert result[DeviceAttributes.fresh_air_mode.value] == "Low"

            mock_message.fresh_air_power = False
            result = self.device.process_message(bytearray())
            assert result[DeviceAttributes.fresh_air_mode.value] == "Off"

            mock_message.power = False
            result = self.device.process_message(bytearray())
            assert not result[DeviceAttributes.screen_display.value]
            assert not self.device.attributes[DeviceAttributes.screen_display]

    def test_set_target_temperature(self) -> None:
        """Test set target temperature."""
        with patch.object(self.device, "build_send") as mock_build_send:
            self.device.set_target_temperature(22.5, 1)
            mock_build_send.assert_called_once()
            message = mock_build_send.call_args[0][0]
            assert message.target_temperature == 22.5
            assert message.mode == 1
            assert message.power
            self.device._used_subprotocol = True
            self.device.set_target_temperature(22.5, 1)

    def test_set_swing(self) -> None:
        """Test set swing."""
        with patch.object(self.device, "send_message_v2") as mock_build_send:
            self.device.set_swing(True, False)
            mock_build_send.assert_called()

    def test_invalid_customize_format(self) -> None:
        """Test invalid customize format."""
        self.device.set_customize("{")
