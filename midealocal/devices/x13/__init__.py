"""Midea local x13 device."""

import json
import logging
from enum import StrEnum
from typing import Any, ClassVar

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice

from .message import Message13Response, MessageQuery, MessageSet

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    """Midea x13 device attributes."""

    brightness = "brightness"
    color_temperature = "color_temperature"
    rgb_color = "rgb_color"
    effect = "effect"
    power = "power"


class Midea13Device(MideaDevice):
    """Midea x13 Device."""

    _effects: ClassVar[list[str]] = [
        "Manual",
        "Living",
        "Reading",
        "Mildly",
        "Cinema",
        "Night",
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
        customize: str,
    ) -> None:
        """Initialize Midea x13 Device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.X13,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.brightness: None,
                DeviceAttributes.color_temperature: None,
                DeviceAttributes.rgb_color: None,
                DeviceAttributes.effect: None,
                DeviceAttributes.power: False,
            },
        )
        self._color_temp_range: list[int] = []
        self._default_color_temp_range: list[int] = [2700, 6500]
        self.set_customize(customize)

    @property
    def effects(self) -> list[str]:
        """Midea x13 Device effects."""
        return Midea13Device._effects

    @property
    def color_temp_range(self) -> list[int]:
        """Midea x13 Device color temperature range."""
        return self._color_temp_range

    def kelvin_to_midea(self, kelvin: int) -> float:
        """Midea x13 Device kelvin to midea."""
        return round(
            (kelvin - self._color_temp_range[0])
            / (self._color_temp_range[1] - self._color_temp_range[0])
            * 255,
        )

    def midea_to_kelvin(self, midea: int) -> float:
        """Midea x13 Device midea to kelvin."""
        return (
            round((self._color_temp_range[1] - self._color_temp_range[0]) / 255 * midea)
            + self._color_temp_range[0]
        )

    def build_query(self) -> list[MessageQuery]:
        """Midea x13 Device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea x13 Device process message."""
        message = Message13Response(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status: dict[str, Any] = {}
        if hasattr(message, "control_success"):
            new_status = {"control_success": message.control_success}
            if message.control_success:
                self.refresh_status()
        else:
            for status in self._attributes:
                if hasattr(message, str(status)):
                    value = getattr(message, str(status))
                    if status == DeviceAttributes.effect:
                        self._attributes[status] = Midea13Device._effects[value]
                    elif status == DeviceAttributes.color_temperature:
                        self._attributes[status] = self.midea_to_kelvin(value)
                    else:
                        self._attributes[status] = value
                    new_status[str(status)] = self._attributes[status]
        return new_status

    def set_attribute(self, attr: str, value: str | int | bool) -> None:
        """Midea x13 Device set attribute."""
        if attr in [
            DeviceAttributes.brightness,
            DeviceAttributes.color_temperature,
            DeviceAttributes.effect,
            DeviceAttributes.power,
        ]:
            message = MessageSet(self._message_protocol_version)
            if attr == DeviceAttributes.effect and value in self._effects:
                setattr(message, str(attr), Midea13Device._effects.index(str(value)))
            elif attr == DeviceAttributes.color_temperature:
                setattr(message, str(attr), self.kelvin_to_midea(int(value)))
            else:
                setattr(message, str(attr), value)
            self.build_send(message)

    def set_customize(self, customize: str) -> None:
        """Midea x13 Device set customize."""
        self._color_temp_range = self._default_color_temp_range
        if customize and len(customize) > 0:
            try:
                params = json.loads(customize)
                if params and "color_temp_range_kelvin" in params:
                    self._color_temp_range = params.get("color_temp_range_kelvin")
            except Exception:
                _LOGGER.exception("[%s] Set customize error", self.device_id)
            self.update_all({"color_temp_range": self._color_temp_range})


class MideaAppliance(Midea13Device):
    """Midea x13 appliance."""
