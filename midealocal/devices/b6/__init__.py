"""Midea local B6 device."""

import json
import logging
from enum import StrEnum
from typing import Any

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice

from .message import MessageB6Response, MessageQuery, MessageSet

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    """Midea B6 device attributes."""

    power = "power"
    light = "light"
    mode = "mode"
    fan_level = "fan_level"
    fan_speed = "fan_speed"
    oilcup_full = "oilcup_full"
    cleaning_reminder = "cleaning_reminder"


class MideaB6Device(MideaDevice):
    """Midea B6 device."""

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
        """Initialize Midea B6 device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.B6,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.power: False,
                DeviceAttributes.light: None,
                DeviceAttributes.mode: None,
                DeviceAttributes.fan_level: 0,
                DeviceAttributes.fan_speed: 0,
                DeviceAttributes.oilcup_full: False,
                DeviceAttributes.cleaning_reminder: False,
            },
        )
        self._default_speeds = {0: "Off", 1: "Level 1", 2: "Level 2"}
        self._default_power_speed = 2
        self._power_speed = self._default_power_speed
        self._speeds = self._default_speeds
        self.set_customize(customize)

    @property
    def speed_count(self) -> int:
        """Midea B6 device speed count."""
        return len(self._speeds) - 1

    @property
    def preset_modes(self) -> list[str]:
        """Midea B6 device preset modes."""
        return list(self._speeds.values())

    def build_query(self) -> list[MessageQuery]:
        """Midea B6 device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea B6 device process message."""
        message = MessageB6Response(msg)
        self._message_protocol_version = message.protocol_version
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        for status in self._attributes:
            if hasattr(message, str(status)):
                value = getattr(message, str(status))
                if status == DeviceAttributes.fan_level:
                    if value in self._speeds:
                        self._attributes[DeviceAttributes.mode] = self._speeds.get(
                            value,
                        )
                        self._attributes[DeviceAttributes.fan_speed] = list(
                            self._speeds.keys(),
                        ).index(value)
                    else:
                        self._attributes[DeviceAttributes.mode] = None
                        self._attributes[DeviceAttributes.fan_speed] = 0
                    new_status[DeviceAttributes.mode.value] = self._attributes[
                        DeviceAttributes.mode
                    ]
                    new_status[DeviceAttributes.fan_speed.value] = self._attributes[
                        DeviceAttributes.fan_speed
                    ]
                self._attributes[status] = getattr(message, str(status))
                new_status[str(status)] = self._attributes[status]
        return new_status

    def set_attribute(self, attr: str, value: bool | int | str) -> None:
        """Midea B6 device set attribute."""
        message = None
        if attr == DeviceAttributes.fan_speed:
            if int(value) < len(self._speeds):
                message = MessageSet(self._message_protocol_version)
                message.fan_level = list(self._speeds.keys())[int(value)]
        elif attr == DeviceAttributes.mode:
            if value in self._speeds.values():
                message = MessageSet(self._message_protocol_version)
                message.fan_level = list(self._speeds.keys())[
                    list(self._speeds.values()).index(str(value))
                ]
            elif not value:
                message = MessageSet(self._message_protocol_version)
                message.power = False
        elif attr == DeviceAttributes.power:
            message = MessageSet(self._message_protocol_version)
            message.power = bool(value)
            message.fan_level = self._power_speed
        elif attr == DeviceAttributes.light:
            message = MessageSet(self._message_protocol_version)
            message.light = int(value)
        if message is not None:
            self.build_send(message)

    def turn_on(self, fan_speed: int | None = None, mode: str | None = None) -> None:
        """Midea B6 device turn on."""
        message = MessageSet(self._message_protocol_version)
        message.power = True
        if fan_speed is not None and fan_speed < len(self._speeds):
            message.fan_level = list(self._speeds.keys())[fan_speed]
        else:
            message.fan_level = self._power_speed
        if mode is not None in self._speeds.values():
            message.fan_level = list(self._speeds.keys())[
                list(self._speeds.values()).index(mode)
            ]
        self.build_send(message)

    def set_customize(self, customize: str) -> None:
        """Midea B6 device set customize."""
        self._speeds = self._default_speeds
        self._power_speed = self._default_power_speed
        if customize and len(customize) > 0:
            try:
                params = json.loads(customize)
                if params:
                    if "default_speed" in params:
                        self._power_speed = int(params.get("default_speed"))
                    if "speeds" in params:
                        self._speeds = {}
                        speeds = {}
                        for k, v in params.get("speeds").items():
                            speeds[int(k)] = v
                        keys = sorted(speeds.keys())
                        for k in keys:
                            self._speeds[k] = speeds[k]
                    self.update_all(
                        {"speeds": self._speeds, "default_speed": self._power_speed},
                    )
            except Exception:
                _LOGGER.exception("[%s] Set customize error", self.device_id)


class MideaAppliance(MideaB6Device):
    """Midea B6 appliance."""
