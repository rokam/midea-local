"""Midea local EC message."""

from midealocal.const import DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)


class MessageECBase(MessageRequest):
    """EC message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes = ListTypes.X00,
    ) -> None:
        """Initialize EC message base."""
        super().__init__(
            device_type=DeviceType.EC,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageECBase):
    """EC message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize EC message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
        )

    @property
    def body(self) -> bytearray:
        """EC message query body."""
        return bytearray([0xAA, 0x55, 0x01, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class ECGeneralMessageBody(MessageBody):
    """EC message general body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize EC message general body."""
        super().__init__(body)
        self.mode = body[4] + (body[5] << 8)
        self.progress = body[8]
        self.cooking = self.progress == 1
        self.time_remaining = body[12] * 60 + body[13]
        self.keep_warm_time = body[16] * 60 + body[17]
        self.top_temperature = body[21]
        self.bottom_temperature = body[22]
        self.with_pressure = (body[23] & 0x04) > 0


class ECBodyNew(MessageBody):
    """EC message new body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize EC message new body."""
        super().__init__(body)
        self.progress = body[11]
        self.cooking = self.progress == 1
        self.time_remaining = body[16] * 60 + body[17]
        self.keep_warm_time = body[19] * 60 + body[20]
        self.top_temperature = body[48]
        self.bottom_temperature = body[49]
        self.with_pressure = body[33] > 0


class MessageECResponse(MessageResponse):
    """EC message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize EC message response."""
        super().__init__(bytearray(message))
        if (
            self.message_type == MessageType.notify1
            and super().body[3] == ListTypes.X01
        ):
            self.set_body(ECBodyNew(super().body))
        elif (
            (self.message_type == MessageType.set and super().body[3] == ListTypes.X02)
            or (
                self.message_type == MessageType.query
                and super().body[3] == ListTypes.X03
            )
            or (
                self.message_type == MessageType.notify1
                and super().body[3] == ListTypes.X04
            )
            or (
                self.message_type == MessageType.notify1
                and super().body[3] == ListTypes.X3D
            )
        ):
            self.set_body(ECGeneralMessageBody(super().body))
        elif (
            self.message_type == MessageType.notify1
            and super().body[3] == ListTypes.X06
        ):
            self.mode = super().body[4] + (super().body[5] << 8)
        self.set_attr()
