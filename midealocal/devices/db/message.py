"""Midea local DB message."""

from midealocal.const import DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)


class MessageDBBase(MessageRequest):
    """DB message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize DB message base."""
        super().__init__(
            device_type=DeviceType.DB,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageDBBase):
    """DB message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize DB message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X03,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class MessagePower(MessageDBBase):
    """DB message power."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize DB message power."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X02,
        )
        self.power = False

    @property
    def _body(self) -> bytearray:
        power = 0x01 if self.power else 0x00
        return bytearray(
            [
                power,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
                0xFF,
            ],
        )


class MessageStart(MessageDBBase):
    """DB message start."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize DB message start."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X02,
        )
        self.start = False
        self.washing_data = bytearray([])

    @property
    def _body(self) -> bytearray:
        if self.start:  # Pause
            return bytearray([0xFF, 0x01]) + self.washing_data
        # Pause
        return bytearray([0xFF, 0x00])


class DBGeneralMessageBody(MessageBody):
    """DB message general body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize DB message general body."""
        super().__init__(body)
        self.power = body[1] > 0
        self.start = body[2] in [2, 6]
        self.washing_data = body[3:16]
        self.progress = 0
        self.time_remaining: float | None = None
        for i in range(7):
            if (body[16] & (1 << i)) > 0:
                self.progress = i + 1
                break
        if self.power:
            self.time_remaining = body[17] + (body[18] << 8)


class MessageDBResponse(MessageResponse):
    """DB message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize DB message response."""
        super().__init__(bytearray(message))
        if self.message_type in [MessageType.query, MessageType.set] or (
            self.message_type == MessageType.notify1 and self.body_type == ListTypes.X04
        ):
            self.set_body(DBGeneralMessageBody(super().body))
        self.set_attr()
