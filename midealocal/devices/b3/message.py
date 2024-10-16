"""Midea local B3 message."""

from midealocal.const import MAX_BYTE_VALUE, DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)

X21_BOTTOM_COMPARTMENT_REMAINING_BYTE = 18
X21_MIDDLE_COMPARTMENT_REMAINING_BYTE = 19
X21_TOP_COMPARTMENT_REMAINING_BYTE = 17
X31_BOTTOM_COMPARTMENT_REMAINING_BYTE = 24
X31_MIDDLE_COMPARTMENT_REMAINING_BYTE = 25
X31_TOP_COMPARTMENT_REMAINING_BYTE = 23


class MessageB3Base(MessageRequest):
    """B3 message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize B3 message base."""
        super().__init__(
            device_type=DeviceType.B3,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageB3Base):
    """B3 message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize B3 message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X31,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class B3MessageBody31(MessageBody):
    """B3 message body 31."""

    def __init__(self, body: bytearray) -> None:
        """Initialize B3 message body 31."""
        super().__init__(body)
        self.top_compartment_status = body[1]
        self.top_compartment_mode = body[2]
        self.top_compartment_temperature = body[3]
        self.top_compartment_remaining = (
            body[23] * 3600
            if len(body) > X31_TOP_COMPARTMENT_REMAINING_BYTE
            and body[23] != MAX_BYTE_VALUE
            else (
                0 + body[4] * 60
                if body[4] != MAX_BYTE_VALUE
                else 0 + body[5]
                if body[5] != MAX_BYTE_VALUE
                else 0
            )
        )
        self.bottom_compartment_status = body[6]
        self.bottom_compartment_mode = body[7]
        self.bottom_compartment_temperature = body[8]
        self.bottom_compartment_remaining = (
            body[24] * 3600
            if len(body) > X31_BOTTOM_COMPARTMENT_REMAINING_BYTE
            and body[24] != MAX_BYTE_VALUE
            else (
                0 + body[9] * 60
                if body[9] != MAX_BYTE_VALUE
                else 0 + body[10]
                if body[10] != MAX_BYTE_VALUE
                else 0
            )
        )
        self.middle_compartment_status = body[17]
        self.middle_compartment_mode = body[18]
        self.middle_compartment_temperature = body[19]
        self.middle_compartment_remaining = (
            body[25] * 3600
            if len(body) > X31_MIDDLE_COMPARTMENT_REMAINING_BYTE
            and body[25] != MAX_BYTE_VALUE
            else (
                0 + body[20] * 60
                if body[20] != MAX_BYTE_VALUE
                else 0 + body[21]
                if body[21] != MAX_BYTE_VALUE
                else 0
            )
        )
        self.lock = body[11] & 0x01 > 0
        self.bottom_compartment_door = body[11] & 0x02 > 0
        self.top_compartment_door = body[11] & 0x04 > 0
        self.middle_compartment_door = body[11] & 0x10 > 0
        self.bottom_compartment_preheating = body[16] & 0x01 > 0
        self.top_compartment_preheating = body[16] & 0x02 > 0
        self.middle_compartment_preheating = body[16] & 0x10 > 0
        self.bottom_compartment_cooling = body[16] & 0x04 > 0
        self.top_compartment_cooling = body[16] & 0x08 > 0
        self.middle_compartment_cooling = body[16] & 0x20 > 0


class B3MessageBody21(MessageBody):
    """B3 message body 21."""

    def __init__(self, body: bytearray) -> None:
        """Initialize B3 message body 21."""
        super().__init__(body)
        self.top_compartment_status = body[1]
        self.top_compartment_mode = body[2]
        self.top_compartment_temperature = body[3]
        self.top_compartment_remaining = (
            body[17] * 3600
            if len(body) > X21_TOP_COMPARTMENT_REMAINING_BYTE
            and body[17] != MAX_BYTE_VALUE
            else (
                0 + body[4] * 60
                if body[4] != MAX_BYTE_VALUE
                else 0 + body[5]
                if body[5] != MAX_BYTE_VALUE
                else 0
            )
        )
        self.bottom_compartment_status = body[6]
        self.bottom_compartment_mode = body[7]
        self.bottom_compartment_temperature = body[8]
        self.bottom_compartment_remaining = (
            body[18] * 3600
            if len(body) > X21_BOTTOM_COMPARTMENT_REMAINING_BYTE
            and body[18] != MAX_BYTE_VALUE
            else (
                0 + body[9] * 60
                if body[9] != MAX_BYTE_VALUE
                else 0 + body[10]
                if body[10] != MAX_BYTE_VALUE
                else 0
            )
        )
        self.middle_compartment_status = body[12]
        self.middle_compartment_mode = body[13]
        self.middle_compartment_temperature = body[14]
        self.middle_compartment_remaining = (
            body[19] * 3600
            if len(body) > X21_MIDDLE_COMPARTMENT_REMAINING_BYTE
            and body[19] != MAX_BYTE_VALUE
            else (
                0 + body[15] * 60
                if body[15] != MAX_BYTE_VALUE
                else 0 + body[16]
                if body[16] != MAX_BYTE_VALUE
                else 0
            )
        )
        self.lock = body[11] & 0x01 > 0


class B3MessageBody24(MessageBody):
    """B3 message body 24."""

    def __init__(self, body: bytearray) -> None:
        """Initialize B3 message body 24."""
        super().__init__(body)
        self.top_compartment_status = body[5]
        self.top_compartment_mode = body[6]
        self.top_compartment_temperature = body[7]
        self.top_compartment_remaining = (
            body[8] * 60
            if body[8] != MAX_BYTE_VALUE
            else 0 + body[9]
            if body[9] != MAX_BYTE_VALUE
            else 0
        )
        self.bottom_compartment_status = body[10]
        self.bottom_compartment_mode = body[11]
        self.bottom_compartment_temperature = body[12]
        self.bottom_compartment_remaining = (
            body[13] * 60
            if body[13] != MAX_BYTE_VALUE
            else 0 + body[14]
            if body[14] != MAX_BYTE_VALUE
            else 0
        )
        self.bottom_compartment_status = body[15]
        self.bottom_compartment_mode = body[16]
        self.bottom_compartment_temperature = body[17]
        self.bottom_compartment_remaining = (
            body[18] * 60
            if body[18] != MAX_BYTE_VALUE
            else 0 + body[19]
            if body[19] != MAX_BYTE_VALUE
            else 0
        )


class MessageB3Response(MessageResponse):
    """B3 message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize B3 message response."""
        super().__init__(bytearray(message))
        if (
            self.message_type == MessageType.query
            and self.body_type == ListTypes.X31
            or self.message_type == MessageType.notify1
            and self.body_type == ListTypes.X41
        ):
            self.set_body(B3MessageBody31(super().body))
        elif (
            self.message_type == MessageType.set
            and self.body_type == ListTypes.X21
            or self.message_type == MessageType.set
            and self.body_type == ListTypes.X24
        ):
            self.set_body(B3MessageBody21(super().body))
        self.set_attr()
