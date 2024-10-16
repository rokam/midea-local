"""Midea local B8 message."""

from midealocal.const import DeviceType
from midealocal.message import (
    BoolParser,
    IntEnumParser,
    IntParser,
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)

from .const import (
    B8CleanMode,
    B8ControlType,
    B8DeviceAttributes,
    B8ErrorCanFixDescription,
    B8ErrorRebootDescription,
    B8ErrorType,
    B8ErrorWarningDescription,
    B8FanLevel,
    B8FunctionType,
    B8MopState,
    B8Moviment,
    B8Speed,
    B8StatusType,
    B8WaterLevel,
    B8WorkMode,
    B8WorkStatus,
)


class MessageB8Base(MessageRequest):
    """B8 message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize B8 message base."""
        super().__init__(
            device_type=DeviceType.B8,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageB8Base):
    """B8 message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize B8 message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X32,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x01])


class MessageSet(MessageB8Base):
    """B8 message set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize B8 message set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X22,
        )
        self.clean_mode = B8CleanMode.AUTO
        self.fan_level = B8FanLevel.NORMAL
        self.water_level = B8WaterLevel.LOW
        self.voice_volume = 0
        self.zone_id = 0

    @property
    def _body(self) -> bytearray:
        return bytearray(
            [
                0x02,
                0x02,
                self.clean_mode,
                self.fan_level,
                self.water_level,
                self.voice_volume,
                self.zone_id,
            ]
            + [0x00] * 7,
        )


class MessageSetCommand(MessageB8Base):
    """B8 message set command."""

    def __init__(
        self,
        protocol_version: int,
        work_mode: B8WorkMode,
    ) -> None:
        """Initialize B8 message set command."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X22,
        )
        self.work_mode = work_mode

    @property
    def _body(self) -> bytearray:
        return bytearray(
            [
                self.work_mode,
                0x00,
                0x00,
            ],
        )


class MessageB8GenericBody(MessageBody):
    """B8 message generic body."""

    def __init__(self, body: bytearray, offset: int) -> None:
        """Initialize B8 message generic body."""
        super().__init__(body)
        self.parser_list.extend(
            [
                IntEnumParser[B8WorkStatus](
                    B8DeviceAttributes.WORK_STATUS,
                    1 + offset,
                    B8WorkStatus,
                ),
                IntEnumParser[B8FunctionType](
                    B8DeviceAttributes.FUNCTION_TYPE,
                    2 + offset,
                    B8FunctionType,
                ),
                IntEnumParser[B8ControlType](
                    B8DeviceAttributes.CONTROL_TYPE,
                    3 + offset,
                    B8ControlType,
                ),
                IntEnumParser[B8Moviment](
                    B8DeviceAttributes.MOVE_DIRECTION,
                    4 + offset,
                    B8Moviment,
                ),
                IntEnumParser[B8CleanMode](
                    B8DeviceAttributes.CLEAN_MODE,
                    5 + offset,
                    B8CleanMode,
                ),
                IntEnumParser[B8FanLevel](
                    B8DeviceAttributes.FAN_LEVEL,
                    6 + offset,
                    B8FanLevel,
                ),
                IntParser(B8DeviceAttributes.AREA, 7 + offset),
                IntEnumParser[B8WaterLevel](
                    B8DeviceAttributes.WATER_LEVEL,
                    8 + offset,
                    B8WaterLevel,
                ),
                IntParser(B8DeviceAttributes.VOICE_VOLUME, 9 + offset, max_value=100),
                BoolParser(
                    B8DeviceAttributes.HAVE_RESERVE_TASK,
                    10 + offset,
                ),
                IntParser(
                    B8DeviceAttributes.BATTERY_PERCENT,
                    11 + offset,
                    max_value=100,
                ),
                IntParser(B8DeviceAttributes.WORK_TIME, 12 + offset),
                BoolParser(B8DeviceAttributes.UV_SWITCH, 13 + offset, bit=0),
                BoolParser(B8DeviceAttributes.WIFI_SWITCH, 13 + offset, bit=1),
                BoolParser(B8DeviceAttributes.VOICE_SWITCH, 13 + offset, bit=2),
                BoolParser(B8DeviceAttributes.COMMAND_SOURCE, 13 + offset, bit=6),
                BoolParser(B8DeviceAttributes.DEVICE_ERROR, 13 + offset, bit=7),
                IntEnumParser[B8ErrorType](
                    B8DeviceAttributes.ERROR_TYPE,
                    14 + offset,
                    B8ErrorType,
                ),
                IntEnumParser[B8MopState](
                    B8DeviceAttributes.MOP,
                    16 + offset,
                    B8MopState,
                    default_value=B8MopState.LACK_WATER,
                ),
                BoolParser(B8DeviceAttributes.CARPET_SWITCH, 17 + offset),
                BoolParser(
                    B8DeviceAttributes.LASER_SENSOR_ERROR,
                    18 + offset,
                    bit=0,
                ),
                BoolParser(
                    B8DeviceAttributes.LASER_SENSOR_SHELTER,
                    18 + offset,
                    bit=1,
                ),
                BoolParser(
                    B8DeviceAttributes.BOARD_COMMUNICATION_ERROR,
                    18 + offset,
                    bit=2,
                ),
                IntEnumParser[B8Speed](B8DeviceAttributes.SPEED, 19 + offset, B8Speed),
            ],
        )
        self.parse_all()

        # Error description without parser
        self.error_desc: (
            B8ErrorCanFixDescription
            | B8ErrorRebootDescription
            | B8ErrorWarningDescription
        ) = B8ErrorCanFixDescription.NO
        error_type = getattr(self, B8DeviceAttributes.ERROR_TYPE, B8ErrorType.NO)
        if error_type == B8ErrorType.CAN_FIX:
            self.error_desc = B8ErrorCanFixDescription(
                self.read_byte(body, 15 + offset),
            )
        elif error_type == B8ErrorType.REBOOT:
            self.error_desc = B8ErrorRebootDescription(
                self.read_byte(body, 15 + offset),
            )
        elif error_type == B8ErrorType.WARNING:
            self.error_desc = B8ErrorWarningDescription(
                self.read_byte(body, 15 + offset),
            )


class MessageB8WorkStatusBody(MessageB8GenericBody):
    """B8 message work status body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize B8 message work status body."""
        super().__init__(body, 1)


class MessageB8NotifyBody(MessageB8GenericBody):
    """B8 message notify body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize B8 message notify body."""
        super().__init__(body, 0)


class MessageB8Response(MessageResponse):
    """B8 message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize B8 message response."""
        super().__init__(bytearray(message))
        body = MessageB8Response.parse_body(
            MessageType(self.message_type),
            super().body,
        )
        if body is not None:
            self.set_body(body)
            self.set_attr()

    @staticmethod
    def parse_body(message_type: MessageType, body: bytearray) -> MessageBody | None:
        """Parse body."""
        body_type = body[0]
        status_type = body[1]
        if (
            message_type == MessageType.query
            and body_type == ListTypes.X32
            and status_type == B8StatusType.X01
        ):
            return MessageB8WorkStatusBody(body)
        if message_type == MessageType.notify1 and body_type == ListTypes.X42:
            return MessageB8NotifyBody(body)
        return None
