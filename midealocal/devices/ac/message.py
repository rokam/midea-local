"""Midea AC message."""

from enum import IntEnum

from midealocal.const import MAX_BYTE_VALUE, DeviceType
from midealocal.crc8 import calculate
from midealocal.message import (
    ListTypes,
    MessageBody,
    MessageRequest,
    MessageResponse,
    MessageType,
    NewProtocolMessageBody,
)

BB_AC_MODES = [0, 3, 1, 2, 4, 5]
BB_MIN_BODY_LENGTH = 21
CONFORT_MODE_MIN_LENGTH = 16
CONFORT_MODE_C0_MIN_LENGTH = 23
ECO_MODE_MIN_SUBPROTOCOL_LENGTH = 27
FRESH_AIR_LENGTH = 2
FROST_PROTECT_C0_MIN_LENGTH = 22
INDIRECT_WIND_VALUE = 0x02
MAX_MSG_SERIAL_NUM = 254
SCREEN_DISPLAY_BYTE_CHECK = 0x07
SUB_PROTOCOL_BODY_TEMP_CHECK = 0x80
TEMP_DECIMAL_MIN_BODY_LENGTH = 20
TEMP_NEG_VALUE = 49
TIMER_MIN_SUBPROTOCOL_LENGTH = 27
XBB_SN8_BYTE_FLAG = 0x31
XC1_SUBBODY_TYPE_44 = 0x44
XC1_SUBBODY_TYPE_40 = 0x40


class Capabilities(IntEnum):
    """AC Capabilities."""

    SWING_UD_ANGLE = 0x0009
    SWING_LR_ANGLE = 0x000A
    SILKY_COOL = 0x0018
    SMART_EYE = 0x0030
    WIND_ON_ME = 0x0032
    WIND_OFF_ME = 0x0033
    SELF_CLEAN = 0x0039  # AKA Active Clean
    ONE_KEY_NO_WIND_ON_ME = 0x0042
    BREEZE_CONTROL = 0x0043  # AKA "FA No Wind Sense"
    RATE_SELECT = 0x0048
    FRESH_AIR = 0x004B
    PARENT_CONTROL = 0x0051  # ??
    PREVENT_STRAIGHT_WIND_SELECT = 0x0058  # ??
    WIND_AROUND = 0x0059  # ??
    JET_COOL = 0x0067  # ??
    IECO_SWITCH = 0x00E3  # ??
    ICHECK = 0x0091  # ??
    EMERGENT_HEAT_WIND = 0x0093  # ??
    HEAT_PTC_WIND = 0x0094  # ??
    CVP = 0x0098  # ??
    FAN_SPEED_CONTROL = 0x0210
    PRESET_ECO = 0x0212
    PRESET_FREEZE_PROTECTION = 0x0213
    MODES = 0x0214
    SWING_MODES = 0x0215
    POWER = 0x0216
    FILTER_REMIND = 0x0217
    AUX_ELECTRIC_HEAT = 0x0219  # AKA PTC
    PRESET_TURBO = 0x021A
    FILTER_CHECK = 0x0221
    ANION = 0x021E
    HUMIDITY = 0x021F
    FAHRENHEIT = 0x0222
    DISPLAY_CONTROL = 0x0224
    TEMPERATURES = 0x0225
    BUZZER = 0x022C  # ??
    MAIN_HORIZONTAL_GUIDE_STRIP = 0x0230  # ??
    SUP_HORIZONTAL_GUIDE_STRIP = 0x0231  # ??
    TWINS_MACHINE = 0x0232  # ??
    GUIDE_STRIP_TYPE = 0x0233  # ??
    BODY_CHECK = 0x0234  # ??


class PowerAnalysisMethod(IntEnum):
    """AC Power analysis method."""

    TYPE_1 = 1
    TYPE_2 = 2
    TYPE_3 = 3


class NewProtocolTags(IntEnum):
    """New protocol tags."""

    indoor_humidity = 0x0015
    screen_display = 0x0017
    breezeless = 0x0018
    prompt_tone = 0x001A
    indirect_wind = 0x0042
    fresh_air_1 = 0x0233
    fresh_air_2 = 0x004B


class MessageACBase(MessageRequest):
    """AC message base."""

    _message_serial = 0

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        body_type: ListTypes,
    ) -> None:
        """Initialize AC message base."""
        super().__init__(
            device_type=DeviceType.AC,
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=body_type,
        )
        MessageACBase._message_serial += 1
        if MessageACBase._message_serial >= MAX_MSG_SERIAL_NUM:
            MessageACBase._message_serial = 1
        self._message_id = MessageACBase._message_serial

    @property
    def _body(self) -> bytearray:
        raise NotImplementedError

    @property
    def body(self) -> bytearray:
        """AC message base body."""
        body = bytearray([self.body_type]) + self._body + bytearray([self._message_id])
        body.append(calculate(body))
        return body


class MessageQuery(MessageACBase):
    """AC message query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize AC message query."""
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


class MessageCapabilitiesQuery(MessageACBase):
    """AC message capabilities query."""

    def __init__(
        self,
        protocol_version: int,
        additional_capabilities: bool,
    ) -> None:
        """Initialize AC message capabilities query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.B5,
        )
        self._additional_capabilities = additional_capabilities

    @property
    def _body(self) -> bytearray:
        if self._additional_capabilities:
            return bytearray([0x01, 0x01, 0x01])
        return bytearray([0x01, 0x00])


class MessagePowerQuery(MessageACBase):
    """AC message power query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize AC message power query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X41,
        )

    @property
    def _body(self) -> bytearray:
        return bytearray([0x21, 0x01, 0x44, 0x00, 0x01])

    @property
    def body(self) -> bytearray:
        """AC message power query body."""
        body = bytearray([self.body_type]) + self._body
        body.append(calculate(body))
        return body


class MessageToggleDisplay(MessageACBase):
    """AC message toggle display."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize AC message toggle display."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.X41,
        )
        self.prompt_tone = False

    @property
    def _body(self) -> bytearray:
        prompt_tone = 0x40 if self.prompt_tone else 0
        return bytearray(
            [
                0x02 | prompt_tone,
                0x00,
                0xFF,
                0x02,
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
                0x00,
            ],
        )


class MessageNewProtocolQuery(MessageACBase):
    """AC message new protocol query."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize AC message new protocol query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            body_type=ListTypes.B1,
        )

    @property
    def _body(self) -> bytearray:
        query_params = [
            NewProtocolTags.indirect_wind,
            NewProtocolTags.breezeless,
            NewProtocolTags.indoor_humidity,
            NewProtocolTags.screen_display,
            NewProtocolTags.fresh_air_1,
            NewProtocolTags.fresh_air_2,
        ]

        _body = bytearray([len(query_params)])
        for param in query_params:
            _body.extend([param & 0xFF, param >> 8])
        return _body


class MessageSubProtocol(MessageACBase):
    """AC message sub protocol."""

    def __init__(
        self,
        protocol_version: int,
        message_type: MessageType,
        subprotocol_query_type: int,
    ) -> None:
        """Initialize AC message sub protocol."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=message_type,
            body_type=ListTypes.AA,
        )
        self._subprotocol_query_type = subprotocol_query_type

    @property
    def _subprotocol_body(self) -> bytes:
        return bytes([])

    @property
    def body(self) -> bytearray:
        """AC message sub protocol body."""
        body = bytearray([self.body_type]) + self._body
        body.append(calculate(body))
        body.append(self.checksum(body))
        return body

    @property
    def _body(self) -> bytearray:
        _subprotocol_body = self._subprotocol_body
        _body = bytearray(
            [
                6
                + 2
                + (len(_subprotocol_body) if _subprotocol_body is not None else 0),
                0x00,
                0xFF,
                0xFF,
                self._subprotocol_query_type,
            ],
        )
        if _subprotocol_body is not None:
            _body.extend(_subprotocol_body)
        return _body


class MessageSubProtocolQuery(MessageSubProtocol):
    """AC message sub protocol query."""

    def __init__(
        self,
        protocol_version: int,
        subprotocol_query_type: int,
    ) -> None:
        """Initialize AC message sub protocol query."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.query,
            subprotocol_query_type=subprotocol_query_type,
        )


class MessageSubProtocolSet(MessageSubProtocol):
    """AC message sub protocol set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize AC message sub protocol set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            subprotocol_query_type=0x20,
        )
        self.power = False
        self.mode = 0
        self.target_temperature = 20.0
        self.fan_speed = 102
        self.boost_mode = False
        self.aux_heating = False
        self.dry = False
        self.eco_mode = False
        self.sleep_mode = False
        self.sn8_flag = False
        self.timer = False
        self.prompt_tone = False

    @property
    def _subprotocol_body(self) -> bytes:
        power = 0x01 if self.power else 0
        dry = 0x10 if self.power and self.dry else 0
        boost_mode = 0x20 if self.boost_mode else 0
        aux_heating = 0x40 if self.aux_heating else 0x80
        sleep_mode = 0x80 if self.sleep_mode else 0
        try:
            mode = 0 if self.mode == 0 else BB_AC_MODES[self.mode] - 1
        except IndexError:
            mode = 2  # set Auto if invalid mode
        target_temperature = int(self.target_temperature * 2 + 30)
        water_model_temperature_set = int((self.target_temperature - 1) * 2 + 50)
        fan_speed = self.fan_speed
        eco = 0x40 if self.eco_mode else 0

        prompt_tone = 0x01 if self.prompt_tone else 0
        timer = 0x04 if (self.sn8_flag and self.timer) else 0
        return bytearray(
            [
                0x02 | boost_mode | power | dry,
                aux_heating,
                sleep_mode,
                0x00,
                0x00,
                mode,
                target_temperature,
                fan_speed,
                0x32,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x01,
                0x01,
                0x00,
                0x01,
                water_model_temperature_set,
                prompt_tone,
                target_temperature,
                0x32,
                0x66,
                0x00,
                eco | timer,
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
                0x08,
            ],
        )


class MessageGeneralSet(MessageACBase):
    """AC message general set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize AC message general set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.X40,
        )
        self.power = False
        self.prompt_tone = True
        self.mode = 0
        self.target_temperature = 20.0
        self.fan_speed = 102
        self.swing_vertical = False
        self.swing_horizontal = False
        self.boost_mode = False
        self.smart_eye = False
        self.dry = False
        self.aux_heating = False
        self.eco_mode = False
        self.temp_fahrenheit = False
        self.sleep_mode = False
        self.natural_wind = False
        self.frost_protect = False
        self.comfort_mode = False

    @property
    def _body(self) -> bytearray:
        # Byte1, Power, prompt_tone
        power = 0x01 if self.power else 0
        prompt_tone = 0x40 if self.prompt_tone else 0
        # Byte2, mode target_temperature
        mode = (self.mode << 5) & 0xE0
        target_temperature = (int(self.target_temperature) & 0xF) | (
            0x10 if int(round(self.target_temperature * 2)) % 2 != 0 else 0
        )
        # Byte 3, fan_speed
        fan_speed = self.fan_speed & 0x7F
        # Byte 7, swing_mode
        swing_mode = (
            0x30
            | (0x0C if self.swing_vertical else 0)
            | (0x03 if self.swing_horizontal else 0)
        )
        # Byte 8, turbo
        boost_mode = 0x20 if self.boost_mode else 0
        # Byte 9 aux_heating eco_mode
        smart_eye = 0x01 if self.smart_eye else 0
        dry = 0x04 if self.dry else 0
        aux_heating = 0x08 if self.aux_heating else 0
        eco_mode = 0x80 if self.eco_mode else 0
        # Byte 10 temp_fahrenheit
        temp_fahrenheit = 0x04 if self.temp_fahrenheit else 0
        sleep_mode = 0x01 if self.sleep_mode else 0
        boost_mode_1 = 0x02 if self.boost_mode else 0
        # Byte 17 natural_wind
        natural_wind = 0x40 if self.natural_wind else 0
        # Byte 21 frost_protect
        frost_protect = 0x80 if self.frost_protect else 0
        # Byte 22 comfort_mode
        comfort_mode = 0x01 if self.comfort_mode else 0

        return bytearray(
            [
                power | prompt_tone,
                mode | target_temperature,
                fan_speed,
                0x00,
                0x00,
                0x00,
                swing_mode,
                boost_mode,
                smart_eye | dry | aux_heating | eco_mode,
                temp_fahrenheit | sleep_mode | boost_mode_1,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                natural_wind,
                0x00,
                0x00,
                0x00,
                frost_protect,
                comfort_mode,
            ],
        )


class MessageNewProtocolSet(MessageACBase):
    """AC message new protocol set."""

    def __init__(self, protocol_version: int) -> None:
        """Initialize AC message new protocol set."""
        super().__init__(
            protocol_version=protocol_version,
            message_type=MessageType.set,
            body_type=ListTypes.B0,
        )
        self.indirect_wind: bytes | None = None
        self.prompt_tone: bytes | None = None
        self.breezeless: bytes | None = None
        self.screen_display_alternate: bytes | None = None
        self.fresh_air_1: bytes | None = None
        self.fresh_air_2: bytes | None = None

    @property
    def _body(self) -> bytearray:
        pack_count = 0
        payload = bytearray([0x00])
        if self.breezeless is not None:
            pack_count += 1
            payload.extend(
                NewProtocolMessageBody.pack(
                    param=NewProtocolTags.breezeless,
                    value=bytearray([0x01 if self.breezeless else 0x00]),
                ),
            )
        if self.indirect_wind is not None:
            pack_count += 1
            payload.extend(
                NewProtocolMessageBody.pack(
                    param=NewProtocolTags.indirect_wind,
                    value=bytearray([0x02 if self.indirect_wind else 0x01]),
                ),
            )
        if self.prompt_tone is not None:
            pack_count += 1
            payload.extend(
                NewProtocolMessageBody.pack(
                    param=NewProtocolTags.prompt_tone,
                    value=bytearray([0x01 if self.prompt_tone else 0x00]),
                ),
            )
        if self.screen_display_alternate is not None:
            pack_count += 1
            payload.extend(
                NewProtocolMessageBody.pack(
                    param=NewProtocolTags.screen_display,
                    value=bytearray([0x64 if self.screen_display_alternate else 0x00]),
                ),
            )
        if self.fresh_air_1 is not None and len(self.fresh_air_1) == FRESH_AIR_LENGTH:
            pack_count += 1
            fresh_air_power = 2 if next(iter(self.fresh_air_1)) > 0 else 1
            fresh_air_fan_speed = list(self.fresh_air_1)[1]
            payload.extend(
                NewProtocolMessageBody.pack(
                    param=NewProtocolTags.fresh_air_1,
                    value=bytearray(
                        [
                            fresh_air_power,
                            fresh_air_fan_speed,
                            0x00,
                            0x00,
                            0x00,
                            0x00,
                            0x00,
                            0x00,
                            0x00,
                            0x00,
                        ],
                    ),
                ),
            )
        if self.fresh_air_2 is not None and len(self.fresh_air_2) == FRESH_AIR_LENGTH:
            pack_count += 1
            fresh_air_power = 1 if next(iter(self.fresh_air_2)) > 0 else 0
            fresh_air_fan_speed = list(self.fresh_air_2)[1]
            payload.extend(
                NewProtocolMessageBody.pack(
                    param=NewProtocolTags.fresh_air_2,
                    value=bytearray([fresh_air_power, fresh_air_fan_speed, 0xFF]),
                ),
            )
        payload[0] = pack_count
        return payload


class XA0MessageBody(MessageBody):
    """AC A0 message body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize AC A0 message body."""
        super().__init__(body)
        self.power = (body[1] & 0x1) > 0
        self.target_temperature = (
            ((body[1] & 0x3E) >> 1) - 4 + 16.0 + (0.5 if body[1] & 0x40 > 0 else 0.0)
        )
        self.mode = (body[2] & 0xE0) >> 5
        self.fan_speed = body[3] & 0x7F
        self.swing_vertical = (body[7] & 0xC) > 0
        self.swing_horizontal = (body[7] & 0x3) > 0
        self.boost_mode = ((body[8] & 0x20) > 0) or ((body[10] & 0x2) > 0)
        self.smart_eye = (body[9] & 0x01) > 0
        self.dry = (body[9] & 0x04) > 0
        self.aux_heating = (body[9] & 0x08) > 0
        self.eco_mode = (body[9] & 0x10) > 0
        self.sleep_mode = (body[10] & 0x01) > 0
        self.natural_wind = (body[10] & 0x40) > 0
        self.full_dust = (body[13] & 0x20) > 0
        self.comfort_mode = (
            (body[14] & 0x1) > 0 if len(body) > CONFORT_MODE_MIN_LENGTH else False
        )


class XA1MessageBody(MessageBody):
    """AC A1 message body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize AC A1 message body."""
        super().__init__(body)
        if body[13] != MAX_BYTE_VALUE:
            temp_integer = int((body[13] - 50) / 2)
            temp_decimal = (
                ((body[18] & 0xF) * 0.1)
                if len(body) > TEMP_DECIMAL_MIN_BODY_LENGTH
                else 0
            )
            if body[13] > TEMP_NEG_VALUE:
                self.indoor_temperature = temp_integer + temp_decimal
            else:
                self.indoor_temperature = temp_integer - temp_decimal
        if body[14] == MAX_BYTE_VALUE:
            self.outdoor_temperature = None
        else:
            temp_integer = int((body[14] - 50) / 2)
            temp_decimal = (
                (((body[18] & 0xF0) >> 4) * 0.1)
                if len(body) > TEMP_DECIMAL_MIN_BODY_LENGTH
                else 0
            )
            if body[14] > TEMP_NEG_VALUE:
                self.outdoor_temperature = temp_integer + temp_decimal
            else:
                self.outdoor_temperature = temp_integer - temp_decimal
        self.indoor_humidity = body[17]


class XBXMessageBody(NewProtocolMessageBody):
    """AC BX message body."""

    def __init__(self, body: bytearray, bt: int) -> None:
        """Initialize AC BX message body."""
        super().__init__(body, bt)

        params = self.parse()
        if NewProtocolTags.indirect_wind in params:
            self.indirect_wind = (
                params[NewProtocolTags.indirect_wind][0] == INDIRECT_WIND_VALUE
            )
        if NewProtocolTags.indoor_humidity in params:
            self.indoor_humidity = params[NewProtocolTags.indoor_humidity][0]
        if NewProtocolTags.breezeless in params:
            self.breezeless = params[NewProtocolTags.breezeless][0] == 1
        if NewProtocolTags.screen_display in params:
            self.screen_display_alternate = (
                params[NewProtocolTags.screen_display][0] > 0
            )
            self.screen_display_new = True
        if NewProtocolTags.fresh_air_1 in params:
            self.fresh_air_1 = True
            data = params[NewProtocolTags.fresh_air_1]
            self.fresh_air_power = data[0] == INDIRECT_WIND_VALUE
            self.fresh_air_fan_speed = data[1]
        if NewProtocolTags.fresh_air_2 in params:
            self.fresh_air_2 = True
            data = params[NewProtocolTags.fresh_air_2]
            self.fresh_air_power = data[0] > 0
            self.fresh_air_fan_speed = data[1]

        if Capabilities.MODES in params:
            v = params[Capabilities.MODES][0]
            self.modes: dict[str, bool] = {}
            self.modes["heat"] = v in [1, 2, 4, 6, 7, 9]
            self.modes["cool"] = v != 2  # noqa: PLR2004
            self.modes["dry"] = v in [0, 1, 5, 6, 9]
            self.modes["auto"] = v in [0, 1, 2, 7, 8, 9]


class XC0MessageBody(MessageBody):
    """AC C0 message body."""

    def __init__(self, body: bytearray) -> None:
        """Initialize AC C0 message body."""
        super().__init__(body)
        self.power = (body[1] & 0x1) > 0
        self.mode = (body[2] & 0xE0) >> 5
        self.target_temperature = (
            (body[2] & 0x0F) + 16.0 + (0.5 if body[0x02] & 0x10 > 0 else 0.0)
        )
        self.fan_speed = body[3] & 0x7F
        self.swing_vertical = (body[7] & 0x0C) > 0
        self.swing_horizontal = (body[7] & 0x03) > 0
        self.boost_mode = ((body[8] & 0x20) > 0) or ((body[10] & 0x2) > 0)
        self.smart_eye = (body[8] & 0x40) > 0
        self.natural_wind = (body[9] & 0x2) > 0
        self.dry = (body[9] & 0x4) > 0
        self.eco_mode = (body[9] & 0x10) > 0
        self.aux_heating = (body[9] & 0x08) > 0
        self.temp_fahrenheit = (body[10] & 0x04) > 0
        self.sleep_mode = (body[10] & 0x01) > 0
        if body[11] != MAX_BYTE_VALUE:
            temp_integer = int((body[11] - 50) / 2)
            temp_decimal = (body[15] & 0x0F) * 0.1
            if body[11] > TEMP_NEG_VALUE:
                self.indoor_temperature = temp_integer + temp_decimal
            else:
                self.indoor_temperature = temp_integer - temp_decimal
        if body[12] == MAX_BYTE_VALUE:
            self.outdoor_temperature = None
        else:
            temp_integer = int((body[12] - 50) / 2)
            temp_decimal = ((body[15] & 0xF0) >> 4) * 0.1
            if body[12] > TEMP_NEG_VALUE:
                self.outdoor_temperature = temp_integer + temp_decimal
            else:
                self.outdoor_temperature = temp_integer - temp_decimal
        self.full_dust = (body[13] & 0x20) > 0
        self.screen_display = (
            (body[14] >> 4 & 0x7) != SCREEN_DISPLAY_BYTE_CHECK
        ) and self.power
        self.frost_protect = (
            (body[21] & 0x80) > 0 if len(body) >= FROST_PROTECT_C0_MIN_LENGTH else False
        )
        self.comfort_mode = (
            (body[22] & 0x1) > 0 if len(body) >= CONFORT_MODE_C0_MIN_LENGTH else False
        )


class XC1MessageBody(MessageBody):
    """AC C1 message body."""

    def __init__(self, body: bytearray, analysis_method: int = 3) -> None:
        """Initialize AC C1 message body."""
        super().__init__(body)
        if body[3] == XC1_SUBBODY_TYPE_44:
            self.total_energy_consumption = XC1MessageBody.parse_consumption(
                analysis_method,
                body[4],
                body[5],
                body[6],
                body[7],
            )
            self.current_energy_consumption = XC1MessageBody.parse_consumption(
                analysis_method,
                body[12],
                body[13],
                body[14],
                body[15],
            )
            self.realtime_power = XC1MessageBody.parse_power(
                analysis_method,
                body[16],
                body[17],
                body[18],
            )
        elif body[3] == XC1_SUBBODY_TYPE_40:
            pass

    @staticmethod
    def parse_value(byte: int) -> int:
        """AC C1 message body parse value."""
        return (byte >> 4) * 10 + (byte & 0x0F)

    @staticmethod
    def parse_power(analysis_method: int, byte1: int, byte2: int, byte3: int) -> float:
        """AC C1 message body parse power."""
        if analysis_method == PowerAnalysisMethod.TYPE_1:
            return (
                float(
                    XC1MessageBody.parse_value(byte1) * 10000
                    + XC1MessageBody.parse_value(byte2) * 100
                    + XC1MessageBody.parse_value(byte3),
                )
                / 10
            )
        if analysis_method == PowerAnalysisMethod.TYPE_2:
            return float((byte1 << 16) + (byte2 << 8) + byte3) / 10
        return float(byte1 * 10000 + byte2 * 100 + byte3) / 10

    @staticmethod
    def parse_consumption(
        analysis_method: int,
        byte1: int,
        byte2: int,
        byte3: int,
        byte4: int,
    ) -> float:
        """AC C1 message body parse consumption."""
        if analysis_method == PowerAnalysisMethod.TYPE_1:
            return (
                float(
                    XC1MessageBody.parse_value(byte1) * 1000000
                    + XC1MessageBody.parse_value(byte2) * 10000
                    + XC1MessageBody.parse_value(byte3) * 100
                    + XC1MessageBody.parse_value(byte4),
                )
                / 100
            )
        if analysis_method == PowerAnalysisMethod.TYPE_2:
            return float((byte1 << 32) + (byte2 << 16) + (byte3 << 8) + byte4) / 10
        return float(byte1 * 1000000 + byte2 * 10000 + byte3 * 100 + byte4) / 100


class XBBMessageBody(MessageBody):
    """AC BB message body."""

    def __init__(self, body: bytearray) -> None:
        """Initializ AC BB message body."""
        super().__init__(body)
        subprotocol_head = body[:6]
        subprotocol_body = body[6:]
        data_type = subprotocol_head[-1]
        subprotocol_body_len = len(subprotocol_body)
        if data_type in (ListTypes.X11, ListTypes.X20):
            self.power = (subprotocol_body[0] & 0x1) > 0
            self.dry = (subprotocol_body[0] & 0x10) > 0
            self.boost_mode = (subprotocol_body[0] & 0x20) > 0
            self.aux_heating = (subprotocol_body[1] & 0x40) > 0
            self.sleep_mode = (subprotocol_body[2] & 0x80) > 0
            try:
                self.mode = BB_AC_MODES.index(subprotocol_body[5] + 1)
            except ValueError:
                self.mode = 0
            self.target_temperature = (subprotocol_body[6] - 30) / 2
            self.fan_speed = subprotocol_body[7]
            self.timer = (
                (subprotocol_body[25] & 0x04) > 0
                if subprotocol_body_len > TIMER_MIN_SUBPROTOCOL_LENGTH
                else False
            )
            self.eco_mode = (
                (subprotocol_body[25] & 0x40) > 0
                if subprotocol_body_len > ECO_MODE_MIN_SUBPROTOCOL_LENGTH
                else False
            )
        elif data_type == ListTypes.X10:
            if subprotocol_body[8] & 0x80 == SUB_PROTOCOL_BODY_TEMP_CHECK:
                self.indoor_temperature = (
                    0 - (~(subprotocol_body[7] + subprotocol_body[8] * 256) + 1)
                    & 0xFFFF
                ) / 100
            else:
                self.indoor_temperature = (
                    subprotocol_body[7] + subprotocol_body[8] * 256
                ) / 100
            self.indoor_humidity = subprotocol_body[30]
            self.sn8_flag = subprotocol_body[80] == XBB_SN8_BYTE_FLAG
        elif data_type == ListTypes.X12:
            pass
        elif data_type == ListTypes.X30:
            if subprotocol_body[6] & 0x80 == SUB_PROTOCOL_BODY_TEMP_CHECK:
                self.outdoor_temperature = (
                    0 - (~(subprotocol_body[5] + subprotocol_body[6] * 256) + 1)
                    & 0xFFFF
                ) / 100
            else:
                self.outdoor_temperature = (
                    subprotocol_body[5] + subprotocol_body[6] * 256
                ) / 100
        elif data_type in (ListTypes.X13, ListTypes.X21):
            pass


class MessageACResponse(MessageResponse):
    """AC message response."""

    def __init__(self, message: bytearray, power_analysis_method: int = 3) -> None:
        """Initialize AC message response."""
        super().__init__(message)
        if self.message_type == MessageType.notify2 and self.body_type == ListTypes.A0:
            self.set_body(XA0MessageBody(super().body))
        elif (
            self.message_type == MessageType.notify1 and self.body_type == ListTypes.A1
        ):
            self.set_body(XA1MessageBody(super().body))
        elif self.message_type in [
            MessageType.query,
            MessageType.set,
            MessageType.notify2,
        ] and self.body_type in [ListTypes.B0, ListTypes.B1, ListTypes.B5]:
            self.set_body(XBXMessageBody(super().body, self.body_type))
        elif (
            self.message_type in [MessageType.query, MessageType.set]
            and self.body_type == ListTypes.C0
        ):
            self.set_body(XC0MessageBody(super().body))
        elif self.message_type == MessageType.query and self.body_type == ListTypes.C1:
            self.set_body(XC1MessageBody(super().body, power_analysis_method))
        elif (
            self.message_type
            in [MessageType.set, MessageType.query, MessageType.notify2]
            and self.body_type == ListTypes.BB
            and len(super().body) >= BB_MIN_BODY_LENGTH
        ):
            self.used_subprotocol = True
            self.set_body(XBBMessageBody(super().body))

        self.set_attr()
