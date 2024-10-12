"""Midea local E1 message."""

from midealocal.const import DeviceType
from midealocal.message import (
    BodyType,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)

BRIGTH_BYTE = 24
STORAGE_REMAINING_BYTE = 18
HUMIDITY_BYTE = 33


class MessageE1Base(MessageRequest):
    """E1 message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: BodyType,
    ) -> None:
        """Initialize E1 message base."""
        super().__init__(
            device_type=DeviceType.E1,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessagePower(MessageE1Base):
    """E1 message power."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize E1 message power."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=BodyType.X08,
        )
        self.power = False

    @property
    def _body(self) -> bytearray:
        power = 0x01 if self.power else 0x00
        return bytearray([power, 0x00, 0x00, 0x00])


class MessageWork(MessageE1Base):
    """E1 message work."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize E1 message work."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=BodyType.X08,
        )
        self.work_status = 0x3
        self.mode = 0

    @property
    def _body(self) -> bytearray:
        return bytearray([self.work_status, self.mode, 0x00, 0x00])


class MessageLock(MessageE1Base):
    """E1 message lock."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize E1 message lock."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=BodyType.X83,
        )
        self.lock = False

    @property
    def _body(self) -> bytearray:
        lock = 0x03 if self.lock else 0x04
        return bytearray([lock]) + bytearray([0x00] * 36)


class MessageStorage(MessageE1Base):
    """E1 message storage."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize E1 message storage."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=BodyType.X81,
        )
        self.storage = False

    @property
    def _body(self) -> bytearray:
        storage = 0x01 if self.storage else 0x00
        return (
            bytearray([0x00, 0x00, 0x00, storage])
            + bytearray([0xFF] * 6)
            + bytearray([0x00] * 27)
        )


class MessageQuery(MessageE1Base):
    """E1 message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize E1 message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=BodyType.X00,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class E1GeneralMessageBody(MessageBody):
    """E1 message general body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize E1 message general body."""
        super().__init__(body)
        self.power = body[1] > 0
        self.status = body[1]
        self.mode = body[2]
        self.additional = body[3]
        self.door = (body[5] & 0x01) == 0  # 0 - open, 1 - close
        self.rinse_aid = (body[5] & 0x02) > 0  # 0 - enough, 1 - shortage
        self.salt = (body[5] & 0x04) > 0  # 0 - enough, 1 - shortage
        start_pause = (body[5] & 0x08) > 0
        if start_pause:
            self.start = True
        elif self.status in [2, 3]:
            self.start = False
        self.child_lock = (body[5] & 0x10) > 0
        self.uv = (body[4] & 0x2) > 0
        self.dry = (body[4] & 0x10) > 0
        self.dry_status = (body[4] & 0x20) > 0
        self.storage = (body[5] & 0x20) > 0
        self.storage_status = (body[5] & 0x40) > 0
        self.time_remaining = body[6]
        self.progress = body[9]
        self.storage_remaining = (
            body[18] if len(body) > STORAGE_REMAINING_BYTE else False
        )
        self.temperature = body[11]
        self.humidity = body[33] if len(body) > HUMIDITY_BYTE else None
        self.waterswitch = (body[4] & 0x4) > 0
        self.water_lack = (body[5] & 0x80) > 0
        self.error_code = body[10]
        self.softwater = body[13]
        self.wrong_operation = body[16]
        self.bright = body[24] if len(body) > BRIGTH_BYTE else None


class MessageE1Response(MessageResponse):
    """E1 message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize E1 message response."""
        super().__init__(bytearray(message))
        if (
            self.message_type == MessageType.set and 0 <= self.body_type <= BodyType.X07
        ) or (
            self.message_type in [MessageType.query, MessageType.notify1]
            and self.body_type == 0
        ):
            self.set_body(E1GeneralMessageBody(super().body))
        self.set_attr()
