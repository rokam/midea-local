"""Test ac message."""

import pytest

from midealocal.const import ProtocolVersion
from midealocal.devices.ac.message import (
    MessageACBase,
    MessageACResponse,
    MessageCapabilitiesQuery,
    MessageGeneralSet,
    MessageNewProtocolQuery,
    MessagePowerQuery,
    MessageQuery,
    MessageSubProtocol,
    MessageSubProtocolSet,
    MessageToggleDisplay,
    NewProtocolTags,
)
from midealocal.message import ListTypes, MessageType


class TestMessageACBase:
    """Test AC Message Base."""

    def test_message_id_increment(self) -> None:
        """Test message Id Increment."""
        msg = MessageACBase(
            protocol_version=ProtocolVersion.V1,
            message_type=MessageType.query,
            body_type=ListTypes.X01,
        )
        msg2 = MessageACBase(
            protocol_version=ProtocolVersion.V1,
            message_type=MessageType.query,
            body_type=ListTypes.X01,
        )
        assert msg2._message_id == msg._message_id + 1
        # test reset
        for _ in range(254 - msg2._message_id):
            msg = MessageACBase(
                protocol_version=ProtocolVersion.V1,
                message_type=MessageType.query,
                body_type=ListTypes.X01,
            )
        assert msg._message_id == 1

    def test_body_not_implemented(self) -> None:
        """Test body not implemented."""
        msg = MessageACBase(
            protocol_version=ProtocolVersion.V1,
            message_type=MessageType.query,
            body_type=ListTypes.X01,
        )
        with pytest.raises(NotImplementedError):
            _ = msg.body


class TestMessageQuery:
    """Test Message Query."""

    def test_query_body(self) -> None:
        """Test query body."""
        msg = MessageQuery(protocol_version=ProtocolVersion.V1)
        expected_body = bytearray(
            [
                0x41,
                0x81,
                0x00,
                0xFF,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )
        assert msg.body[:-2] == expected_body


class TestMessageCapabilitiesQuery:
    """Test Message Capabilities Query."""

    def test_capabilities_query_body(self) -> None:
        """Test capabilities query body."""
        msg = MessageCapabilitiesQuery(ProtocolVersion.V1, False)
        expected_body = bytearray(
            [0xB5, 0x01, 0x00],
        )
        assert msg.body[:-2] == expected_body

    def test_capabilities_query_body_additional(self) -> None:
        """Test capabilities query body."""
        msg = MessageCapabilitiesQuery(ProtocolVersion.V1, True)
        expected_body = bytearray(
            [0xB5, 0x01, 0x01, 0x01],
        )
        assert msg.body[:-2] == expected_body


class TestMessagePowerQuery:
    """Test Message Power Query."""

    def test_power_query_body(self) -> None:
        """Test power query body."""
        msg = MessagePowerQuery(protocol_version=ProtocolVersion.V1)
        expected_body = bytearray([0x41, 0x21, 0x01, 0x44, 0x00, 0x01])
        assert msg.body[:-1] == expected_body


class TestMessageToggleDisplay:
    """Test Message Toggle Display."""

    def test_toggle_disply_body(self) -> None:
        """Test toggle display body."""
        msg = MessageToggleDisplay(protocol_version=ProtocolVersion.V1)
        expected_body = bytearray(
            [
                0x41,
                0x02,
                0x00,
                0xFF,
                0x02,
                0x00,
                0x02,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )
        assert msg.body[:-2] == expected_body
        msg.prompt_tone = True
        expected_body = bytearray(
            [
                0x41,
                0x02 | 0x40,
                0x00,
                0xFF,
                0x02,
                0x00,
                0x02,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )
        assert msg.body[:-2] == expected_body


class TestMessageNewProtocolQuery:
    """Test Message New Protocol Query."""

    def test_new_protocol_query_body(self) -> None:
        """Test new protocol query body."""
        msg = MessageNewProtocolQuery(protocol_version=ProtocolVersion.V1)
        expected_body = bytearray(
            [
                0xB1,
                0x06,
                NewProtocolTags.indirect_wind & 0xFF,
                NewProtocolTags.indirect_wind >> 8,
                NewProtocolTags.breezeless & 0xFF,
                NewProtocolTags.breezeless >> 8,
                NewProtocolTags.indoor_humidity & 0xFF,
                NewProtocolTags.indoor_humidity >> 8,
                NewProtocolTags.screen_display & 0xFF,
                NewProtocolTags.screen_display >> 8,
                NewProtocolTags.fresh_air_1 & 0xFF,
                NewProtocolTags.fresh_air_1 >> 8,
                NewProtocolTags.fresh_air_2 & 0xFF,
                NewProtocolTags.fresh_air_2 >> 8,
            ],
        )
        assert msg.body[:-2] == expected_body


class TestMessageSubProtocol:
    """Test Message Sub Protocol."""

    def test_sub_protocol_body(self) -> None:
        """Test sub protocol body."""
        msg = MessageSubProtocol(
            protocol_version=ProtocolVersion.V1,
            message_type=MessageType.query,
            subprotocol_query_type=0xCC,
        )
        expected_body = bytearray(
            [
                0xAA,
                0x08,
                0x00,
                0xFF,
                0xFF,
                0xCC,
            ],
        )
        assert msg.body[:-2] == expected_body


class TestMessageSubProtocolSet:
    """Test Message Sub Protocol Set."""

    def test_sub_protocol_set_body(self) -> None:
        """Test sub protocol set body."""
        msg = MessageSubProtocolSet(protocol_version=ProtocolVersion.V1)
        expected_body = bytearray(
            [
                0xAA,
                45,
                0x00,
                0xFF,
                0xFF,
                0x20,
                0x02,
                0x80,
                0x00,
                0x00,
                0x00,
                0x00,
                20 * 2 + 30,
                102,
                0x32,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x01,
                0x01,
                0x00,
                0x01,
                19 * 2 + 50,
                0x00,
                20 * 2 + 30,
                0x32,
                0x66,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x08,
            ],
        )
        assert msg.body[:-2] == expected_body

        msg.power = True
        msg.mode = 6
        msg.target_temperature = 24.0
        msg.fan_speed = 90
        msg.boost_mode = True
        msg.aux_heating = True
        msg.dry = True
        msg.eco_mode = True
        msg.sleep_mode = True
        msg.sn8_flag = True
        msg.timer = True
        msg.prompt_tone = True
        expected_body[6] = 0x02 | 0x20 | 0x01 | 0x10
        expected_body[7] = 0x40
        expected_body[8] = 0x80
        expected_body[11] = 0x02
        expected_body[12] = 24 * 2 + 30
        expected_body[13] = 90
        expected_body[25] = 23 * 2 + 50
        expected_body[26] = 0x01
        expected_body[27] = 24 * 2 + 30
        expected_body[31] = 0x40 | 0x04
        assert msg.body[:-2] == expected_body


class TestMessageGeneralSet:
    """Test Message General Set."""

    def test_general_set_body(self) -> None:
        """Test general set body."""
        msg = MessageGeneralSet(protocol_version=ProtocolVersion.V1)
        expected_body = bytearray(
            [
                0x40,
                0x40,
                0x00 | (20 & 0xF) | (0x10 if 20 % 2 != 0 else 0),
                102 & 0x7F,
                0x00,
                0x00,
                0x00,
                0x30,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )
        assert msg.body[:-2] == expected_body
        msg.power = True
        msg.prompt_tone = False
        msg.mode = 2
        msg.target_temperature = 24.0
        msg.fan_speed = 92
        msg.swing_vertical = True
        msg.swing_horizontal = True
        msg.boost_mode = True
        msg.smart_eye = True
        msg.dry = True
        msg.aux_heating = True
        msg.eco_mode = True
        msg.temp_fahrenheit = True
        msg.sleep_mode = True
        msg.natural_wind = True
        msg.frost_protect = True
        msg.comfort_mode = True
        expected_body[1] = 0x01
        expected_body[2] = (
            (0x02 << 5) & 0xE0 | (24 & 0xF) | (0x10 if 24 % 2 != 0 else 0)
        )
        expected_body[3] = 92 & 0x7F
        expected_body[7] = 0x30 | 0x0C | 0x03
        expected_body[8] = 0x20
        expected_body[9] = 0x01 | 0x04 | 0x08 | 0x80
        expected_body[10] = 0x04 | 0x01 | 0x02
        expected_body[17] = 0x40
        expected_body[21] = 0x80
        expected_body[22] = 0x01
        assert msg.body[:-2] == expected_body


class TestMessageACResponse:
    """Test Message AC Response."""

    @pytest.fixture(autouse=True)
    def _setup_header(self) -> None:
        """Do setup header."""
        self.header = bytearray(
            [
                0xAA,
                0x00,
                0xA1,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x01,
                0x05,
            ],
        )

    def test_message_notify2_a0(self) -> None:
        """Test Message parse notify2 A0."""
        body = bytearray(18)
        body[0] = 0xA0  # Body type
        body[1] = 0b01011111  # Power on, target temperature with 0.5 increment
        body[2] = 0b11100000  # Mode
        body[3] = 0b01111111  # Fan speed
        body[7] = 0b00001111  # Swing vertical and horizontal
        body[8] = 0b00100000  # Boost mode
        body[9] = 0b00011101  # Smart eye, dry, aux heating, eco mode
        body[10] = 0b01000011  # Sleep mode, natural wind
        body[13] = 0b00100000  # Full dust
        body[14] = 0b00000001  # Comfort mode

        response = MessageACResponse(self.header + body)
        assert hasattr(response, "power")
        assert hasattr(response, "target_temperature")
        assert response.target_temperature == 27.5  # ((31 >> 1) - 4 + 16 + 0.5) = 27.5
        assert hasattr(response, "mode")
        assert response.mode == 7
        assert hasattr(response, "fan_speed")
        assert response.fan_speed == 127
        assert hasattr(response, "swing_vertical")
        assert hasattr(response, "swing_horizontal")
        assert hasattr(response, "boost_mode")
        assert hasattr(response, "smart_eye")
        assert hasattr(response, "dry")
        assert hasattr(response, "aux_heating")
        assert hasattr(response, "eco_mode")
        assert hasattr(response, "sleep_mode")
        assert hasattr(response, "natural_wind")
        assert hasattr(response, "full_dust")
        assert hasattr(response, "comfort_mode")

    def test_message_notify1_a1(self) -> None:
        """Test Message parse notify1 A1."""
        self.header[9] = 0x04
        body = bytearray(22)
        body[0] = 0xA1  # Body type
        body[13] = 100  # Indoor temperature byte
        body[14] = 60  # Outdoor temperature byte
        body[17] = 50  # Indoor humidity byte
        body[18] = 0xF3  # Decimal part for temperature
        response = MessageACResponse(self.header + body)

        assert hasattr(response, "indoor_temperature")
        assert response.indoor_temperature == 25.3  # ((100 - 50) / 2) + 0.3 = 25.3
        assert hasattr(response, "outdoor_temperature")
        assert response.outdoor_temperature == 6.5  # ((60 - 50) / 2) + 1.5 = 6.5
        assert hasattr(response, "indoor_humidity")
        assert response.indoor_humidity == 50

        body[14] = 0xFF  # Outdoor temperature byte
        response = MessageACResponse(self.header + body)
        assert hasattr(response, "outdoor_temperature")
        assert response.outdoor_temperature is None

        body[13] = 48  # Indoor temperature byte
        body[14] = 40  # Outdoor temperature byte
        response = MessageACResponse(self.header + body)
        assert hasattr(response, "indoor_temperature")
        assert response.indoor_temperature == -1.3  # ((49 - 50) / 2) - 0.3 = -1.3
        assert hasattr(response, "outdoor_temperature")
        assert response.outdoor_temperature == -6.5  # ((40 - 50) / 2) - 1.5 = -6.5

    def test_message_query_b5(self) -> None:
        """Test message query b5."""
        body = bytearray(
            [
                0xB5,
                0x07,
                0x12,
                0x02,
                0x01,
                0x01,
                0x13,
                0x02,
                0x01,
                0x00,
                0x14,
                0x02,
                0x01,
                0x00,
                0x15,
                0x02,
                0x01,
                0x01,
                0x16,
                0x02,
                0x01,
                0x01,
                0x17,
                0x02,
                0x01,
                0x01,
                0x1A,
                0x02,
                0x01,
                0x01,
                0xD6,
            ],
        )
        response = MessageACResponse(self.header + body)
        assert hasattr(response, "modes")
        assert not response.modes["heat"]
        assert response.modes["cool"]
        assert response.modes["dry"]
        assert response.modes["auto"]

    def test_message_notify2_b0(self) -> None:
        """Test Message parse notify2 B0."""
        body = bytearray(29)
        body[0] = 0xB0  # Body type
        body[1] = 0x05  # Params count
        body[2] = NewProtocolTags.indirect_wind & 0xFF  # Low byte param
        body[3] = NewProtocolTags.indirect_wind >> 8  # High byte param
        body[5] = 0x01  # Value length
        body[6] = 0x02  # Value True
        body[7] = NewProtocolTags.indoor_humidity & 0xFF  # Low byte param
        body[8] = NewProtocolTags.indoor_humidity >> 8  # High byte param
        body[10] = 0x01  # Value length
        body[11] = 30  # Value 30
        body[12] = NewProtocolTags.breezeless & 0xFF  # Low byte param
        body[13] = NewProtocolTags.breezeless >> 8  # High byte param
        body[15] = 0x01  # Value length
        body[16] = 0x01  # Value True
        body[17] = NewProtocolTags.screen_display & 0xFF  # Low byte param
        body[18] = NewProtocolTags.screen_display >> 8  # High byte param
        body[20] = 0x01  # Value length
        body[21] = 0x01  # Value True
        body[22] = NewProtocolTags.fresh_air_1 & 0xFF  # Low byte param
        body[23] = NewProtocolTags.fresh_air_1 >> 8  # High byte param
        body[25] = 0x02  # Value length
        body[26] = 0x02  # Value Power True
        body[27] = 10  # Value Speed 10

        response = MessageACResponse(self.header + body)

        assert hasattr(response, "indirect_wind")
        assert hasattr(response, "indoor_humidity")
        assert response.indoor_humidity == 30
        assert hasattr(response, "breezeless")
        assert hasattr(response, "screen_display_alternate")
        assert hasattr(response, "screen_display_new")
        assert hasattr(response, "fresh_air_1")
        assert hasattr(response, "fresh_air_power")
        assert hasattr(response, "fresh_air_fan_speed")
        assert response.fresh_air_fan_speed == 10

        body[22] = NewProtocolTags.fresh_air_2 & 0xFF  # Low byte param
        body[23] = NewProtocolTags.fresh_air_2 >> 8  # High byte param
        body[25] = 0x02  # Value length
        body[26] = 0x01  # Value Power True
        body[27] = 20  # Value Speed 20

        response = MessageACResponse(self.header + body)
        assert not hasattr(response, "fresh_air_1")
        assert hasattr(response, "fresh_air_2")
        assert hasattr(response, "fresh_air_power")
        assert hasattr(response, "fresh_air_fan_speed")
        assert response.fresh_air_fan_speed == 20

    def test_message_query_c0(self) -> None:
        """Test Message parse query C0."""
        self.header[9] = 0x03
        body = bytearray(24)
        body[0] = 0xC0  # Body type
        body[1] = 0b00000001  # Power on
        body[2] = 0b10101110  # Mode (5), target temperature (14), 0.5 increment
        body[3] = 0b01111111  # Fan speed
        body[7] = 0b00001111  # Swing vertical and horizontal
        body[8] = 0b01100000  # Boost mode, smart eye
        body[9] = 0b00011110  # Natural wind, dry, eco mode, aux heating
        body[10] = 0b01000111  # Sleep mode, temp Fahrenheit, boost mode (alternative)
        body[11] = 0x64  # Indoor temperature byte
        body[12] = 0x64  # Outdoor temperature byte
        body[13] = 0b00100000  # Full dust
        body[14] = 0b01110000  # Screen display
        body[15] = 0b00110010  # Decimal parts for temperature
        body[21] = 0b10000000  # Frost protect
        body[22] = 0b00000001  # Comfort mode

        response = MessageACResponse(self.header + body)
        assert hasattr(response, "power")
        assert hasattr(response, "mode")
        assert response.mode == 5
        assert hasattr(response, "target_temperature")
        assert response.target_temperature == 30  # 14 + 16
        assert hasattr(response, "fan_speed")
        assert response.fan_speed == 127
        assert hasattr(response, "swing_vertical")
        assert hasattr(response, "swing_horizontal")
        assert hasattr(response, "boost_mode")
        assert hasattr(response, "smart_eye")
        assert hasattr(response, "natural_wind")
        assert hasattr(response, "dry")
        assert hasattr(response, "eco_mode")
        assert hasattr(response, "aux_heating")
        assert hasattr(response, "temp_fahrenheit")
        assert hasattr(response, "sleep_mode")
        assert hasattr(response, "indoor_temperature")
        assert response.indoor_temperature == 25.2  # ((100 - 50) / 2) + 0.2
        assert hasattr(response, "outdoor_temperature")
        assert response.outdoor_temperature == 25.3  # ((100 - 50) / 2) + 0.3
        assert hasattr(response, "full_dust")
        assert hasattr(response, "screen_display")
        assert response.screen_display is False
        assert hasattr(response, "frost_protect")
        assert hasattr(response, "comfort_mode")

        body[11] = 40  # Indoor temperature byte
        body[12] = 40  # Outdoor temperature byte
        response = MessageACResponse(self.header + body)
        assert hasattr(response, "indoor_temperature")
        assert response.indoor_temperature == -5.2  # ((40 - 50) / 2) - 0.2
        assert hasattr(response, "outdoor_temperature")
        assert response.outdoor_temperature == -5.3  # ((40 - 50) / 2) - 0.3

        body[12] = 0xFF  # Outdoor temperature byte
        response = MessageACResponse(self.header + body)
        assert hasattr(response, "outdoor_temperature")
        assert response.outdoor_temperature is None

    def test_message_query_c1_method1(self) -> None:
        """Test Message parse query C1 method1."""
        self.header[9] = 0x03
        body = bytearray(20)
        body[0] = 0xC1  # Body type
        body[3] = 0x44  # Set the type to 0x44

        # Total energy consumption bytes
        body[4] = 0x12  # High nibble: 1, Low nibble: 2 (value: 12)
        body[5] = 0x34  # High nibble: 3, Low nibble: 4 (value: 34)
        body[6] = 0x56  # High nibble: 5, Low nibble: 6 (value: 56)
        body[7] = 0x78  # High nibble: 7, Low nibble: 8 (value: 78)
        expected_total_energy = float(12 * 1000000 + 34 * 10000 + 56 * 100 + 78) / 100

        # Current energy consumption bytes
        body[12] = 0x87  # High nibble: 8, Low nibble: 7 (value: 87)
        body[13] = 0x65  # High nibble: 6, Low nibble: 5 (value: 65)
        body[14] = 0x43  # High nibble: 4, Low nibble: 3 (value: 43)
        body[15] = 0x21  # High nibble: 2, Low nibble: 1 (value: 21)
        expected_current_energy = float(87 * 1000000 + 65 * 10000 + 43 * 100 + 21) / 100

        # Real-time power bytes
        body[16] = 0x11  # High nibble: 1, Low nibble: 1 (value: 11)
        body[17] = 0x22  # High nibble: 2, Low nibble: 2 (value: 22)
        body[18] = 0x33  # High nibble: 3, Low nibble: 3 (value: 33)
        expected_realtime_power = float(11 * 10000 + 22 * 100 + 33) / 10

        response = MessageACResponse(self.header + body, 1)

        assert hasattr(response, "total_energy_consumption")
        assert response.total_energy_consumption == expected_total_energy
        assert hasattr(response, "current_energy_consumption")
        assert response.current_energy_consumption == expected_current_energy
        assert hasattr(response, "realtime_power")
        assert response.realtime_power == expected_realtime_power

    def test_message_query_c1_method2(self) -> None:
        """Test Message parse query C1 method2."""
        self.header[9] = 0x03
        body = bytearray(20)
        body[0] = 0xC1  # Body type
        body[3] = 0x44  # Set the type to 0x44

        # Total energy consumption bytes
        body[4] = 0x01
        body[5] = 0x23
        body[6] = 0x45
        body[7] = 0x67
        expected_total_energy = (
            float((0x01 << 32) + (0x23 << 16) + (0x45 << 8) + 0x67) / 10
        )

        # Current energy consumption bytes
        body[12] = 0x89
        body[13] = 0xAB
        body[14] = 0xCD
        body[15] = 0xEF
        expected_current_energy = (
            float((0x89 << 32) + (0xAB << 16) + (0xCD << 8) + 0xEF) / 10
        )

        # Real-time power bytes
        body[16] = 0x12
        body[17] = 0x34
        body[18] = 0x56
        expected_realtime_power = float((0x12 << 16) + (0x34 << 8) + 0x56) / 10

        response = MessageACResponse(self.header + body, 2)

        assert hasattr(response, "total_energy_consumption")
        assert response.total_energy_consumption == expected_total_energy
        assert hasattr(response, "current_energy_consumption")
        assert response.current_energy_consumption == expected_current_energy
        assert hasattr(response, "realtime_power")
        assert response.realtime_power == expected_realtime_power

    def test_message_query_c1_method3(self) -> None:
        """Test Message parse query C1 method3."""
        self.header[9] = 0x03
        body = bytearray(20)
        body[0] = 0xC1  # Body type
        body[3] = 0x44  # Set the type to 0x44
        # Total energy consumption bytes
        body[4] = 0x12
        body[5] = 0x34
        body[6] = 0x56
        body[7] = 0x78
        expected_total_energy = (
            float(0x12 * 1000000 + 0x34 * 10000 + 0x56 * 100 + 0x78) / 100
        )

        # Current energy consumption bytes
        body[12] = 0x87
        body[13] = 0x65
        body[14] = 0x43
        body[15] = 0x21
        expected_current_energy = (
            float(0x87 * 1000000 + 0x65 * 10000 + 0x43 * 100 + 0x21) / 100
        )
        # Real-time power bytes
        body[16] = 0x11
        body[17] = 0x22
        body[18] = 0x33
        expected_realtime_power = float(0x11 * 10000 + 0x22 * 100 + 0x33) / 10
        response = MessageACResponse(self.header + body)

        assert hasattr(response, "total_energy_consumption")
        assert response.total_energy_consumption == expected_total_energy
        assert hasattr(response, "current_energy_consumption")
        assert response.current_energy_consumption == expected_current_energy
        assert hasattr(response, "realtime_power")
        assert response.realtime_power == expected_realtime_power

    def test_message_query_c1_0x40(self) -> None:
        """Test Message parse query C1 0x40."""
        self.header[9] = 0x03
        body = bytearray(20)
        body[0] = 0xC1  # Body type
        body[3] = 0x40
        response = MessageACResponse(self.header + body)
        assert not hasattr(response, "total_energy_consumption")
        assert not hasattr(response, "current_energy_consumption")
        assert not hasattr(response, "realtime_power")

    def test_message_query_bb_0x20(self) -> None:
        """Test Message parse query BB 0x20."""
        self.header[9] = 0x03
        body = bytearray(100)
        body[:6] = bytearray([0xBB, 0, 0, 0, 0, 0x20])  # Set the header and data type
        body[6] = 0b00110001  # Power, dry, boost_mode
        body[7] = 0b01000000  # aux_heating
        body[8] = 0b10000000  # sleep_mode
        body[11] = 2  # Mode index for BB_AC_MODES
        body[12] = 0x3C  # Target temperature: ((60 - 30) / 2) = 15.0
        body[13] = 127  # Fan speed
        body[31] = 0b01000100  # Timer, eco_mode

        response = MessageACResponse(self.header + body)
        assert hasattr(response, "power")
        assert hasattr(response, "dry")
        assert hasattr(response, "boost_mode")
        assert hasattr(response, "aux_heating")
        assert hasattr(response, "sleep_mode")
        assert hasattr(response, "mode")
        assert response.mode == 1
        assert hasattr(response, "target_temperature")
        assert response.target_temperature == 15.0
        assert hasattr(response, "fan_speed")
        assert response.fan_speed == 127
        assert hasattr(response, "timer")
        assert hasattr(response, "eco_mode")

        body[11] = 10  # Invalid mode index for BB_AC_MODES
        response = MessageACResponse(self.header + body)
        assert hasattr(response, "mode")
        assert response.mode == 0

    def test_message_query_bb_0x10(self) -> None:
        """Test Message parse query BB 0x20."""
        self.header[9] = 0x03
        body = bytearray(100)
        body[:6] = bytearray([0xBB, 0, 0, 0, 0, 0x10])  # Set the header and data type
        body[14] = 0x88  # Indoor temperature byte 2
        body[13] = 0x77  # Indoor temperature byte 1
        body[36] = 60  # Indoor humidity
        body[86] = 0x31  # sn8_flag

        response = MessageACResponse(self.header + body)
        assert hasattr(response, "indoor_temperature")
        assert response.indoor_temperature == 349.35
        assert hasattr(response, "indoor_humidity")
        assert response.indoor_humidity == 60
        assert hasattr(response, "sn8_flag")

        body[14] = 0x78  # Indoor temperature byte 2
        response = MessageACResponse(self.header + body)
        assert hasattr(response, "indoor_temperature")
        assert response.indoor_temperature == 308.39

    def test_message_query_bb_0x30(self) -> None:
        """Test Message parse query BB 0x30."""
        self.header[9] = 0x03
        body = bytearray(100)
        body[:6] = bytearray([0xBB, 0, 0, 0, 0, 0x30])  # Set the header and data type
        body[11] = 0x22  # Outdoor temperature byte 1
        body[12] = 0x80  # Outdoor temperature byte 2

        response = MessageACResponse(self.header + body)
        assert hasattr(response, "outdoor_temperature")
        assert response.outdoor_temperature == 328.02

        body[12] = 0x65  # Outdoor temperature byte 2

        response = MessageACResponse(self.header + body)
        assert hasattr(response, "outdoor_temperature")
        assert response.outdoor_temperature == 258.9

    def test_message_query_bb_unimplemented(self) -> None:
        """Test Message parse query BB unimplemented."""
        self.header[9] = 0x03
        body = bytearray(100)
        body[:6] = bytearray([0xBB, 0, 0, 0, 0, 0x12])  # Set the header and data type
        response = MessageACResponse(self.header + body)
        assert not hasattr(response, "power")

        body[5] = 0x13
        response = MessageACResponse(self.header + body)
        assert not hasattr(response, "power")
