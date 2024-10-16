"""Test DA message."""

import pytest

from midealocal.const import ProtocolVersion
from midealocal.devices.da.message import (
    MessageDABase,
    MessageDAResponse,
    MessagePower,
    MessageQuery,
    MessageStart,
)
from midealocal.message import ListTypes, MessageType


class TestMessageDABase:
    """Test DA Message Base."""

    def test_body_not_implemented(self) -> None:
        """Test body not implemented."""
        msg = MessageDABase(
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
        expected_body = bytearray([0x03])
        assert query.body == expected_body


class TestMessagePower:
    """Test Message Power."""

    def test_power_body(self) -> None:
        """Test power body."""
        power = MessagePower(protocol_version=ProtocolVersion.V1)
        expected_body = bytearray([0x02, 0x00, 0xFF])
        assert power.body == expected_body
        power.power = True
        expected_body = bytearray([0x02, 0x01, 0xFF])
        assert power.body == expected_body


class TestMessageStart:
    """Test Message Start."""

    def test_start_body(self) -> None:
        """Test start body."""
        start = MessageStart(protocol_version=ProtocolVersion.V1)
        expected_body = bytearray([0x02, 0xFF, 0x00])
        assert start.body == expected_body
        start.start = True
        expected_body = bytearray([0x02, 0xFF, 0x01])
        assert start.body == expected_body
        start.washing_data = bytearray([0x01, 0x02, 0x03])
        assert start.body == expected_body + start.washing_data


class TestMessageDAResponse:
    """Test Message DA Response."""

    def test_da_general_response(self) -> None:
        """Test general response."""
        header = bytearray(
            [
                0xAA,
                0x00,
                0xDA,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x01,
                0x03,
            ],
        )
        body = bytearray(26)
        body[0] = 0x04  # Body Type
        body[1] = 1  # Set power to True
        body[2] = 2  # Set start condition to True
        body[24] = 10  # Mock error_code
        body[4] = 5  # Mock program
        body[9] = 30  # Mock wash_time
        body[12] = 10  # Mock soak_time
        body[10] = (2 << 4) | 3  # Mock dehydration_time and rinse_count
        body[6] = (3 << 4) | 2  # Mock dehydration_speed and wash_strength
        body[5] = (4 << 4) | 1  # Mock rinse_level and wash_level
        body[8] = (5 << 4) | 4  # Mock softener and detergent
        body[16] = 2 << 1  # Mock progress
        body[17] = 15  # Mock time_remaining lower byte
        body[18] = 1  # Mock time_remaining upper byte
        response = MessageDAResponse(header + body)
        assert hasattr(response, "power")
        assert response.power
        assert hasattr(response, "start")
        assert response.start
        assert hasattr(response, "error_code")
        assert response.error_code == 10
        assert hasattr(response, "program")
        assert response.program == 5
        assert hasattr(response, "wash_time")
        assert response.wash_time == 30
        assert hasattr(response, "soak_time")
        assert response.soak_time == 10
        assert hasattr(response, "dehydration_time")
        assert response.dehydration_time == 2
        assert hasattr(response, "dehydration_speed")
        assert response.dehydration_speed == 3
        assert hasattr(response, "rinse_count")
        assert response.rinse_count == 3
        assert hasattr(response, "rinse_level")
        assert response.rinse_level == 4
        assert hasattr(response, "wash_level")
        assert response.wash_level == 1
        assert hasattr(response, "wash_strength")
        assert response.wash_strength == 2
        assert hasattr(response, "softener")
        assert response.softener == 5
        assert hasattr(response, "detergent")
        assert response.detergent == 4
        assert hasattr(response, "progress")
        assert response.progress == 2
        assert hasattr(response, "time_remaining")
        assert response.time_remaining == 15 + 60
