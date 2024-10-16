"""Midea local FD message."""

from midealocal.const import DeviceType
from midealocal.crc8 import calculate
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)

DISINFECT_A0_BODY_LENGTH = 29
DISINFECT_C8_BODY_LENGTH = 36
MAX_FAN_SPEED = 5
MAX_MSG_SERIAL_NUM = 254


class MessageFDBase(MessageRequest):
    """FD message base."""

    _message_serial = 0

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize FD message base."""
        super().__init__(
            device_type=DeviceType.FD,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )
        MessageFDBase._message_serial += 1
        if MessageFDBase._message_serial >= MAX_MSG_SERIAL_NUM:
            MessageFDBase._message_serial = 1
        self._message_id = MessageFDBase._message_serial

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError

    @property
    def body(self) -> bytearray:
        """FD message base body."""
        body = bytearray([self.body_type]) + self._body + bytearray([self._message_id])
        body.append(calculate(body))
        return body


class MessageQuery(MessageFDBase):
    """FD message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize FD message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X41,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray(
            [
                0x81,
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


class MessageSet(MessageFDBase):
    """FD message set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize FD message set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X48,
        )
        self.power = False
        self.fan_speed = 0
        self.target_humidity = 50
        self.prompt_tone = False
        self.screen_display = 0x07
        self.mode = 0x01
        self.disinfect = None

    @property
    def _body(self) -> bytearray:
        power = 0x01 if self.power else 0x00
        prompt_tone = 0x40 if self.prompt_tone else 0x00
        disinfect = 0 if self.disinfect is None else (1 if self.disinfect else 2)
        return bytearray(
            [
                power | prompt_tone | 0x02,
                0x00,
                self.fan_speed,
                0x00,
                0x00,
                0x00,
                self.target_humidity,
                0x00,
                self.screen_display,
                self.mode,
                0x00,
                0x00,
                0x00,
                0x00,
                disinfect,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )


class FDC8MessageBody(MessageBody):
    """FD message C8 body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize FD message C8 body."""
        super().__init__(body)
        self.power = (body[1] & 0x01) > 0
        self.fan_speed = body[3] & 0x7F
        self.target_humidity = body[7]
        self.current_humidity = body[16]
        self.current_temperature = (body[17] - 50) / 2
        self.tank = body[10]
        self.mode = (body[8] & 0x70) >> 4
        self.screen_display = body[9] & 0x07
        if len(body) > DISINFECT_C8_BODY_LENGTH:
            disinfect = body[34] & 0x03
            if disinfect:
                self.disinfect = disinfect == 1


class FDA0MessageBody(MessageBody):
    """FD message A0 body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize FD message A0 body."""
        super().__init__(body)
        self.power = (body[1] & 0x01) > 0
        self.fan_speed = body[3] & 0x7F
        self.target_humidity = body[7]
        self.current_humidity = body[16]
        self.current_temperature = (body[17] - 50) / 2
        self.tank = body[10]
        self.mode = body[10] & 0x07
        self.screen_display = body[9] & 0x07
        if len(body) > DISINFECT_A0_BODY_LENGTH:
            disinfect = body[27] & 0x03
            if disinfect:
                self.disinfect = disinfect == 1


class MessageFDResponse(MessageResponse):
    """FD message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize FD message response."""
        super().__init__(bytearray(message))
        if self.message_type in [
            MessageType.query,
            MessageType.set,
            MessageType.notify1,
        ]:
            if self.body_type in [0xB0, 0xB1]:
                pass
            elif self.body_type == ListTypes.A0:
                self.set_body(FDA0MessageBody(super().body))
            elif self.body_type == ListTypes.C8:
                self.set_body(FDC8MessageBody(super().body))
        self.fan_speed: int
        self.set_attr()
        if (
            hasattr(self, "fan_speed")
            and self.fan_speed is not None
            and self.fan_speed < MAX_FAN_SPEED
        ):
            self.fan_speed = 1
