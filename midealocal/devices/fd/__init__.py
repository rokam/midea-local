"""Midea local FD device."""

import logging
from enum import StrEnum
from typing import Any, ClassVar

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice

from .message import MessageFDResponse, MessageQuery, MessageSet

_LOGGER = logging.getLogger(__name__)

MAX_SUBTYPE_OLD_SPEEDS = 5


class DeviceAttributes(StrEnum):
    """Midea FD device attributes."""

    power = "power"
    fan_speed = "fan_speed"
    prompt_tone = "prompt_tone"
    target_humidity = "target_humidity"
    current_humidity = "current_humidity"
    current_temperature = "current_temperature"
    tank = "tank"
    mode = "mode"
    screen_display = "screen_display"
    disinfect = "disinfect"


class MideaFDDevice(MideaDevice):
    """Midea FD device."""

    _modes: ClassVar[list[str]] = [
        "Manual",
        "Auto",
        "Continuous",
        "Living-Room",
        "Bed-Room",
        "Kitchen",
        "Sleep",
    ]
    _speeds_old: ClassVar[dict[int, str]] = {
        1: "Lowest",
        40: "Low",
        60: "Medium",
        80: "High",
        102: "Auto",
        127: "Off",
    }
    _speeds_new: ClassVar[dict[int, str]] = {
        1: "Lowest",
        39: "Low",
        59: "Medium",
        80: "High",
        101: "Auto",
        127: "Off",
    }
    _screen_displays: ClassVar[dict[int, str]] = {0: "Bright", 6: "Dim", 7: "Off"}
    _detect_modes: ClassVar[list[str]] = ["Off", "PM 2.5", "Methanal"]

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
        """Initialize Midea FD device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.FD,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.power: False,
                DeviceAttributes.fan_speed: None,
                DeviceAttributes.prompt_tone: True,
                DeviceAttributes.target_humidity: 60,
                DeviceAttributes.current_humidity: None,
                DeviceAttributes.current_temperature: None,
                DeviceAttributes.tank: 0,
                DeviceAttributes.mode: None,
                DeviceAttributes.screen_display: None,
                DeviceAttributes.disinfect: None,
            },
        )
        if self.subtype > MAX_SUBTYPE_OLD_SPEEDS:
            self._speeds = MideaFDDevice._speeds_new
        else:
            self._speeds = MideaFDDevice._speeds_old

    @property
    def modes(self) -> list[str]:
        """Midea FD device modes."""
        return list(MideaFDDevice._modes)

    @property
    def fan_speeds(self) -> list[str]:
        """Midea FD device fan speeds."""
        return list(self._speeds.values())

    @property
    def screen_displays(self) -> list[str]:
        """Midea FD device screen displays."""
        return list(MideaFDDevice._screen_displays.values())

    @property
    def detect_modes(self) -> list[str]:
        """Midea FD device detect modes."""
        return self._detect_modes

    def build_query(self) -> list[MessageQuery]:
        """Midea FD device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea FD device process message."""
        message = MessageFDResponse(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        for status in self._attributes:
            if hasattr(message, str(status)):
                value = getattr(message, str(status))
                if status == DeviceAttributes.mode:
                    if value <= len(MideaFDDevice._modes):
                        self._attributes[status] = MideaFDDevice._modes[value - 1]
                    else:
                        self._attributes[status] = None
                elif status == DeviceAttributes.fan_speed:
                    if value in self._speeds:
                        self._attributes[status] = self._speeds.get(value)
                    else:
                        self._attributes[status] = None
                elif status == DeviceAttributes.screen_display:
                    if value in MideaFDDevice._screen_displays:
                        self._attributes[status] = MideaFDDevice._screen_displays.get(
                            value,
                        )
                    else:
                        self._attributes[status] = None
                else:
                    self._attributes[status] = value
                new_status[str(status)] = self._attributes[status]
        return new_status

    def make_message_set(self) -> MessageSet:
        """Midea FD device make message set."""
        message = MessageSet(self._message_protocol_version)
        message.power = self._attributes[DeviceAttributes.power]
        message.prompt_tone = self._attributes[DeviceAttributes.prompt_tone]
        message.screen_display = self._attributes[DeviceAttributes.screen_display]
        message.disinfect = self._attributes[DeviceAttributes.disinfect]
        if self._attributes[DeviceAttributes.mode] in MideaFDDevice._modes:
            message.mode = (
                MideaFDDevice._modes.index(self._attributes[DeviceAttributes.mode]) + 1
            )
        else:
            message.mode = 1
        message.fan_speed = (
            40
            if self._attributes[DeviceAttributes.fan_speed] is None
            else list(self._speeds.keys())[
                list(self._speeds.values()).index(
                    self._attributes[DeviceAttributes.fan_speed],
                )
            ]
        )
        message.screen_display = (
            0
            if self._attributes[DeviceAttributes.screen_display] is None
            else list(MideaFDDevice._screen_displays.keys())[
                list(MideaFDDevice._screen_displays.values()).index(
                    self._attributes[DeviceAttributes.screen_display],
                )
            ]
        )
        return message

    def set_attribute(self, attr: str, value: str | int | bool) -> None:
        """Midea FD device set attribute."""
        if attr == DeviceAttributes.prompt_tone:
            self._attributes[DeviceAttributes.prompt_tone] = value
            self.update_all({DeviceAttributes.prompt_tone.value: value})
        else:
            message = self.make_message_set()
            if attr == DeviceAttributes.mode:
                if value in MideaFDDevice._modes:
                    message.mode = MideaFDDevice._modes.index(str(value)) + 1
            elif attr == DeviceAttributes.fan_speed:
                if value in self._speeds.values():
                    message.fan_speed = list(self._speeds.keys())[
                        list(self._speeds.values()).index(str(value))
                    ]
            elif attr == DeviceAttributes.screen_display:
                if value in MideaFDDevice._screen_displays.values():
                    message.screen_display = list(
                        MideaFDDevice._screen_displays.keys(),
                    )[list(MideaFDDevice._screen_displays.values()).index(str(value))]
                elif not value:
                    message.screen_display = 7
            else:
                setattr(message, str(attr), value)
            self.build_send(message)


class MideaAppliance(MideaFDDevice):
    """Midea FD appliance."""
