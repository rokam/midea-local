"""Midea local ED message."""

from enum import IntEnum

from midealocal.const import DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)


class Attributes(IntEnum):
    """Attributes."""

    CHILD_LOCK = 0x000
    LIFE = 0x10
    TDS = 0x013
    WATER_CONSUMPTION = 0x011


class NewSetTags(IntEnum):
    """New set tags."""

    power = 0x0100
    lock = 0x0201


class EDNewSetParamPack:
    """ED new set parameter pack."""

    @staticmethod
    def pack(param: int, value: int, addition: int = 0) -> bytearray:
        """Pack parameter."""
        return bytearray(
            [param & 0xFF, param >> 8, value, addition & 0xFF, addition >> 8],
        )


class MessageEDBase(MessageRequest):
    """ED message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes = ListTypes.X00,
    ) -> None:
        """Initialize ED message base."""
        super().__init__(
            device_type=DeviceType.ED,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageEDBase):
    """ED message query."""

    def __init__(self, protocol_version: int, body_type: ListTypes) -> None:
        """Initialize ED message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x01])


class MessageNewSet(MessageEDBase):
    """ED message new set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize ED message new set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X15,
        )
        self.power: bool | None = None
        self.lock: bool | None = None

    @property
    def _body(self) -> bytearray:
        pack_count = 0
        payload = bytearray([0x01, 0x00])
        if self.power is not None:
            pack_count += 1
            payload.extend(
                EDNewSetParamPack.pack(
                    param=NewSetTags.power,  # power
                    value=0x01 if self.power else 0x00,
                ),
            )
        if self.lock is not None:
            pack_count += 1
            payload.extend(
                EDNewSetParamPack.pack(
                    param=NewSetTags.lock,  # lock
                    value=0x01 if self.lock else 0x00,
                ),
            )
        payload[1] = pack_count
        return payload


class MessageOldSet(MessageEDBase):
    """ED message old set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize ED message old set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
        )

    @property
    def body(self) -> bytearray:
        """ED message old set body."""
        return bytearray([])

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class EDMessageBody01(MessageBody):
    """ED message body 01."""

    def __init__(self, body: bytearray) -> None:
        """Initialize ED message body 01."""
        super().__init__(body)
        self.power = (body[2] & 0x01) > 0
        self.water_consumption = body[7] + (body[8] << 8)
        self.in_tds = body[36] + (body[37] << 8)
        self.out_tds = body[38] + (body[39] << 8)
        self.child_lock = body[15] > 0
        self.filter1 = round((body[25] + (body[26] << 8)) / 24)
        self.filter2 = round((body[27] + (body[28] << 8)) / 24)
        self.filter3 = round((body[29] + (body[30] << 8)) / 24)
        self.life1 = body[16]
        self.life2 = body[17]
        self.life3 = body[18]


class EDMessageBody03(MessageBody):
    """ED message body 03."""

    def __init__(self, body: bytearray) -> None:
        """Initialize ED message body 03."""
        super().__init__(body)
        self.power = (body[51] & 0x01) > 0
        self.child_lock = (body[51] & 0x08) > 0
        self.water_consumption = body[20] + (body[21] << 8)
        self.life1 = body[22]
        self.life2 = body[23]
        self.life3 = body[24]
        self.in_tds = body[27] + (body[28] << 8)
        self.out_tds = body[29] + (body[30] << 8)


class EDMessageBody05(MessageBody):
    """ED message body 05."""

    def __init__(self, body: bytearray) -> None:
        """Initialize ED message body 05."""
        super().__init__(body)
        self.power = (body[51] & 0x01) > 0
        self.child_lock = (body[51] & 0x08) > 0
        self.water_consumption = body[20] + (body[21] << 8)


class EDMessageBody06(MessageBody):
    """ED message body 06."""

    def __init__(self, body: bytearray) -> None:
        """Initialize ED message body 06."""
        super().__init__(body)
        self.power = (body[51] & 0x01) > 0
        self.child_lock = (body[51] & 0x08) > 0
        self.water_consumption = body[25] + (body[26] << 8)


class EDMessageBody07(MessageBody):
    """ED message body 07."""

    def __init__(self, body: bytearray) -> None:
        """Initialize ED message body 07."""
        super().__init__(body)
        self.water_consumption = (body[21] << 8) + body[20]
        self.power = (body[51] & 0x01) > 0
        self.child_lock = (body[51] & 0x08) > 0


class EDMessageBodyFF(MessageBody):
    """ED message body FF."""

    def __init__(self, body: bytearray) -> None:
        """Initialize ED message body FF."""
        super().__init__(body)
        data_offset = 2
        while True:
            length = (body[data_offset + 2] >> 4) + 2
            attr = ((body[data_offset + 2] % 16) << 8) + body[data_offset + 1]
            if attr == Attributes.CHILD_LOCK:
                self.child_lock = (body[data_offset + 5] & 0x01) > 0
                self.power = (body[data_offset + 6] & 0x01) > 0
            elif attr == Attributes.WATER_CONSUMPTION:
                self.water_consumption = (
                    float(
                        body[data_offset + 3]
                        + (body[data_offset + 4] << 8)
                        + (body[data_offset + 5] << 16)
                        + (body[data_offset + 6] << 24),
                    )
                    / 1000
                )
            elif attr == Attributes.TDS:
                self.in_tds = body[data_offset + 3] + (body[data_offset + 4] << 8)
                self.out_tds = body[data_offset + 5] + (body[data_offset + 6] << 8)
            elif attr == Attributes.LIFE:
                self.life1 = body[data_offset + 3]
                self.life2 = body[data_offset + 4]
                self.life3 = body[data_offset + 5]
            # fix index out of range error
            if data_offset + length + 6 > len(body):
                break
            data_offset += length


class MessageEDResponse(MessageResponse):
    """ED message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize ED message response."""
        super().__init__(bytearray(message))
        if self._message_type in [
            MessageType.set,
            MessageType.query,
            MessageType.notify1,
        ]:
            self.device_class = self._body_type
            if self._body_type in [ListTypes.X00, ListTypes.X15, ListTypes.FF]:
                self.set_body(EDMessageBodyFF(super().body))
            if self.body_type == ListTypes.X01:
                self.set_body(EDMessageBody01(super().body))
            elif self.body_type in [ListTypes.X03, ListTypes.X04]:
                self.set_body(EDMessageBody03(super().body))
            elif self.body_type == ListTypes.X05:
                self.set_body(EDMessageBody05(super().body))
            elif self.body_type == ListTypes.X06:
                self.set_body(EDMessageBody06(super().body))
            elif self.body_type == ListTypes.X07:
                self.set_body(EDMessageBody07(super().body))
        self.set_attr()
