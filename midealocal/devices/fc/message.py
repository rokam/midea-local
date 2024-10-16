"""Midea local FC message."""

from midealocal.const import MAX_BYTE_VALUE, DeviceType
from midealocal.crc8 import calculate
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)

ANION_GET_BYTE = 19
ANION_NOTIFY_BYTE = 10
CHILD_LOCK_GET_BYTE = 8
CHILD_LOCK_NOTIFY_BYTE = 10
DETECT_MODE_GET_BYTE = 29
DETECT_MODE_NOTIFY_BYTE = 22
FILTER1_LIFE_BYTE = 23
FILTER2_LIFE_BYTE = 24
HCHO_GET_BYTE = 38
HCHO_NOTIFY_BYTE = 31
MAX_MSG_SERIAL_NUM = 254
PM25_BYTE = 14
STANDBY_GET_BYTE = 34
STANDBY_NOTIFY_BYTE = 27
STANDBY_VALUE = 0x14
TVOC_BYTE = 15


class MessageFCBase(MessageRequest):
    """FC message base."""

    _message_serial = 0

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize FC message base."""
        super().__init__(
            device_type=DeviceType.FC,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )
        MessageFCBase._message_serial += 1
        if MessageFCBase._message_serial >= MAX_MSG_SERIAL_NUM:
            MessageFCBase._message_serial = 1
        self._message_id = MessageFCBase._message_serial

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError

    @property
    def body(self) -> bytearray:
        """FC message base body."""
        body = bytearray([self.body_type]) + self._body + bytearray([self._message_id])
        body.append(calculate(body))
        return body


class MessageQuery(MessageFCBase):
    """FC message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize FC message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X41,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray(
            [
                0x00,
                0x00,
                0xFF,
                0x03,
                0x00,
                0x00,
                0x02,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )


class MessageSet(MessageFCBase):
    """FC message set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize FC message set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X48,
        )
        self.power = False
        self.mode = 0
        self.fan_speed = 0
        self.child_lock = False
        self.prompt_tone = False
        self.anion = False
        self.standby = False
        self.screen_display = 0
        self.detect_mode = 0
        self.standby_detect = [40, 20]

    @property
    def _body(self) -> bytearray:
        # byte1 power
        power = 0x01 if self.power else 0x00
        detect = 0x08 if self.detect_mode > 0 else 0x00
        detect_mode = (self.detect_mode - 1) if self.detect_mode > 0 else 0
        # byte2 mode
        # byte3 fan_speed
        # byte 8 child_lock
        child_lock = 0x80 if self.child_lock else 0x00
        # byte 9 anion
        anion = 0x20 if self.anion else 0x00
        # byte 10 prompt_tone
        prompt_tone = 0x40 if self.prompt_tone else 0x00
        # byte 15/16/17 standby
        if self.standby:
            standby = 0x04
            standby_detect_high = self.standby_detect[0]
            standby_detect_low = self.standby_detect[1]
        else:
            standby = 0x08
            standby_detect_high = 0
            standby_detect_low = 0
        return bytearray(
            [
                power | prompt_tone | detect | 0x02,
                self.mode,
                self.fan_speed,
                0x00,
                0x00,
                0x00,
                0x00,
                child_lock,
                self.screen_display,
                anion,
                0x00,
                0x00,
                0x00,
                detect_mode,
                standby,
                standby_detect_high,
                standby_detect_low,
                0x00,
                0x00,
                0x00,
            ],
        )


class FCGeneralMessageBody(MessageBody):
    """FC message general body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize FC message general body."""
        super().__init__(body)
        self.power = (body[1] & 0x01) > 0
        self.mode = body[2] & 0xF0
        self.fan_speed = body[3] & 0x7F
        self.screen_display = body[9] & 0x07
        self.pm25: int | None = None
        self.tvoc: int | None = None
        self.hcho: int | None = None

        if len(body) > PM25_BYTE and body[14] != MAX_BYTE_VALUE:
            self.pm25 = body[13] + (body[14] << 8)
        if len(body) > TVOC_BYTE and body[15] != MAX_BYTE_VALUE:
            self.tvoc = body[15]
        self.anion = (body[19] & 0x40 > 0) if len(body) > ANION_GET_BYTE else False
        self.standby = (
            ((body[34] & 0xFF) == STANDBY_VALUE)
            if len(body) > STANDBY_GET_BYTE
            else False
        )
        self.child_lock = (
            (body[8] & 0x80 > 0) if len(body) > CHILD_LOCK_GET_BYTE else False
        )
        if len(body) > FILTER1_LIFE_BYTE:
            self.filter1_life = body[23]
        if len(body) > FILTER2_LIFE_BYTE:
            self.filter2_life = body[24]
        if len(body) > DETECT_MODE_GET_BYTE:
            if (body[1] & 0x08) > 0:
                self.detect_mode = body[29] + 1
            else:
                self.detect_mode = 0
        if len(body) > HCHO_GET_BYTE and body[38] != MAX_BYTE_VALUE:
            self.hcho = body[37] + (body[38] << 8)


class FCNotifyMessageBody(MessageBody):
    """FC message notify body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize FC message notify body."""
        super().__init__(body)
        self.power = (body[1] & 0x01) > 0
        self.mode = body[2] & 0xF0
        self.fan_speed = body[3] & 0x7F
        self.screen_display = body[9] & 0x07
        self.pm25: int | None = None
        self.tvoc: int | None = None
        self.hcho: int | None = None

        if len(body) > PM25_BYTE and body[14] != MAX_BYTE_VALUE:
            self.pm25 = body[13] + (body[14] << 8)
        if len(body) > TVOC_BYTE and body[15] != MAX_BYTE_VALUE:
            self.tvoc = body[15]
        self.anion = (body[10] & 0x20 > 0) if len(body) > ANION_NOTIFY_BYTE else False
        self.standby = (
            (body[27] & 0x14 == MAX_BYTE_VALUE)
            if len(body) > STANDBY_NOTIFY_BYTE
            else False
        )
        self.child_lock = (
            (body[10] & 0x10 > 0) if len(body) > CHILD_LOCK_NOTIFY_BYTE else False
        )
        if len(body) > DETECT_MODE_NOTIFY_BYTE:
            if (body[1] & 0x08) > 0:
                self.detect_mode = body[22] + 1
            else:
                self.detect_mode = 0
        if len(body) > HCHO_NOTIFY_BYTE and body[31] != MAX_BYTE_VALUE:
            self.hcho = body[30] + (body[31] << 8)


class MessageFCResponse(MessageResponse):
    """FC message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize FC message response."""
        super().__init__(bytearray(message))
        if self.body_type in [ListTypes.B0, ListTypes.B1]:
            pass
        elif (
            self.message_type
            in [MessageType.query, MessageType.set, MessageType.notify1]
            and self.body_type == ListTypes.C8
        ):
            self.set_body(FCGeneralMessageBody(super().body))
        elif (
            self.message_type == MessageType.notify1 and self.body_type == ListTypes.A0
        ):
            self.set_body(FCNotifyMessageBody(super().body))
        self.set_attr()
