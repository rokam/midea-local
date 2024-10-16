"""Midea local x26 message."""

from enum import IntEnum
from typing import Any

from midealocal.const import MAX_BYTE_VALUE, DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)

MAX_HEAT_LOW_TEMP = 50


class DeviceMode(IntEnum):
    """Device mode."""

    OFF = 0
    HEAT_HIGH = 1
    HEAT_LOW = 2
    BATH = 3
    BLOW = 4
    VENTILATION = 5
    DRY = 6


class Message26Base(MessageRequest):
    """X26 message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize X26 message base."""
        super().__init__(
            device_type=DeviceType.X26,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(Message26Base):
    """X26 message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize X26 message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X01,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class MessageSet(Message26Base):
    """X26 message set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize X26 message set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X01,
        )
        self.fields: dict[str, int] = {}
        self.main_light = False
        self.night_light = False
        self.mode = 0
        self.direction = 0xFD

    def read_field(self, field: str) -> int:
        """X26 message set read field."""
        value = self.fields.get(field, 0)
        return value if value else 0

    @property
    def _body(self) -> bytearray:
        return bytearray(
            [
                1 if self.main_light else 0,
                self.read_field("MAIN_LIGHT_BRIGHTNESS"),
                1 if self.night_light else 0,
                self.read_field("NIGHT_LIGHT_BRIGHTNESS"),
                self.read_field("RADAR_INDUCTION_ENABLE"),
                self.read_field("RADAR_INDUCTION_CLOSING_TIME"),
                self.read_field("LIGHT_INTENSITY_THRESHOLD"),
                self.read_field("RADAR_SENSITIVITY"),
                1 if self.mode in (DeviceMode.HEAT_LOW, DeviceMode.HEAT_HIGH) else 0,
                (
                    0
                    if self.mode not in (DeviceMode.HEAT_LOW, DeviceMode.HEAT_HIGH)
                    else 55
                    if self.mode == DeviceMode.HEAT_HIGH
                    else 30
                ),
                self.read_field("HEATING_SPEED"),
                self.direction,
                1 if self.mode == DeviceMode.BATH else 0,
                self.read_field("BATH_HEATING_TIME"),
                self.read_field("BATH_TEMPERATURE"),
                self.read_field("BATH_SPEED"),
                self.direction,
                1 if self.mode == DeviceMode.VENTILATION else 0,
                self.read_field("VENTILATION_SPEED"),
                self.direction,
                1 if self.mode == DeviceMode.DRY else 0,
                self.read_field("DRYING_TIME"),
                self.read_field("DRYING_TEMPERATURE"),
                self.read_field("DRYING_SPEED"),
                self.direction,
                1 if self.mode == DeviceMode.BLOW else 0,
                self.read_field("BLOWING_SPEED"),
                self.direction,
                self.read_field("DELAY_ENABLE"),
                self.read_field("DELAY_TIME"),
                self.read_field("SOFT_WIND_ENABLE"),
                self.read_field("SOFT_WIND_TIME"),
                self.read_field("SOFT_WIND_TEMPERATURE"),
                self.read_field("SOFT_WIND_SPEED"),
                self.read_field("SOFT_WIND_DIRECTION"),
                self.read_field("WINDLESS_ENABLE"),
                self.read_field("ANION_ENABLE"),
                self.read_field("SMELLY_ENABLE"),
                self.read_field("SMELLY_THRESHOLD"),
            ],
        )


class Message26Body(MessageBody):
    """X26 message body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize X26 message body."""
        super().__init__(body)
        self.fields = self._gen_fields(body)
        self.main_light = self.read_byte(body, 1) > 0
        self.night_light = self.read_byte(body, 3) > 0
        heat_mode = self.read_byte(body, 9) > 0
        heat_temperature = self.read_byte(body, 10)
        heat_direction = self.read_byte(body, 12)
        bath_mode = self.read_byte(body, 13) > 0
        bath_direction = self.read_byte(body, 17)
        ventilation_mode = self.read_byte(body, 18) > 0
        ventilation_direction = self.read_byte(body, 20)
        dry_mode = self.read_byte(body, 21) > 0
        dry_direction = self.read_byte(body, 25)
        blow_mode = self.read_byte(body, 26) > 0
        blow_direction = self.read_byte(body, 28)
        if self.read_byte(body, 31) != MAX_BYTE_VALUE:
            self.current_humidity = self.read_byte(body, 31)
        if self.read_byte(body, 32) != MAX_BYTE_VALUE:
            self.current_radar = self.read_byte(body, 32)
        if self.read_byte(body, 33) != MAX_BYTE_VALUE:
            self.current_temperature = self.read_byte(body, 33)
        self.mode = 0
        self.direction = 0xFD
        if heat_mode:
            if heat_temperature > MAX_HEAT_LOW_TEMP:
                self.mode = 1
            else:
                self.mode = 2
            self.direction = heat_direction
        elif bath_mode:
            self.mode = 3
            self.direction = bath_direction
        elif blow_mode:
            self.mode = 4
            self.direction = blow_direction
        elif ventilation_mode:
            self.mode = 5
            self.direction = ventilation_direction
        elif dry_mode:
            self.mode = 6
            self.direction = dry_direction

    def _gen_fields(self, body: bytearray) -> dict[str, int]:
        fields: dict[str, int] = {}
        fields["MAIN_LIGHT_BRIGHTNESS"] = self.read_byte(body, 2)
        fields["NIGHT_LIGHT_BRIGHTNESS"] = self.read_byte(body, 4)
        fields["RADAR_INDUCTION_ENABLE"] = self.read_byte(body, 5)
        fields["RADAR_INDUCTION_CLOSING_TIME"] = self.read_byte(body, 6)
        fields["LIGHT_INTENSITY_THRESHOLD"] = self.read_byte(body, 7)
        fields["RADAR_SENSITIVITY"] = self.read_byte(body, 8)
        fields["HEATING_SPEED"] = self.read_byte(body, 11)
        fields["BATH_HEATING_TIME"] = self.read_byte(body, 14)
        fields["BATH_TEMPERATURE"] = self.read_byte(body, 15)
        fields["BATH_SPEED"] = self.read_byte(body, 16)
        fields["VENTILATION_SPEED"] = self.read_byte(body, 19)
        fields["DRYING_TIME"] = self.read_byte(body, 22)
        fields["DRYING_TEMPERATURE"] = self.read_byte(body, 23)
        fields["DRYING_SPEED"] = self.read_byte(body, 24)
        fields["BLOWING_SPEED"] = self.read_byte(body, 27)
        fields["DELAY_ENABLE"] = self.read_byte(body, 29)
        fields["DELAY_TIME"] = self.read_byte(body, 30)
        fields["SOFT_WIND_ENABLE"] = self.read_byte(body, 38)
        fields["SOFT_WIND_TIME"] = self.read_byte(body, 39)
        fields["SOFT_WIND_TEMPERATURE"] = self.read_byte(body, 40)
        fields["SOFT_WIND_SPEED"] = self.read_byte(body, 41)
        fields["SOFT_WIND_DIRECTION"] = self.read_byte(body, 42)
        fields["WINDLESS_ENABLE"] = self.read_byte(body, 43)
        fields["ANION_ENABLE"] = self.read_byte(body, 44)
        fields["SMELLY_ENABLE"] = self.read_byte(body, 45)
        fields["SMELLY_THRESHOLD"] = self.read_byte(body, 46)

        return fields


class Message26Response(MessageResponse):
    """X26 message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize X26 message response."""
        super().__init__(bytearray(message))
        if (
            self.message_type
            in [MessageType.set, MessageType.notify1, MessageType.query]
            and self.body_type == 0x01
        ):
            self.set_body(Message26Body(super().body))
        self.fields: dict[str, Any]
        self.set_attr()
