"""Midea local E3 device."""

import json
import logging
from enum import StrEnum
from typing import Any

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice

from .message import (
    MessageE3Response,
    MessageNewProtocolSet,
    MessagePower,
    MessageQuery,
    MessageSet,
)

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    """Midea E3 device attributes."""

    power = "power"
    burning_state = "burning_state"
    zero_cold_water = "zero_cold_water"
    protection = "protection"
    zero_cold_pulse = "zero_cold_pulse"
    smart_volume = "smart_volume"
    current_temperature = "current_temperature"
    target_temperature = "target_temperature"


class MideaE3Device(MideaDevice):
    """Midea E3 device."""

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
        """Initialize Midea E3 device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.E3,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.power: False,
                DeviceAttributes.burning_state: False,
                DeviceAttributes.zero_cold_water: False,
                DeviceAttributes.protection: False,
                DeviceAttributes.zero_cold_pulse: False,
                DeviceAttributes.smart_volume: False,
                DeviceAttributes.current_temperature: None,
                DeviceAttributes.target_temperature: 40,
            },
        )
        self._old_subtypes = [32, 33, 34, 35, 36, 37, 40, 43, 48, 49, 80]
        self._precision_halves: bool | None = None
        self._default_precision_halves = False
        self.set_customize(customize)

    @property
    def precision_halves(self) -> bool | None:
        """Midea E3 device precision halves."""
        return self._precision_halves

    def build_query(self) -> list[MessageQuery]:
        """Midea E3 device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea E3 device process message."""
        message = MessageE3Response(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        for status in self._attributes:
            if hasattr(message, str(status)):
                if self._precision_halves and status in [
                    DeviceAttributes.current_temperature,
                    DeviceAttributes.target_temperature,
                ]:
                    self._attributes[status] = getattr(message, str(status)) / 2
                else:
                    self._attributes[status] = getattr(message, str(status))
                new_status[str(status)] = self._attributes[status]

        return new_status

    def make_message_set(self) -> MessageSet:
        """Midea E3 device make message set."""
        message = MessageSet(self._message_protocol_version)
        message.zero_cold_water = self._attributes[DeviceAttributes.zero_cold_water]
        message.protection = self._attributes[DeviceAttributes.protection]
        message.zero_cold_pulse = self._attributes[DeviceAttributes.zero_cold_pulse]
        message.smart_volume = self._attributes[DeviceAttributes.smart_volume]
        message.target_temperature = self._attributes[
            DeviceAttributes.target_temperature
        ]
        return message

    def set_attribute(self, attr: str, value: bool | int | str) -> None:
        """Midea E3 device set attribute."""
        message: MessagePower | MessageSet | MessageNewProtocolSet | None = None
        if attr not in [
            DeviceAttributes.burning_state,
            DeviceAttributes.current_temperature,
            DeviceAttributes.protection,
        ]:
            if self._precision_halves and attr == DeviceAttributes.target_temperature:
                value = int(value * 2)
            if attr == DeviceAttributes.power:
                message = MessagePower(self._message_protocol_version)
                message.power = bool(value)
            elif self.subtype in self._old_subtypes:
                message = self.make_message_set()
                setattr(message, str(attr), value)
            else:
                message = MessageNewProtocolSet(self._message_protocol_version)
                message.key = str(attr)
                message.value = value
            self.build_send(message)

    def set_customize(self, customize: str) -> None:
        """Midea E3 device set customize."""
        self._precision_halves = self._default_precision_halves
        if customize and len(customize) > 0:
            try:
                params = json.loads(customize)
                if params and "precision_halves" in params:
                    self._precision_halves = params.get("precision_halves")
            except Exception:
                _LOGGER.exception("[%s] Set customize error", self.device_id)
            self.update_all({"precision_halves": self._precision_halves})


class MideaAppliance(MideaE3Device):
    """Midea E3 appliance."""
