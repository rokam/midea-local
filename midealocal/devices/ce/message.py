"""Midea local CE message."""

from midealocal.const import MAX_BYTE_VALUE, DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)


class MessageCEBase(MessageRequest):
    """CE message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize CE message base."""
        super().__init__(
            device_type=DeviceType.CE,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageCEBase):
    """CE message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize CE message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X01,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class MessageSet(MessageCEBase):
    """CE message set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize CE message set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X01,
        )

        self.power = False
        self.fan_speed = 0
        self.link_to_ac = False
        self.sleep_mode = False
        self.eco_mode = False
        self.aux_heating = False
        self.powerful_purify = False
        self.scheduled = False
        self.child_lock = False

    @property
    def _body(self) -> bytearray:
        power = 0x80 if self.power else 0x00
        link_to_ac = 0x01 if self.link_to_ac else 0x00
        sleep_mode = 0x02 if self.sleep_mode else 0x00
        eco_mode = 0x04 if self.eco_mode else 0x00
        aux_heating = 0x08 if self.aux_heating else 0x00
        powerful_purify = 0x10 if self.powerful_purify else 0x00
        scheduled = 0x01 if self.scheduled else 0x00
        child_lock = 0x7F if self.child_lock else 0x00
        return bytearray(
            [
                power | 0x01,
                self.fan_speed,
                link_to_ac | sleep_mode | eco_mode | aux_heating | powerful_purify,
                scheduled,
                0x00,
                child_lock,
            ],
        )


class CEGeneralMessageBody(MessageBody):
    """CE message general body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize CE message general body."""
        super().__init__(body)
        self.power = (body[1] & 0x80) > 0
        self.child_lock = (body[1] & 0x20) > 0
        self.scheduled = (body[1] & 0x40) > 0
        self.fan_speed = body[2]
        self.pm25 = (body[3] << 8) + body[4]
        self.co2 = (body[5] << 8) + body[6]
        self.current_humidity: float | None = None
        self.current_temperature: float | None = None
        self.hcho: float | None = None
        self.aux_heating: bool | None = None

        if body[7] != MAX_BYTE_VALUE:
            self.current_humidity = (body[7] << 8) + body[8] / 10
        if body[9] != MAX_BYTE_VALUE:
            self.current_temperature = (body[9] << 8) + (body[10] - 60) / 2
        if body[11] != MAX_BYTE_VALUE:
            self.hcho = (body[11] << 8) + body[12] / 1000
        self.link_to_ac = (body[17] & 0x01) > 0
        self.sleep_mode = (body[17] & 0x02) > 0
        self.eco_mode = (body[17] & 0x04) > 0
        if (body[19] & 0x02) > 0:
            self.aux_heating = (body[17] & 0x08) > 0
        self.powerful_purify = (body[17] & 0x10) > 0
        self.filter_cleaning_reminder = (body[18] & 0x01) > 0
        self.filter_change_reminder = (body[18] & 0x02) > 0
        self.error_code = body[24]


class CENotifyMessageBody(MessageBody):
    """CE message notify body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize CE message notify body."""
        super().__init__(body)
        self.current_humidity: float | None = None
        self.current_temperature: float | None = None
        self.hcho: float | None = None

        self.pm25 = (body[1] << 8) + body[2]
        self.co2 = (body[3] << 8) + body[4]
        if body[5] != MAX_BYTE_VALUE:
            self.current_humidity = (body[5] << 8) + body[6] / 10
        if body[7] != MAX_BYTE_VALUE:
            self.current_temperature = (body[7] << 8) + (body[8] - 60) / 2
        if body[9] != MAX_BYTE_VALUE:
            self.hcho = (body[9] << 8) + body[10] / 1000
        self.error_code = body[12]


class MessageCEResponse(MessageResponse):
    """CE message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize CE message response."""
        super().__init__(bytearray(message))
        if (
            self.message_type in [MessageType.query, MessageType.set]
            and self.body_type == ListTypes.X01
        ) or (
            self.message_type == MessageType.notify1 and self.body_type == ListTypes.X02
        ):
            self.set_body(CEGeneralMessageBody(super().body))
        elif (
            self.message_type == MessageType.notify1 and self.body_type == ListTypes.X01
        ):
            self.set_body(CENotifyMessageBody(super().body))
        self.set_attr()
