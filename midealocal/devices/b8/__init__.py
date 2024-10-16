"""Midea local B8 device."""

import logging
from enum import IntEnum
from typing import Any

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice

from .const import (
    B8CleanMode,
    B8ControlType,
    B8DeviceAttributes,
    B8ErrorCanFixDescription,
    B8ErrorType,
    B8FanLevel,
    B8FunctionType,
    B8MopState,
    B8Moviment,
    B8Speed,
    B8WaterLevel,
    B8WorkMode,
    B8WorkStatus,
)
from .message import (
    MessageB8Response,
    MessageQuery,
    MessageSet,
    MessageSetCommand,
)

_LOGGER = logging.getLogger(__name__)


class MideaB8Device(MideaDevice):
    """Midea B8 device."""

    def __init__(
        self,
        name: str,
        device_id: int,
        ip_address: str,
        port: int,
        token: str,
        key: str,
        device_protocol: ProtocolVersion,
        model: str,
        subtype: int,
        customize: str,  # noqa: ARG002
    ) -> None:
        """Initialize Midea B8 device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.B8,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                B8DeviceAttributes.WORK_STATUS: B8WorkStatus.NONE.name.lower(),
                B8DeviceAttributes.FUNCTION_TYPE: B8FunctionType.NONE.name.lower(),
                B8DeviceAttributes.CONTROL_TYPE: B8ControlType.NONE.name.lower(),
                B8DeviceAttributes.MOVE_DIRECTION: B8Moviment.NONE.name.lower(),
                B8DeviceAttributes.CLEAN_MODE: B8CleanMode.NONE.name.lower(),
                B8DeviceAttributes.FAN_LEVEL: B8FanLevel.OFF.name.lower(),
                B8DeviceAttributes.AREA: 0,
                B8DeviceAttributes.WATER_LEVEL: B8WaterLevel.OFF.name.lower(),
                B8DeviceAttributes.VOICE_VOLUME: 0,
                B8DeviceAttributes.MOP: B8MopState.OFF.name.lower(),
                B8DeviceAttributes.CARPET_SWITCH: False,
                B8DeviceAttributes.SPEED: B8Speed.HIGH.name.lower(),
                B8DeviceAttributes.HAVE_RESERVE_TASK: False,
                B8DeviceAttributes.BATTERY_PERCENT: 0,
                B8DeviceAttributes.WORK_TIME: 0,
                B8DeviceAttributes.UV_SWITCH: False,
                B8DeviceAttributes.WIFI_SWITCH: False,
                B8DeviceAttributes.VOICE_SWITCH: False,
                B8DeviceAttributes.COMMAND_SOURCE: False,
                B8DeviceAttributes.ERROR_TYPE: B8ErrorType.NO.name.lower(),
                B8DeviceAttributes.ERROR_DESC: B8ErrorCanFixDescription.NO.name.lower(),
                B8DeviceAttributes.DEVICE_ERROR: False,
                B8DeviceAttributes.BOARD_COMMUNICATION_ERROR: False,
                B8DeviceAttributes.LASER_SENSOR_SHELTER: False,
                B8DeviceAttributes.LASER_SENSOR_ERROR: False,
            },
        )

    def build_query(self) -> list[MessageQuery]:
        """Midea B8 device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea B8 device process message."""
        message = MessageB8Response(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        for status in self._attributes:
            if hasattr(message, str(status)):
                value = getattr(message, str(status))
                if isinstance(value, IntEnum):  # lowercase name for IntEnums
                    value = value.name.lower()
                self._attributes[status] = value
                new_status[str(status)] = self._attributes[status]
        return new_status

    def _gen_set_msg_default_values(self) -> MessageSet:
        msg = MessageSet(self._message_protocol_version)
        msg.clean_mode = B8CleanMode[
            self.attributes[B8DeviceAttributes.CLEAN_MODE].upper()
        ]
        msg.fan_level = B8FanLevel[
            self.attributes[B8DeviceAttributes.FAN_LEVEL].upper()
        ]
        msg.water_level = B8WaterLevel[
            self.attributes[B8DeviceAttributes.WATER_LEVEL].upper()
        ]
        msg.voice_volume = self.attributes[B8DeviceAttributes.VOICE_VOLUME]
        return msg

    def set_work_mode(self, work_mode: B8WorkMode) -> None:
        """Midea B8 device set work mode."""
        if work_mode == B8WorkMode.WORK:
            self.set_attribute(
                B8DeviceAttributes.CLEAN_MODE,
                self.attributes[B8DeviceAttributes.CLEAN_MODE],
            )
            return

        msg = MessageSetCommand(self._message_protocol_version, work_mode=work_mode)
        self.build_send(msg)

    def set_attribute(self, attr: str, value: bool | int | str) -> None:
        """Midea B8 device set attribute."""
        try:
            msg = self._gen_set_msg_default_values()
            if attr == B8DeviceAttributes.CLEAN_MODE:
                msg.clean_mode = B8CleanMode[str(value).upper()]
            elif attr == B8DeviceAttributes.FAN_LEVEL:
                msg.fan_level = B8FanLevel[str(value).upper()]
            elif attr == B8DeviceAttributes.WATER_LEVEL:
                msg.water_level = B8WaterLevel[str(value).upper()]
            elif attr == B8DeviceAttributes.VOICE_VOLUME:
                msg.voice_volume = int(value)

            if msg is not None:
                self.build_send(msg)
        except KeyError:
            _LOGGER.exception("Wrong value for attribute %s: %s", attr, value)


class MideaAppliance(MideaB8Device):
    """Midea B8 appliance."""
