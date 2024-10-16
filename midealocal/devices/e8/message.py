"""Midea local E8 message."""

from enum import IntEnum

from midealocal.const import DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)

MIN_RESPONSE_BODY_LENGTH = 6


class SubCommand(IntEnum):
    """Sub Command."""

    X02 = 0x02
    X04 = 0x04
    X06 = 0x06


class MessageE8Base(MessageRequest):
    """E8 message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize E8 message base."""
        super().__init__(
            device_type=DeviceType.E8,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageE8Base):
    """E8 message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize E8 message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.AA,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x55, 0x00, 0x01, 0x00, 0x00])


class E8MessageBody(MessageBody):
    """E8 message body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize E8 message body."""
        super().__init__(body)
        self.status = body[11]
        self.time_remaining = body[16] * 3600 + body[17] * 60 + body[18]
        self.keep_warm_remaining = body[19] * 3600 + body[20] * 60 + body[21]
        self.working_time = body[28] * 3600 + body[29] * 60 + body[30]
        self.target_temperature = body[39]
        self.current_temperature = body[39]
        self.finished = (body[41] & 0x01) > 0
        self.water_shortage = body[43] > 0


class MessageE8Response(MessageResponse):
    """E8 message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize E8 message response."""
        super().__init__(bytearray(message))
        if len(super().body) > MIN_RESPONSE_BODY_LENGTH:
            sub_cmd = super().body[6]
            if (
                (
                    self.message_type == MessageType.set
                    and sub_cmd in [SubCommand.X02, SubCommand.X04, SubCommand.X06]
                )
                or self.message_type in [MessageType.query, MessageType.notify1]
                and sub_cmd == SubCommand.X02
            ):
                self.set_body(E8MessageBody(super().body))
        self.set_attr()
