"""B0 Midea local message."""

from midealocal.const import MAX_BYTE_VALUE, DeviceType, ProtocolVersion
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)

MIN_MSG_BODY = 15


class MessageB0Base(MessageRequest):
    """B0 message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize B0 message base."""
        super().__init__(
            device_type=DeviceType.B0,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery00(MessageB0Base):
    """B0 message query 00."""

    def __init__(self, protocol_version: ProtocolVersion) -> None:
        """Initialize B0 message query 00."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X00,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class MessageQuery01(MessageB0Base):
    """B0 message query 01."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize B0 message query 01."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X01,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class B0MessageBody(MessageBody):
    """B0 message body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize B0 message body."""
        super().__init__(body)
        if len(body) > MIN_MSG_BODY:
            self.door = (body[0] & 0x80) > 0
            self.status = body[0] & 0x7F
            self.time_remaining = body[2] * 60 + body[3]
            self.error_code = body[5]


class B0Message01Body(MessageBody):
    """B0 message 01 body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize B0 message 01 body."""
        super().__init__(body)
        if len(body) > MIN_MSG_BODY:
            self.door = (body[32] & 0x02) > 0
            self.status = body[31]
            self.time_remaining = (
                (0 if body[22] == MAX_BYTE_VALUE else body[22]) * 3600
                + (0 if body[23] == MAX_BYTE_VALUE else body[23]) * 60
                + (0 if body[24] == MAX_BYTE_VALUE else body[24])
            )
            self.current_temperature = (body[25] << 8) + (body[26])
            if self.current_temperature == 0:
                self.current_temperature = (body[27] << 8) + body[28]
            self.tank_ejected = (body[32] & 0x04) > 0
            self.water_shortage = (body[32] & 0x08) > 0
            self.water_change_reminder = (body[32] & 0x10) > 0


class MessageB0Response(MessageResponse):
    """B0 message response."""

    def __init__(self, message: bytearray) -> None:
        """Initialize B0 message response."""
        super().__init__(message)
        if self.message_type in [MessageType.notify1, MessageType.query]:
            if self.body_type == ListTypes.X01:
                self.set_body(B0Message01Body(super().body))
            elif self.body_type == ListTypes.X04:
                pass
            else:
                self.set_body(B0MessageBody(super().body))
        self.set_attr()
