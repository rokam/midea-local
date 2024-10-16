"""Test a1 message."""

import pytest

from midealocal.const import ProtocolVersion
from midealocal.devices.a1.message import (
    MessageA1Base,
    MessageA1Response,
    MessageNewProtocolQuery,
    MessageNewProtocolSet,
    MessageQuery,
    MessageSet,
    NewProtocolTags,
)
from midealocal.message import ListTypes, MessageType


class TestMessageA1Base:
    """Test A1 Message Base."""

    def test_message_id_increment(self) -> None:
        """Test message Id Increment."""
        msg = MessageA1Base(
            protocol_version=ProtocolVersion.V1,
            message_type=MessageType.query,
            body_type=ListTypes.X01,
        )
        msg2 = MessageA1Base(
            protocol_version=ProtocolVersion.V1,
            message_type=MessageType.query,
            body_type=ListTypes.X01,
        )
        assert msg2._message_id == msg._message_id + 1
        # test reset
        for _ in range(100 - msg2._message_id):
            msg = MessageA1Base(
                protocol_version=ProtocolVersion.V1,
                message_type=MessageType.query,
                body_type=ListTypes.X01,
            )
        assert msg._message_id == 1

    def test_body_not_implemented(self) -> None:
        """Test body not implemented."""
        msg = MessageA1Base(
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
        query = MessageQuery(protocol_version=ProtocolVersion.V1)
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
        assert query.body[:-2] == expected_body


class TestMessageNewProtocolQuery:
    """Test Message New Protocol Query."""

    def test_new_protocol_query_body(self) -> None:
        """Test new protocol query body."""
        query = MessageNewProtocolQuery(protocol_version=ProtocolVersion.V1)
        expected_body = bytearray(
            [0xB1, 1, NewProtocolTags.light & 0xFF, NewProtocolTags.light >> 8],
        )
        assert query.body[:-2] == expected_body


class TestMessageSet:
    """Test Message Set."""

    def test_set_body(self) -> None:
        """Test set body."""
        msg_set = MessageSet(protocol_version=ProtocolVersion.V1)

        expected_body = bytearray([msg_set.body_type]) + bytearray(
            [
                msg_set.power | msg_set.prompt_tone | 0x02,
                msg_set.mode,
                msg_set.fan_speed,
                0x00,
                0x00,
                0x00,
                msg_set.target_humidity,
                msg_set.child_lock,
                msg_set.anion,
                msg_set.swing,
                0x00,
                0x00,
                msg_set.water_level_set,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )
        assert msg_set.body[:-2] == expected_body


class TestMessageNewProtocolSet:
    """Test Message New Protocol Set."""

    def test_new_protocol_set_body(self) -> None:
        """Test new protocol set body."""
        msg_set = MessageNewProtocolSet(protocol_version=ProtocolVersion.V1)
        msg_set.light = True
        expected_body = bytearray(b"\xb0\x01[\x00\x01\x01")
        assert msg_set.body[:-2] == expected_body


class TestMessageA1Response:
    """Test Message A1 Response."""

    def test_a1_general_response(self) -> None:
        """Test general response."""
        header = bytearray(
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
                0x03,
            ],
        )
        body = bytearray(21)
        body[1] = 0b00000001  # Power on (1)
        body[2] = 0b00000010  # Mode (2)
        body[3] = 0b00000100  # Fan speed (4)
        body[7] = 40  # Target humidity (40)
        body[8] = 0b10000000  # Child lock on (128)
        body[9] = 0b01000000  # Anion on (64)
        body[10] = 0b00111111  # Tank (63)
        body[15] = 50  # Water level set (50)
        body[16] = 45  # Current humidity (45)
        body[17] = 100  # Current temperature (75 degrees C, since (100 - 50) / 2 = 25)
        body[19] = 0b00100000  # Swing on (32)
        response = MessageA1Response(header + body)
        assert hasattr(response, "power")
        assert hasattr(response, "mode")
        assert response.mode == 2
        assert hasattr(response, "fan_speed")
        assert response.fan_speed == 1
        assert hasattr(response, "target_humidity")
        assert response.target_humidity == 40
        assert hasattr(response, "child_lock")
        assert hasattr(response, "anion")
        assert hasattr(response, "tank")
        assert response.tank == 63
        assert hasattr(response, "water_level_set")
        assert response.water_level_set == 50
        assert hasattr(response, "current_humidity")
        assert response.current_humidity == 45
        assert hasattr(response, "current_temperature")
        assert response.current_temperature == 25
        assert hasattr(response, "swing")

    def test_a1_new_protocol_message_query(self) -> None:
        """Test A1 new protocol message query."""
        header = bytearray(
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
                0x03,
            ],
        )
        body = bytearray(8)
        body[0] = 0xB0  # Body type
        body[1] = 0x01  # param count
        body[2] = 0x5B  # light param low byte
        body[3] = 0x00  # light param high byte
        body[5] = 0x01  # light value length
        body[6] = 0x01  # light value
        response = MessageA1Response(header + body)
        assert hasattr(response, "light")
        assert response.light

    def test_a1_general_notify_response(self) -> None:
        """Test general notify response."""
        header = bytearray(
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
        body = bytearray(21)
        body[0] = 0xA0  # Body type
        body[1] = 0b00000001  # Power on (1)
        body[2] = 0b00000010  # Mode (2)
        body[3] = 0b00000110  # Fan speed (6)
        body[7] = 40  # Target humidity (40)
        body[8] = 0b10000000  # Child lock on (128)
        body[9] = 0b01000000  # Anion on (64)
        body[10] = 0b00111111  # Tank (63)
        body[15] = 50  # Water level set (50)
        body[16] = 45  # Current humidity (45)
        body[17] = 100  # Current temperature (75 degrees C, since (100 - 50) / 2 = 25)
        body[19] = 0b00100000  # Swing on (32)
        response = MessageA1Response(header + body)
        assert hasattr(response, "power")
        assert hasattr(response, "mode")
        assert response.mode == 2
        assert hasattr(response, "fan_speed")
        assert response.fan_speed == 6
        assert hasattr(response, "target_humidity")
        assert response.target_humidity == 40
        assert hasattr(response, "child_lock")
        assert hasattr(response, "anion")
        assert hasattr(response, "tank")
        assert response.tank == 63
        assert hasattr(response, "water_level_set")
        assert response.water_level_set == 50
        assert hasattr(response, "current_humidity")
        assert response.current_humidity == 45
        assert hasattr(response, "current_temperature")
        assert response.current_temperature == 25
        assert hasattr(response, "swing")
