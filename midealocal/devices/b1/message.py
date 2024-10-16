"""Midea local B1 message."""

from midealocal.const import MAX_BYTE_VALUE, DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)


class MessageB1Base(MessageRequest):
    """B1 message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize B1 message base."""
        super().__init__(
            device_type=DeviceType.B1,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageB1Base):
    """B1 message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize B1 message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X00,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class B1MessageBody(MessageBody):
    """B1 message body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize B1 message body."""
        super().__init__(body)
        self.door = (body[16] & 0x02) > 0
        self.status = body[1]
        self.time_remaining = (
            (0 if body[6] == MAX_BYTE_VALUE else body[6]) * 3600
            + (0 if body[7] == MAX_BYTE_VALUE else body[7]) * 60
            + (0 if body[8] == MAX_BYTE_VALUE else body[8])
        )
        self.current_temperature = body[19]
        self.tank_ejected = (body[16] & 0x04) > 0
        self.water_shortage = (body[16] & 0x08) > 0
        self.water_change_reminder = (body[16] & 0x10) > 0


class MessageB1Response(MessageResponse):
    """B1 message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize B1 message response."""
        super().__init__(bytearray(message))
        if self.message_type in [MessageType.notify1, MessageType.query]:
            self.set_body(B1MessageBody(super().body))
        self.set_attr()
