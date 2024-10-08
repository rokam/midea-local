"""Midea local x26 device."""

import logging
import math
from enum import StrEnum
from typing import Any, ClassVar

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice

from .message import Message26Response, MessageQuery, MessageSet

_LOGGER = logging.getLogger(__name__)

DIRECTION_MIN_VALUE = 60
DIRECTION_MAX_VALUE = 120


class DeviceAttributes(StrEnum):
    """Midea x26 device attributes."""

    main_light = "main_light"
    night_light = "night_light"
    mode = "mode"
    direction = "direction"
    current_humidity = "current_humidity"
    current_radar = "current_radar"
    current_temperature = "current_temperature"


class Midea26Device(MideaDevice):
    """Midea x26 device."""

    _modes: ClassVar[list[str]] = [
        "Off",
        "Heat(high)",
        "Heat(low)",
        "Bath",
        "Blow",
        "Ventilation",
        "Dry",
    ]
    _directions: ClassVar[list[str]] = [
        "60",
        "70",
        "80",
        "90",
        "100",
        "110",
        "120",
        "Oscillate",
    ]

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
        """Initialize Midea x26 device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.X26,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.main_light: False,
                DeviceAttributes.night_light: False,
                DeviceAttributes.mode: None,
                DeviceAttributes.direction: None,
                DeviceAttributes.current_humidity: None,
                DeviceAttributes.current_radar: None,
                DeviceAttributes.current_temperature: None,
            },
        )
        self._fields: dict[str, Any] = {}

    @staticmethod
    def _convert_to_midea_direction(direction: str) -> int:
        if direction == "Oscillate":
            result = 0xFD
        else:
            result = (
                Midea26Device._directions.index(direction) * 10 + 60
                if direction in Midea26Device._directions
                else 0xFD
            )
        return result

    @staticmethod
    def _convert_from_midea_direction(direction: int) -> int:
        if direction > DIRECTION_MAX_VALUE or direction < DIRECTION_MIN_VALUE:
            result = 7
        else:
            result = math.floor((direction - 60 + 5) / 10)
        return result

    @property
    def preset_modes(self) -> list[str]:
        """Midea x26 device preset modes."""
        return Midea26Device._modes

    @property
    def directions(self) -> list[str]:
        """Midea x26 device directions."""
        return Midea26Device._directions

    def build_query(self) -> list[MessageQuery]:
        """Midea x26 device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea x26 device process message."""
        message = Message26Response(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        self._fields = message.fields
        for status in self._attributes:
            if hasattr(message, str(status)):
                value = getattr(message, str(status))
                if status == DeviceAttributes.mode:
                    self._attributes[status] = Midea26Device._modes[value]
                elif status == DeviceAttributes.direction:
                    self._attributes[status] = Midea26Device._directions[
                        self._convert_from_midea_direction(value)
                    ]
                else:
                    self._attributes[status] = value
                new_status[str(status)] = self._attributes[status]
        return new_status

    def set_attribute(self, attr: str, value: bool | int | str) -> None:
        """Midea x26 device set attribute."""
        if attr in [
            DeviceAttributes.main_light,
            DeviceAttributes.night_light,
            DeviceAttributes.mode,
            DeviceAttributes.direction,
        ]:
            message = MessageSet(self._message_protocol_version)
            message.fields = self._fields
            message.main_light = self._attributes[DeviceAttributes.main_light]
            message.night_light = self._attributes[DeviceAttributes.night_light]
            message.mode = Midea26Device._modes.index(
                self._attributes[DeviceAttributes.mode],
            )
            message.direction = self._convert_to_midea_direction(
                self._attributes[DeviceAttributes.direction],
            )
            if attr in [DeviceAttributes.main_light, DeviceAttributes.night_light]:
                message.main_light = False
                message.night_light = False
                setattr(message, str(attr), value)
            elif attr == DeviceAttributes.mode:
                message.mode = Midea26Device._modes.index(str(value))
            elif attr == DeviceAttributes.direction:
                message.direction = self._convert_to_midea_direction(str(value))
            self.build_send(message)


class MideaAppliance(Midea26Device):
    """Midea x26 appliance."""
