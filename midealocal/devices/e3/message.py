"""Midea local E3 message."""

from typing import Any

from midealocal.const import DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)

NEW_PROTOCOL_PARAMS = {
    "none": 0x00,
    "zero_cold_water": 0x03,
    "zero_cold_pulse": 0x04,
    "smart_volume": 0x07,
    "target_temperature": 0x08,
}

ADDITIONAL_BYTE = 20


class MessageE3Base(MessageRequest):
    """E3 message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize E3 message base."""
        super().__init__(
            device_type=DeviceType.E3,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageE3Base):
    """E3 message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize E3 message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X01,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x01])


class MessagePower(MessageE3Base):
    """E3 message power."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize E3 message power."""
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


class MessageSet(MessageE3Base):
    """E3 message set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize E3 message set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X04,
        )

        self.target_temperature = 0
        self.zero_cold_water = False
        self.bathtub_volume = 0
        self.protection = False
        self.zero_cold_pulse = False
        self.smart_volume = False

    @property
    def _body(self) -> bytearray:
        # Byte 2 zero_cold_water mode
        zero_cold_water = 0x01 if self.zero_cold_water else 0x00
        # Byte 3
        protection = 0x08 if self.protection else 0x00
        zero_cold_pulse = 0x10 if self.zero_cold_pulse else 0x00
        smart_volume = 0x20 if self.smart_volume else 0x00
        # Byte 5 target_temperature
        target_temperature = self.target_temperature & 0xFF

        return bytearray(
            [
                0x01,
                zero_cold_water | 0x02,
                protection | zero_cold_pulse | smart_volume,
                0x00,
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
            ],
        )


class MessageNewProtocolSet(MessageE3Base):
    """E3 message new protocol set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize E3 message new protocol set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X14,
        )
        self.key = "none"
        self.value: Any = None

    @property
    def _body(self) -> bytearray:
        key = NEW_PROTOCOL_PARAMS[self.key]
        if self.key == "target_temperature":
            value = self.value
        else:
            value = 0x01 if self.value else 0x00
        return bytearray(
            [
                key,
                value,
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
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )


class E3GeneralMessageBody(MessageBody):
    """E3 message general body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize E3 message general body."""
        super().__init__(body)
        self.power = (body[2] & 0x01) > 0
        self.burning_state = (body[2] & 0x02) > 0
        self.zero_cold_water = (body[2] & 0x04) > 0
        self.current_temperature = body[5]
        self.target_temperature = body[6]
        self.protection = (body[8] & 0x08) > 0
        self.zero_cold_pulse = (
            (body[20] & 0x01) > 0 if len(body) > ADDITIONAL_BYTE else False
        )
        self.smart_volume = (
            (body[20] & 0x02) > 0 if len(body) > ADDITIONAL_BYTE else False
        )


class MessageE3Response(MessageResponse):
    """E3 message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize E3 message response."""
        super().__init__(bytearray(message))
        if (
            (self.message_type == MessageType.query and self.body_type == 0x01)
            or (
                self.message_type == MessageType.set
                and self.body_type in [0x01, 0x02, 0x04, 0x14]
            )
            or (
                self.message_type == MessageType.notify1
                and self.body_type in [0x00, 0x01]
            )
        ):
            self.set_body(E3GeneralMessageBody(super().body))
        self.set_attr()
