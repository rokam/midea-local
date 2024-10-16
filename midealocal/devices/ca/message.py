"""Midea local CA message."""

from midealocal.const import DeviceType
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
)

MIN_CA_GENERAL_BODY_LENGTH = 20
TEMP_POS_LOWER_VALUE = 1
TEMP_POS_UPPER_VALUE = 29
TEMP_NEG_LOWER_VALUE = 49
TEMP_NEG_UPPER_VALUE = 54


class MessageCABase(MessageRequest):
    """CA message base."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize CA message base."""
        super().__init__(
            device_type=DeviceType.CA,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError


class MessageQuery(MessageCABase):
    """CA message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize CA message query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X00,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([])


class CAGeneralMessageBody(MessageBody):
    """CA message general body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize CA message general body."""
        super().__init__(body)
        self.refrigerator_setting_temp = body[2] & 0x0F
        self.freezer_setting_temp = -12 - ((body[2] & 0xF0) >> 4)
        flex_zone_setting_temp = body[3]
        right_flex_zone_setting_temp = body[4]

        if TEMP_POS_LOWER_VALUE <= flex_zone_setting_temp <= TEMP_POS_UPPER_VALUE:
            self.flex_zone_setting_temp = flex_zone_setting_temp - 19
        elif TEMP_NEG_LOWER_VALUE <= flex_zone_setting_temp <= TEMP_NEG_UPPER_VALUE:
            self.flex_zone_setting_temp = 30 - flex_zone_setting_temp
        else:
            self.flex_zone_setting_temp = 0
        if TEMP_POS_LOWER_VALUE <= right_flex_zone_setting_temp <= TEMP_POS_UPPER_VALUE:
            self.right_flex_zone_setting_temp = right_flex_zone_setting_temp - 19
        elif (
            TEMP_NEG_LOWER_VALUE <= right_flex_zone_setting_temp <= TEMP_NEG_UPPER_VALUE
        ):
            self.right_flex_zone_setting_temp = 30 - right_flex_zone_setting_temp
        else:
            self.right_flex_zone_setting_temp = 0

        self.energy_consumption = (body[13] << 8) + body[12]
        self.refrigerator_actual_temp = (body[17] - 100) / 2
        self.freezer_actual_temp = (body[18] - 100) / 2
        self.flex_zone_actual_temp = (body[19] - 100) / 2
        self.right_flex_zone_actual_temp = (body[20] - 100) / 2


class CAExceptionMessageBody(MessageBody):
    """CA message exception body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize CA message exception body."""
        super().__init__(body)
        self.refrigerator_door_overtime = (body[1] & 0x01) > 0
        self.freezer_door_overtime = (body[1] & 0x02) > 0
        self.bar_door_overtime = (body[1] & 0x04) > 0
        self.flex_zone_door_overtime = (body[1] & 0x08) > 0


class CANotify00MessageBody(MessageBody):
    """CA message notify00 body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize CA message notify00 body."""
        super().__init__(body)
        self.refrigerator_door = (body[1] & 0x01) > 0
        self.freezer_door = (body[1] & 0x02) > 0
        self.bar_door = (body[1] & 0x04) > 0
        self.flex_zone_door = (body[1] & 0x010) > 0


class CANotify01MessageBody(MessageBody):
    """CA message notify01 body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize CA message notify01 body."""
        super().__init__(body)
        self.refrigerator_setting_temp = body[37]
        self.freezer_setting_temp = -12 - body[38]
        flex_zone_setting_temp = body[39]
        right_flex_zone_setting_temp = body[40]

        if TEMP_POS_LOWER_VALUE <= flex_zone_setting_temp <= TEMP_POS_UPPER_VALUE:
            self.flex_zone_setting_temp = flex_zone_setting_temp - 19
        elif TEMP_NEG_LOWER_VALUE <= flex_zone_setting_temp <= TEMP_NEG_UPPER_VALUE:
            self.flex_zone_setting_temp = 30 - flex_zone_setting_temp
        else:
            self.flex_zone_setting_temp = 0
        if TEMP_POS_LOWER_VALUE <= right_flex_zone_setting_temp <= TEMP_POS_UPPER_VALUE:
            self.right_flex_zone_setting_temp = right_flex_zone_setting_temp - 19
        elif (
            TEMP_NEG_LOWER_VALUE <= right_flex_zone_setting_temp <= TEMP_NEG_UPPER_VALUE
        ):
            self.right_flex_zone_setting_temp = 30 - right_flex_zone_setting_temp
        else:
            self.right_flex_zone_setting_temp = 0


class MessageCAResponse(MessageResponse):
    """CA message response."""

    def __init__(self, message: bytes) -> None:
        """Initialize CA message response."""
        super().__init__(bytearray(message))
        if (
            (
                self.message_type in [MessageType.query, MessageType.set]
                and self.body_type == ListTypes.X00
            )
            or (
                self.message_type == MessageType.notify1
                and self.body_type == ListTypes.X02
            )
        ) and len(super().body) > MIN_CA_GENERAL_BODY_LENGTH:
            self.set_body(CAGeneralMessageBody(super().body))
        elif (
            self.message_type == MessageType.exception
            and self.body_type == ListTypes.X01
        ) or (
            self.message_type == MessageType.query and self.body_type == ListTypes.X02
        ):
            self.set_body(CAExceptionMessageBody(super().body))
        elif (
            self.message_type == MessageType.notify1 and self.body_type == ListTypes.X00
        ):
            self.set_body(CANotify00MessageBody(super().body))
        elif (
            self.message_type in [MessageType.query, MessageType.notify1]
            and self.body_type == ListTypes.X01
        ):
            self.set_body(CANotify01MessageBody(super().body))
        self.set_attr()
