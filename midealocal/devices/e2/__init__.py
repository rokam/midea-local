"""Midea Local E2 device."""

import json
import logging
from enum import IntEnum, StrEnum
from typing import Any

from midealocal.device import MideaDevice

from .message import (
    MessageE2Response,
    MessageNewProtocolSet,
    MessagePower,
    MessageQuery,
    MessageSet,
)


class OldProtocol(StrEnum):
    """Old protocol."""

    auto = "auto"
    true = "true"
    false = "false"


class E2SubType(IntEnum):
    """E2 sub type."""

    T82 = 82
    T85 = 85
    T36353 = 36353


_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    """Midea E2 device attributes."""

    power = "power"
    heating = "heating"
    keep_warm = "keep_warm"
    protection = "protection"
    current_temperature = "current_temperature"
    target_temperature = "target_temperature"
    whole_tank_heating = "whole_tank_heating"
    variable_heating = "variable_heating"
    heating_time_remaining = "heating_time_remaining"
    water_consumption = "water_consumption"
    heating_power = "heating_power"


class MideaE2Device(MideaDevice):
    """Midea E2 device."""

    def __init__(
        self,
        name: str,
        device_id: int,
        ip_address: str,
        port: int,
        token: str,
        key: str,
        protocol: int,
        model: str,
        subtype: int,
        customize: str,
    ) -> None:
        """Initialize Midea E2 device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=0xE2,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            protocol=protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.power: False,
                DeviceAttributes.heating: False,
                DeviceAttributes.keep_warm: False,
                DeviceAttributes.protection: False,
                DeviceAttributes.current_temperature: None,
                DeviceAttributes.target_temperature: 40,
                DeviceAttributes.whole_tank_heating: False,
                DeviceAttributes.variable_heating: False,
                DeviceAttributes.heating_time_remaining: 0,
                DeviceAttributes.water_consumption: None,
                DeviceAttributes.heating_power: None,
            },
        )
        self._default_old_protocol = OldProtocol.auto
        self._old_protocol = self._default_old_protocol
        self.set_customize(customize)

    def _normalize_old_protocol(self, value: str | bool | int) -> OldProtocol:
        if isinstance(value, str):
            return_value = OldProtocol(value)
            if return_value == OldProtocol.auto:
                result = (
                    self.subtype <= E2SubType.T82
                    or self.subtype in [E2SubType.T85, E2SubType.T36353],
                )
                return_value = OldProtocol.true if result else OldProtocol.false
        if isinstance(value, bool | int):
            return_value = OldProtocol.true if value else OldProtocol.false
        return return_value

    def build_query(self) -> list[MessageQuery]:
        """Midea E2 device build query."""
        return [MessageQuery(self._protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea E2 device process message."""
        message = MessageE2Response(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        for status in self._attributes:
            if hasattr(message, str(status)):
                self._attributes[status] = getattr(message, str(status))
                new_status[str(status)] = getattr(message, str(status))
        return new_status

    def make_message_set(self) -> MessageSet:
        """Midea E2 device make message set."""
        message = MessageSet(self._protocol_version)
        message.protection = self._attributes[DeviceAttributes.protection]
        message.whole_tank_heating = self._attributes[
            DeviceAttributes.whole_tank_heating
        ]
        message.target_temperature = self._attributes[
            DeviceAttributes.target_temperature
        ]
        message.variable_heating = self._attributes[DeviceAttributes.variable_heating]
        return message

    def set_attribute(self, attr: str, value: bool | int | str) -> None:
        """Midea E2 device set attribute."""
        message: MessagePower | MessageSet | MessageNewProtocolSet | None = None
        if attr not in [
            DeviceAttributes.heating,
            DeviceAttributes.keep_warm,
            DeviceAttributes.current_temperature,
        ]:
            old_protocol = self._normalize_old_protocol(self._old_protocol)
            if attr == DeviceAttributes.power:
                message = MessagePower(self._protocol_version)
                message.power = bool(value)
            elif old_protocol == OldProtocol.true:
                message = self.make_message_set()
                setattr(message, str(attr), value)
            else:
                message = MessageNewProtocolSet(self._protocol_version)
                setattr(message, str(attr), value)
            self.build_send(message)

    def set_customize(self, customize: str) -> None:
        """Midea E2 device set customize."""
        self._old_protocol = self._default_old_protocol
        if customize and len(customize) > 0:
            try:
                params = json.loads(customize)
                if params and "old_protocol" in params:
                    self._old_protocol = self._normalize_old_protocol(
                        params["old_protocol"],
                    )
            except Exception:
                _LOGGER.exception("[%s] Set customize error", self.device_id)
            self.update_all({"old_protocol": self._old_protocol})


class MideaAppliance(MideaE2Device):
    """Midea E2 appliance."""
