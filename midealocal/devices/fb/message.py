"""Midea local FB message."""

from midealocal.const import DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)

CHILD_LOCK_BYTE = 18
ENERGY_CONSUMPTION_BYTE = 21
MAX_HEATING_LEVEL = 10
MAX_HUMIDITY = 100
MAX_TARGET_TEMP = 50
MIN_TARGET_TEMP = -40


class MessageFBBase(MessageRequest):
    """FB message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes = ListTypes.X00,
    ) -> None:
        """Initialize FB message base."""
        super().__init__(
            device_type=DeviceType.FB,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageFBBase):
    """FB message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize FB message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
        )

    @property
    def body(self) -> bytearray:
        """FB message query body."""
        return bytearray([])

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class MessageSet(MessageFBBase):
    """FB message set."""

    def __init__(self, protocol_version: int, subtype: int) -> None:
        """Initialize FB message set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X00,
        )
        self._subtype = subtype
        self.power: bool | None = None
        self.mode: int | None = None
        self.heating_level: int | None = None
        self.target_temperature: int | None = None
        self.child_lock: bool | None = None

    @property
    def body(self) -> bytearray:
        """FB message set body."""
        power = 0 if self.power is None else (0x01 if self.power else 0x02)
        mode = 0 if self.mode is None else self.mode
        heating_level = (
            0
            if self.heating_level is None
            else (
                int(
                    self.heating_level
                    if 1 <= self.heating_level <= MAX_HEATING_LEVEL
                    else 0,
                )
                & 0xFF
            )
        )
        target_temperature = (
            0
            if self.target_temperature is None
            else (
                int(
                    (self.target_temperature + 41)
                    if MIN_TARGET_TEMP <= self.target_temperature <= MAX_TARGET_TEMP
                    else (0x80 if self.target_temperature in [0x80, 87] else 0),
                )
                & 0xFF
            )
        )
        child_lock = (
            0xFF if self.child_lock is None else (0x01 if self.child_lock else 0x00)
        )
        _return_body = bytearray(
            [
                power,
                0x00,
                0x00,
                0x00,
                mode,
                heating_level,
                target_temperature,
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
                child_lock,
                0x00,
            ],
        )
        if self._subtype > ListTypes.X05:
            _return_body += bytearray([0x00, 0x00, 0x00])
        return _return_body

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class FBGeneralMessageBody(MessageBody):
    """FB message general body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize FB message general body."""
        super().__init__(body)
        self.power = (body[0] & 0x01) not in [0, 2]
        self.mode = body[4]
        self.heating_level = body[5]
        self.target_temperature = body[6] - 41
        if 1 <= body[7] <= MAX_HUMIDITY:
            self.target_humidity = body[7]
            self.current_humidity = body[12]
        self.current_temperature = body[13] - 20
        if len(body) > CHILD_LOCK_BYTE:
            self.child_lock = (body[18] & 0x01) > 0
        if len(body) > ENERGY_CONSUMPTION_BYTE:
            self.energy_consumption = (body[21] << 8) + body[20]


class MessageFBResponse(MessageResponse):
    """FB message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize FB message response."""
        super().__init__(bytearray(message))
        if self.message_type in [
            MessageType.query,
            MessageType.set,
            MessageType.notify1,
        ]:
            self.set_body(FBGeneralMessageBody(super().body))
        self.set_attr()
