"""Midea local CE device."""

import json
import logging
from enum import StrEnum
from typing import Any, ClassVar

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice

from .message import MessageCEResponse, MessageQuery, MessageSet

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    """Midea CE device attributes."""

    power = "power"
    mode = "mode"
    child_lock = "child_lock"
    scheduled = "scheduled"
    fan_speed = "fan_speed"
    pm25 = "pm25"
    co2 = "co2"
    current_humidity = "current_humidity"
    current_temperature = "current_temperature"
    hcho = "hcho"
    link_to_ac = "link_to_ac"
    sleep_mode = "sleep_mode"
    eco_mode = "eco_mode"
    aux_heating = "aux_heating'"
    powerful_purify = "powerful_purify"
    filter_cleaning_reminder = "filter_cleaning_reminder"
    filter_change_reminder = "filter_change_reminder"
    error_code = "error_code"


class MideaCEDevice(MideaDevice):
    """Midea CE device."""

    _modes: ClassVar[list[str]] = ["Normal", "Sleep mode", "ECO mode"]

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
        customize: str,
    ) -> None:
        """Initialize Midea CE device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.CE,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.power: False,
                DeviceAttributes.mode: None,
                DeviceAttributes.child_lock: False,
                DeviceAttributes.scheduled: False,
                DeviceAttributes.fan_speed: 0,
                DeviceAttributes.pm25: None,
                DeviceAttributes.co2: None,
                DeviceAttributes.current_humidity: None,
                DeviceAttributes.current_temperature: None,
                DeviceAttributes.hcho: None,
                DeviceAttributes.link_to_ac: False,
                DeviceAttributes.sleep_mode: False,
                DeviceAttributes.eco_mode: False,
                DeviceAttributes.aux_heating: None,
                DeviceAttributes.powerful_purify: False,
                DeviceAttributes.filter_cleaning_reminder: False,
                DeviceAttributes.filter_change_reminder: False,
                DeviceAttributes.error_code: 0,
            },
        )
        self._default_speed_count = 7
        self._speed_count = self._default_speed_count
        self.set_customize(customize)

    @property
    def speed_count(self) -> int:
        """Midea CE device speed count."""
        return self._speed_count

    @property
    def preset_modes(self) -> list[str]:
        """Midea CE device preset modes."""
        return self._modes

    def build_query(self) -> list[MessageQuery]:
        """Midea CE device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea CE device process message."""
        message = MessageCEResponse(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        for status in self._attributes:
            if hasattr(message, str(status)):
                value = getattr(message, str(status))
                self._attributes[status] = value
                new_status[str(status)] = self._attributes[status]
        if self._attributes[DeviceAttributes.sleep_mode]:
            self._attributes[DeviceAttributes.mode] = "Sleep mode"
        elif self._attributes[DeviceAttributes.eco_mode]:
            self._attributes[DeviceAttributes.mode] = "ECO mode"
        else:
            self._attributes[DeviceAttributes.mode] = "None"
        new_status[DeviceAttributes.mode.value] = self._attributes[
            DeviceAttributes.mode
        ]
        return new_status

    def make_message_set(self) -> MessageSet:
        """Midea CE device make message set."""
        message = MessageSet(self._message_protocol_version)
        message.power = self._attributes[DeviceAttributes.power]
        message.fan_speed = self._attributes[DeviceAttributes.fan_speed]
        message.link_to_ac = self._attributes[DeviceAttributes.link_to_ac]
        message.sleep_mode = self._attributes[DeviceAttributes.sleep_mode]
        message.eco_mode = self._attributes[DeviceAttributes.eco_mode]
        message.aux_heating = self._attributes[DeviceAttributes.aux_heating]
        message.powerful_purify = self._attributes[DeviceAttributes.powerful_purify]
        message.scheduled = self._attributes[DeviceAttributes.scheduled]
        message.child_lock = self._attributes[DeviceAttributes.child_lock]
        return message

    def set_attribute(self, attr: str, value: str | int | bool) -> None:
        """Midea CE device set attribute."""
        message = self.make_message_set()
        if attr == DeviceAttributes.mode:
            message.sleep_mode = False
            message.eco_mode = False
            if value == "Sleep mode":
                message.sleep_mode = True
            elif value == "ECO mode":
                message.eco_mode = True
        else:
            setattr(message, str(attr), value)
        self.build_send(message)

    def set_customize(self, customize: str) -> None:
        """Midea CE device set customize."""
        self._speed_count = self._default_speed_count
        if customize and len(customize) > 0:
            try:
                params = json.loads(customize)
                if params and "speed_count" in params:
                    self._speed_count = params.get("speed_count")
            except Exception:
                _LOGGER.exception("[%s] Set customize error", self.device_id)
            self.update_all({"speed_count": self._speed_count})


class MideaAppliance(MideaCEDevice):
    """Midea CE appliance."""
