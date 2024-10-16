"""Midea local B4 message."""

from midealocal.const import MAX_BYTE_VALUE, DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)


class MessageB4Base(MessageRequest):
    """B4 message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize B4 message base."""
        super().__init__(
            device_type=DeviceType.B4,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageB4Base):
    """B4 message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize B4 message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X01,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class B4MessageBody(MessageBody):
    """B4 message body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize B4 message body."""
        super().__init__(body)
        self.time_remaining = (
            (0 if body[22] == MAX_BYTE_VALUE else body[22]) * 3600
            + (0 if body[23] == MAX_BYTE_VALUE else body[23]) * 60
            + (0 if body[24] == MAX_BYTE_VALUE else body[24])
        )
        self.current_temperature = (body[25] << 8) + body[26]
        if self.current_temperature == 0:
            self.current_temperature = (body[27] << 8) + body[28]
        self.status = body[31]
        self.door = (body[32] & 0x02) > 0
        self.tank_ejected = (body[16] & 0x04) > 0
        self.water_shortage = (body[16] & 0x08) > 0
        self.water_change_reminder = (body[16] & 0x10) > 0


class MessageB4Response(MessageResponse):
    """B4 message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize B4 message response."""
        super().__init__(bytearray(message))
        if (
            self.message_type
            in [
                MessageType.notify1,
                MessageType.query,
                MessageType.set,
            ]
            and self.body_type == ListTypes.X01
        ):
            self.set_body(B4MessageBody(super().body))
        self.set_attr()
