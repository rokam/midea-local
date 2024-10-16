"""Midea local E2 message."""

from midealocal.const import DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)

HEATING_POWER_BYTE = 34
PROTECTION_BYTE = 22
WATER_CONSUMPTION_BYTE = 25


class MessageE2Base(MessageRequest):
    """E2 message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize E2 message base."""
        super().__init__(
            device_type=DeviceType.E2,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageE2Base):
    """E2 message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize E2 message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X01,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x01])


class MessagePower(MessageE2Base):
    """E2 message power."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize E2 message power."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X02,
        )
        self.power = False

    @property
    def _body(self) -> bytearray:
        if self.power:
            self.body_type = ListTypes.X01
        else:
            self.body_type = ListTypes.X02
        return bytearray([0x01])


class MessageNewProtocolSet(MessageE2Base):
    """E2 message new protocol set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize E2 message new protocol set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X14,
        )
        self.target_temperature: int | None = None
        self.variable_heating: bool | None = None
        self.whole_tank_heating: bool | None = None

    @property
    def _body(self) -> bytearray:
        byte1 = 0x00
        byte2 = 0x00
        if self.target_temperature is not None:
            byte1 = 0x07
            byte2 = int(self.target_temperature) & 0xFF
        elif self.whole_tank_heating is not None:
            byte1 = 0x04
            byte2 = 0x02 if self.whole_tank_heating else 0x01
        elif self.variable_heating is not None:
            byte1 = 0x10
            byte2 = 0x01 if self.variable_heating else 0x00
        return bytearray([byte1, byte2])


class MessageSet(MessageE2Base):
    """E2 message set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize E2 message set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X04,
        )
        self.target_temperature = 0
        self.variable_heating = False
        self.whole_tank_heating = False
        self.protection = False

    @property
    def _body(self) -> bytearray:
        # Byte 4 whole_tank_heating, protection
        protection = 0x04 if self.protection else 0x00
        whole_tank_heating = 0x02 if self.whole_tank_heating else 0x01
        # Byte 5 target_temperature
        target_temperature = self.target_temperature & 0xFF
        # Byte 9 variable_heating
        variable_heating = 0x10 if self.variable_heating else 0x00
        return bytearray(
            [
                0x01,
                0x00,
                0x80,
                whole_tank_heating | protection,
                target_temperature,
                0x00,
                0x00,
                0x00,
                variable_heating,
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


class E2GeneralMessageBody(MessageBody):
    """E2 message general body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize E2 message general body."""
        super().__init__(body)
        self.power = (body[2] & 0x01) > 0
        self.heating = (body[2] & 0x04) > 0
        self.keep_warm = (body[2] & 0x08) > 0
        self.variable_heating = (body[2] & 0x80) > 0
        self.current_temperature = body[4]
        self.whole_tank_heating = (body[7] & 0x08) > 0
        self.heating_time_remaining = body[9] * 60 + body[10]
        self.target_temperature = body[11]
        self.protection = (
            ((body[22] & 0x02) > 0) if len(body) > PROTECTION_BYTE else False
        )
        if len(body) > WATER_CONSUMPTION_BYTE:
            self.water_consumption = body[24] + (body[25] << 8)
        if len(body) > HEATING_POWER_BYTE:
            self.heating_power = body[34] * 100


class MessageE2Response(MessageResponse):
    """E2 message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize E2 message response."""
        super().__init__(bytearray(message))
        if (
            self.message_type in [MessageType.query, MessageType.notify1]
            and self.body_type == 0x01
        ) or (
            self.message_type == MessageType.set
            and self.body_type in [0x01, 0x02, 0x04, 0x14]
        ):
            self.set_body(E2GeneralMessageBody(super().body))
        self.set_attr()
