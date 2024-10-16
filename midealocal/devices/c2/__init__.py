"""Midea local C2 device."""

import json
import logging
from enum import StrEnum
from typing import Any

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice

from .message import MessageC2Response, MessagePower, MessageQuery, MessageSet

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    """Midea C2 device attributes."""

    power = "power"
    child_lock = "child_lock"
    sensor_light = "sensor_light"
    foam_shield = "foam_shield"
    seat_status = "seat_status"
    lid_status = "lid_status"
    light_status = "light_status"
    dry_level = "dry_level"
    water_temp_level = "water_temp_level"
    seat_temp_level = "seat_temp_level"
    water_temperature = "water_temperature"
    seat_temperature = "seat_temperature"
    filter_life = "filter_life"


class MideaC2Device(MideaDevice):
    """Midea C2 device."""

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
        """Initialize Midea C2 device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.C2,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.power: False,
                DeviceAttributes.child_lock: False,
                DeviceAttributes.sensor_light: False,
                DeviceAttributes.foam_shield: False,
                DeviceAttributes.light_status: None,
                DeviceAttributes.seat_status: None,
                DeviceAttributes.lid_status: None,
                DeviceAttributes.dry_level: 0,
                DeviceAttributes.water_temp_level: 0,
                DeviceAttributes.seat_temp_level: 0,
                DeviceAttributes.water_temperature: None,
                DeviceAttributes.seat_temperature: None,
                DeviceAttributes.filter_life: None,
            },
        )
        self._max_dry_level: int | None = None
        self._max_water_temp_level: int | None = None
        self._max_seat_temp_level: int | None = None
        self._default_max_dry_level = 3
        self._default_max_water_temp_level = 5
        self._default_max_seat_temp_level = 5
        self.set_customize(customize)

    @property
    def max_dry_level(self) -> int | None:
        """Midea C2 device max dry level."""
        return self._max_dry_level

    @property
    def max_water_temp_level(self) -> int | None:
        """Midea C2 device max water temperature level."""
        return self._max_water_temp_level

    @property
    def max_seat_temp_level(self) -> int | None:
        """Midea C2 device max seat temperature level."""
        return self._max_seat_temp_level

    def build_query(self) -> list[MessageQuery]:
        """Midea C2 device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea C2 device process message."""
        message = MessageC2Response(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        for status in self._attributes:
            if hasattr(message, str(status)):
                self._attributes[status] = getattr(message, str(status))
                new_status[str(status)] = getattr(message, str(status))
        return new_status

    def set_attribute(self, attr: str, value: bool | int | str) -> None:
        """Midea C2 device set attribute."""
        message: MessagePower | MessageSet | None = None
        if attr == DeviceAttributes.power:
            message = MessagePower(self._message_protocol_version)
            message.power = bool(value)
        elif attr in [
            DeviceAttributes.child_lock,
            DeviceAttributes.sensor_light,
            DeviceAttributes.foam_shield,
            DeviceAttributes.water_temp_level,
            DeviceAttributes.seat_temp_level,
            DeviceAttributes.dry_level,
        ]:
            message = MessageSet(self._message_protocol_version)
            setattr(message, attr, value)
        if message:
            self.build_send(message)

    def set_customize(self, customize: str) -> None:
        """Midea C2 device set customize."""
        self._max_dry_level = self._default_max_dry_level
        self._max_water_temp_level = self._default_max_water_temp_level
        self._max_seat_temp_level = self._default_max_seat_temp_level
        if customize and len(customize) > 0:
            try:
                params = json.loads(customize)
                if params and "max_dry_level" in params:
                    self._max_dry_level = params.get("max_dry_level")
                if params and "max_water_temp_level" in params:
                    self._max_water_temp_level = params.get("max_water_temp_level")
                if params and "max_seat_temp_level" in params:
                    self._max_seat_temp_level = params.get("max_seat_temp_level")
            except Exception:
                _LOGGER.exception("[%s] Set customize error", self.device_id)
            self.update_all(
                {
                    "dry_level": {"max_dry_level": self._max_dry_level},
                    "water_temp_level": {
                        "max_water_temp_level": self._max_water_temp_level,
                    },
                    "seat_temp_level": {
                        "max_seat_temp_level": self._max_seat_temp_level,
                    },
                },
            )


class MideaAppliance(MideaC2Device):
    """Midea C2 appliance."""
