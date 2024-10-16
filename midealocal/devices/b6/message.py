"""Midea local B6 message."""

from midealocal.const import MAX_BYTE_VALUE, DeviceType, ProtocolVersion
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)

FAN_LEVEL_RANGE_1 = 130
FAN_LEVEL_RANGE_2 = 140
FAN_LEVEL_RANGE_3 = 170
MIN_FAN_LEVEL_RANGE = 100

MESSAGE_PROTOCOL_VERSION = 2


class MessageB6Base(MessageRequest):
    """B6 message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize B6 message base."""
        super().__init__(
            device_type=DeviceType.B6,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageB6Base):
    """B6 message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize B6 message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X11
            if protocol_version == MESSAGE_PROTOCOL_VERSION
            else ListTypes.X31,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class MessageQueryTips(MessageB6Base):
    """B6 message query tips."""

    def __init__(self, protocol_version: ProtocolVersion) -> None:
        """Initialize B6 message query tips."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X02,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x01])


class MessageSet(MessageB6Base):
    """B6 message set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize B6 message set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X22
            if protocol_version in [0x00, 0x01]
            else ListTypes.X11,
        )
        self.light: int | None = None
        self.power: bool | None = None
        self.fan_level: int | None = None

    @property
    def _body(self) -> bytearray:
        if self.protocol_version in [0x00, 0x01]:
            light = 0xFF
            value2 = 0xFF
            value3 = 0xFF
            if self.light is not None:
                light = 0x1A if self.light else 0
            elif self.power is not None:
                if self.power:
                    value2 = 0x02
                    value3 = self.fan_level if self.fan_level is not None else 0x01
                else:
                    value2 = 0x03
            elif self.fan_level is not None:
                if self.fan_level == 0:
                    value2 = 0x03
                else:
                    value2 = 0x02
                    value3 = self.fan_level
            return bytearray(
                [0x01, light, value2, value3, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],
            )
        value13 = 0xFF
        value14 = 0xFF
        value15 = 0xFF
        value16 = 0xFF
        if self.power is not None:
            value13 = 0x01
            if self.power:
                value15 = 0x02
                value16 = self.fan_level if self.fan_level is not None else 0x01
            else:
                value15 = 0x01
        elif self.fan_level is not None:
            value13 = 0x01
            if self.fan_level == 0:
                value15 = 0x01
            else:
                value15 = 0x02
                value16 = self.fan_level
        elif self.light is not None:
            value13 = 0x02
            value14 = 0x02
            value15 = 0x01 if self.light else 0x00
        return bytearray([0x01, value13, value14, value15, value16, 0xFF, 0xFF])


class B6FeedbackBody(MessageBody):
    """B6 message feedback body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize B6 message feedback body."""
        super().__init__(body)


class B6GeneralBody(MessageBody):
    """B6 message general body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize B6 message general body."""
        super().__init__(body)
        if body[1] != MAX_BYTE_VALUE:
            self.light = body[1] > 0x00
        self.power = False
        fan_level: int = 0
        if body[2] != MAX_BYTE_VALUE:
            self.power = body[2] in [0x02, 0x06, 0x07, 0x14, 0x15, 0x16]
            if body[2] in [0x14, 0x16]:
                fan_level = 0x16
        if fan_level == 0 and body[3] != MAX_BYTE_VALUE:
            fan_level = body[3]
        if fan_level > MIN_FAN_LEVEL_RANGE:
            if fan_level < FAN_LEVEL_RANGE_1:
                fan_level = 1
            elif fan_level < FAN_LEVEL_RANGE_2:
                fan_level = 2
            elif fan_level < FAN_LEVEL_RANGE_3:
                fan_level = 3
            else:
                fan_level = 4
        self.fan_level = fan_level
        self.oilcup_full = (body[5] & 0x01) > 0
        self.cleaning_reminder = (body[5] & 0x02) > 0


class B6NewProtocolBody(MessageBody):
    """B6 message new protocol body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize B6 message new protocol body."""
        super().__init__(body)
        if body[1] == 0x01:
            pack_bytes = body[3 : 3 + body[2]]
            if pack_bytes[1] != MAX_BYTE_VALUE:
                self.power = True
                self.power = pack_bytes[1] not in [0x00, 0x01, 0x05, 0x07]
            if pack_bytes[2] != MAX_BYTE_VALUE:
                self.fan_level = pack_bytes[2]
            if pack_bytes[6] != MAX_BYTE_VALUE:
                self.light = pack_bytes[6] > 0
            self.oilcup_full = (pack_bytes[18] & 0x02) > 0
            self.cleaning_reminder = (pack_bytes[18] & 0x04) > 0


class B6SpecialBody(MessageBody):
    """B6 message special body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize B6 message special body."""
        super().__init__(body)
        if body[2] != MAX_BYTE_VALUE:
            self.light = body[2] > 0x00
        self.power = False
        if body[3] != MAX_BYTE_VALUE:
            self.power = body[3] in [0x00, 0x02, 0x04]
        if body[4] != MAX_BYTE_VALUE:
            self.fan_level = body[4]


class B6ExceptionBody(MessageBody):
    """B6 message exception body."""


class MessageB6Response(MessageResponse):
    """B6 message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize B6 message response."""
        super().__init__(bytearray(message))
        if (
            self.message_type == MessageType.set
            and self.body_type == ListTypes.X22
            and super().body[1] == ListTypes.X01
        ):
            self.set_body(B6SpecialBody(super().body))
        elif (
            self.message_type == MessageType.set
            and self.body_type == ListTypes.X11
            and super().body[1] == ListTypes.X01
        ):
            #############################
            pass
        elif self.message_type == MessageType.query:
            if self.body_type in [ListTypes.X11, ListTypes.X31]:
                if self.protocol_version in [0, 1]:
                    self.set_body(B6GeneralBody(super().body))
                else:
                    self.set_body(B6NewProtocolBody(super().body))
            elif self.body_type == ListTypes.X32 and super().body[1] == 0x01:
                self.set_body(B6ExceptionBody(super().body))
        elif self.message_type == MessageType.notify1:
            if self.body_type in [ListTypes.X11, ListTypes.X41]:
                if self.protocol_version in [0, 1]:
                    self.set_body(B6GeneralBody(super().body))
                else:
                    self.set_body(B6NewProtocolBody(super().body))
            elif self.body_type == ListTypes.X0A:
                if super().body[1] == ListTypes.A1:
                    self.set_body(B6ExceptionBody(super().body))
                elif super().body[1] == ListTypes.A2:
                    self.oilcup_full = (super().body[2] & 0x01) > 0
                    self.cleaning_reminder = (super().body[2] & 0x02) > 0
        elif (
            self.message_type == MessageType.exception2
            and self.body_type == ListTypes.A1
        ):
            pass

        self.set_attr()
