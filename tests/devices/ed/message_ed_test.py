"""Test ED message."""

import pytest

from midealocal.const import ProtocolVersion
from midealocal.devices.ed.message import (
    EDMessageBody01,
    EDMessageBody03,
    EDMessageBody05,
    EDMessageBody06,
    EDMessageBody07,
    EDMessageBodyFF,
    MessageEDBase,
    MessageEDResponse,
    MessageNewSet,
    MessageQuery,
)
from midealocal.message import ListTypes, MessageType


class TestMessageEDBase:
    """Test ED Message Base."""

    def test_body_not_implemented(self) -> None:
        """Test body not implemented."""
        msg = MessageEDBase(
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
        query = MessageQuery(
            protocol_version=ProtocolVersion.V1,
            body_type=ListTypes.X02,
        )
        expected_body = bytearray([0x02, 0x01])
        assert query.body == expected_body


class TestMessageNewSet:
    """Test MessageNewSet."""

    def test_message_newset(self) -> None:
        """Test MessageNewSet."""
        new_set = MessageNewSet(protocol_version=ProtocolVersion.V1)
        expected_body = bytearray([0x15, 0x01, 0x00])
        assert new_set.body == expected_body
        new_set.power = True
        expected_body = bytearray([0x15, 0x01, 0x01, 0x00, 0x01, 0x01, 0x00, 0x00])
        assert new_set.body == expected_body
        new_set.lock = True
        expected_body = bytearray(
            [
                0x15,
                0x01,
                0x02,
                0x00,
                0x01,
                0x01,
                0x00,
                0x00,
                0x01,
                0x02,
                0x01,
                0x00,
                0x00,
            ],
        )
        assert new_set.body == expected_body
        new_set.power = None
        expected_body = bytearray([0x15, 0x01, 0x01, 0x01, 0x02, 0x01, 0x00, 0x00])
        assert new_set.body == expected_body


class TestEDMessageBody01:
    """Test EDMessageBody01."""

    def test_ed_message01(self) -> None:
        """Test EDMessageBody01."""
        body = bytearray(40)
        body[0] = 0x01  # Body Type
        body[2] = 1  # Set power to True
        body[7] = 2  # Set water_consumption bit1
        body[8] = 3  # Set water_consumption bit2
        body[36] = 4  # Set in_tds bit1
        body[37] = 5  # Set in_tds bit2
        body[38] = 6  # Set out_tds bit1
        body[39] = 7  # Set out_tds bit2
        body[15] = 7  # Set child_lock
        body[25] = 4  # Set filter1 bit1
        body[26] = 5  # Set filter1 bit2
        body[27] = 5  # Set filter2 bit1
        body[28] = 6  # Set filter2 bit2
        body[29] = 6  # Set filter3 bit1
        body[30] = 7  # Set filter3 bit2
        body[16] = 2  # Set life1
        body[17] = 3  # Set life2
        body[18] = 4  # Set life3
        message = EDMessageBody01(body=body)
        assert hasattr(message, "body_type")
        assert message.body_type == 1
        assert hasattr(message, "power")
        assert message.power
        assert hasattr(message, "water_consumption")
        assert message.water_consumption == 770
        assert hasattr(message, "in_tds")
        assert message.in_tds == 1284
        assert hasattr(message, "out_tds")
        assert message.out_tds == 1798
        assert hasattr(message, "child_lock")
        assert message.child_lock
        assert hasattr(message, "filter1")
        assert message.filter1 == 54
        assert hasattr(message, "filter2")
        assert message.filter2 == 64
        assert hasattr(message, "filter3")
        assert message.filter3 == 75
        assert hasattr(message, "life1")
        assert message.life1 == 2
        assert hasattr(message, "life2")
        assert message.life2 == 3
        assert hasattr(message, "life3")
        assert message.life3 == 4


class TestEDMessageBody03:
    """Test EDMessageBody03."""

    def test_ed_message03(self) -> None:
        """Test EDMessageBody03."""
        body = bytearray(52)
        body[0] = 0x03  # Body Type
        body[51] = 1  # Set power to True
        body[20] = 2  # Set water_consumption bit1
        body[21] = 3  # Set water_consumption bit2
        body[27] = 4  # Set in_tds bit1
        body[28] = 5  # Set in_tds bit2
        body[29] = 6  # Set out_tds bit1
        body[30] = 7  # Set out_tds bit2
        body[22] = 2  # Set life1
        body[23] = 3  # Set life2
        body[24] = 4  # Set life3
        message = EDMessageBody03(body=body)
        assert hasattr(message, "body_type")
        assert message.body_type == 3
        assert hasattr(message, "power")
        assert message.power
        assert hasattr(message, "water_consumption")
        assert message.water_consumption == 770
        assert hasattr(message, "in_tds")
        assert message.in_tds == 1284
        assert hasattr(message, "out_tds")
        assert message.out_tds == 1798
        assert hasattr(message, "child_lock")
        assert not message.child_lock
        assert hasattr(message, "life1")
        assert message.life1 == 2
        assert hasattr(message, "life2")
        assert message.life2 == 3
        assert hasattr(message, "life3")
        assert message.life3 == 4


class TestEDMessageBody05:
    """Test EDMessageBody05."""

    def test_ed_message05(self) -> None:
        """Test EDMessageBody05."""
        body = bytearray(52)
        body[0] = 0x05  # Body Type
        body[51] = 1  # Set power to True
        body[20] = 2  # Set water_consumption bit1
        body[21] = 3  # Set water_consumption bit2
        message = EDMessageBody05(body=body)
        assert hasattr(message, "body_type")
        assert message.body_type == 5
        assert hasattr(message, "power")
        assert message.power
        assert hasattr(message, "water_consumption")
        assert message.water_consumption == 770
        assert hasattr(message, "child_lock")
        assert not message.child_lock


class TestEDMessageBody06:
    """Test EDMessageBody06."""

    def test_ed_message06(self) -> None:
        """Test EDMessageBody06."""
        body = bytearray(52)
        body[0] = 0x06  # Body Type
        body[51] = 1  # Set power to True
        body[25] = 2  # Set water_consumption bit1
        body[26] = 3  # Set water_consumption bit2
        message = EDMessageBody06(body=body)
        assert hasattr(message, "body_type")
        assert message.body_type == 6
        assert hasattr(message, "power")
        assert message.power
        assert hasattr(message, "water_consumption")
        assert message.water_consumption == 770
        assert hasattr(message, "child_lock")
        assert not message.child_lock


class TestEDMessageBody07:
    """Test EDMessageBody07."""

    def test_ed_message07(self) -> None:
        """Test EDMessageBody07."""
        body = bytearray(52)
        body[0] = 0x07  # Body Type
        body[51] = 1  # Set power to True
        body[20] = 2  # Set water_consumption bit1
        body[21] = 3  # Set water_consumption bit2
        message = EDMessageBody07(body=body)
        assert hasattr(message, "body_type")
        assert message.body_type == 7
        assert hasattr(message, "power")
        assert message.power
        assert hasattr(message, "water_consumption")
        assert message.water_consumption == 770
        assert hasattr(message, "child_lock")
        assert not message.child_lock


class TestEDMessageBodyFF:
    """Test EDMessageBodyFF."""

    def test_ed_message_ff(self) -> None:
        """Test EDMessageBodyFF."""
        body = bytearray(
            [
                0xFF,  # body_type
                0x01,
                0x07,  # category
                0x00,  # part 1, offset+1,  attr bit1, test 0x00/CHILD_LOCK
                0x40,  # part 1, offset+2,  attr bit2 and length bit
                0x00,  # part 1, offset+3,
                0x00,  # part 1, offset+4,
                0x01,  # part 1, offset+5, child_lock
                0x01,  # part 1, offset+6, power
                0x10,  # part 2, offset+1,  attr bit1, test 0x10/LIFE
                0x40,  # part 2, offset+2,  attr bit2 and length bit
                0x01,  # part 2, offset+3, life1
                0x02,  # part 2, offset+4, life2
                0x03,  # part 2, offset+5, life3
                0x00,  # part 2,
                0x11,  # part 3, offset+1,  attr bit1, test 0x11/WATER_CONSUMPTION
                0x40,  # part 3, offset+2,  attr bit2 and length bit
                0x01,  # part 3, offset+3, water_consumption bit1
                0x02,  # part 3, offset+4, water_consumption bit2
                0x03,  # part 3, offset+5, water_consumption bit3
                0x04,  # part 3, offset+6, water_consumption bit4
                0x13,  # part 4, offset+1,  attr bit1, test 0x13/TDS
                0x40,  # part 4, offset+2,  attr bit2 and length bit
                0x04,  # part 4, offset+3, in_tds bit1
                0x03,  # part 4, offset+4, in_tds bit2
                0x02,  # part 4, offset+5, out_tds bit1
                0x01,  # part 4, offset+6, out_tds bit2
            ],
        )

        message = EDMessageBodyFF(body=body)
        assert hasattr(message, "body_type")
        assert message.body_type == 255
        assert hasattr(message, "power")
        assert message.power
        assert hasattr(message, "water_consumption")
        assert message.water_consumption == 67305.985
        assert hasattr(message, "in_tds")
        assert message.in_tds == 772
        assert hasattr(message, "out_tds")
        assert message.out_tds == 258
        assert hasattr(message, "child_lock")
        assert message.child_lock
        assert hasattr(message, "life1")
        assert message.life1 == 1
        assert hasattr(message, "life2")
        assert message.life2 == 2
        assert hasattr(message, "life3")
        assert message.life3 == 3


class TestMessageEDResponse:
    """Test Message ED Response."""

    def test_ed_general_response(self) -> None:
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
        body = bytearray(
            [
                0xFF,  # body_type
                0x01,
                0x07,  # category
                0x00,  # part 1, offset+1,  attr bit1, test 0x00/CHILD_LOCK
                0x40,  # part 1, offset+2,  attr bit2 and length bit
                0x00,  # part 1, offset+3,
                0x00,  # part 1, offset+4,
                0x01,  # part 1, offset+5, child_lock
                0x01,  # part 1, offset+6, power
                0x10,  # part 2, offset+1,  attr bit1, test 0x10/LIFE
                0x40,  # part 2, offset+2,  attr bit2 and length bit
                0x01,  # part 2, offset+3, life1
                0x02,  # part 2, offset+4, life2
                0x03,  # part 2, offset+5, life3
                0x00,  # part 2,
                0x11,  # part 3, offset+1,  attr bit1, test 0x11/WATER_CONSUMPTION
                0x40,  # part 3, offset+2,  attr bit2 and length bit
                0x01,  # part 3, offset+3, water_consumption bit1
                0x02,  # part 3, offset+4, water_consumption bit2
                0x03,  # part 3, offset+5, water_consumption bit3
                0x04,  # part 3, offset+6, water_consumption bit4
                0x13,  # part 4, offset+1,  attr bit1, test 0x13/TDS
                0x40,  # part 4, offset+2,  attr bit2 and length bit
                0x04,  # part 4, offset+3, in_tds bit1
                0x03,  # part 4, offset+4, in_tds bit2
                0x02,  # part 4, offset+5, out_tds bit1
                0x01,  # part 4, offset+6, out_tds bit2
                0x00,
            ],
        )
        message = MessageEDResponse(header + body)
        assert hasattr(message, "body_type")
        assert message.body_type == 255
        assert hasattr(message, "power")
        assert message.power
        assert hasattr(message, "water_consumption")
        assert message.water_consumption == 67305.985
        assert hasattr(message, "in_tds")
        assert message.in_tds == 772
        assert hasattr(message, "out_tds")
        assert message.out_tds == 258
        assert hasattr(message, "child_lock")
        assert message.child_lock
        assert hasattr(message, "life1")
        assert message.life1 == 1
        assert hasattr(message, "life2")
        assert message.life2 == 2
        assert hasattr(message, "life3")
        assert message.life3 == 3
