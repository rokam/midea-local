"""Midea local FB device."""

import logging
from enum import StrEnum
from typing import Any, ClassVar

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice

from .message import MessageFBResponse, MessageQuery, MessageSet

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    """Midea FB device attributes."""

    power = "power"
    mode = "mode"
    heating_level = "heating_level"
    target_temperature = "target_temperature"
    current_temperature = "current_temperature"
    child_lock = "child_lock"


class MideaFBDevice(MideaDevice):
    """Midea FB device."""

    _modes: ClassVar[dict[int, str]] = {
        0x01: "Auto",
        0x02: "ECO",
        0x03: "Sleep",
        0x04: "Anti-freezing",
        0x05: "Comfort",
        0x06: "Constant-temperature",
        0x07: "Normal",
        0x08: "Fast-heating",
        0x10: "Standby",
    }

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
        """Initialize Midea FB device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.FB,
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
                DeviceAttributes.heating_level: 0,
                DeviceAttributes.target_temperature: None,
                DeviceAttributes.current_temperature: None,
                DeviceAttributes.child_lock: False,
            },
        )

    @property
    def modes(self) -> list[str]:
        """Midea FB device modes."""
        return list(MideaFBDevice._modes.values())

    def build_query(self) -> list[MessageQuery]:
        """Midea FB device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea FB device process message."""
        message = MessageFBResponse(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        for status in self._attributes:
            if hasattr(message, str(status)):
                value = getattr(message, str(status))
                if status == DeviceAttributes.mode:
                    if value in MideaFBDevice._modes:
                        self._attributes[status] = MideaFBDevice._modes.get(value)
                    else:
                        self._attributes[status] = None
                else:
                    self._attributes[status] = value
                new_status[str(status)] = self._attributes[status]
        return new_status

    def set_attribute(self, attr: str, value: str | int | bool) -> None:
        """Midea FB device set attribute."""
        if attr == DeviceAttributes.mode:
            message = MessageSet(self._message_protocol_version, self.subtype)
            if value in MideaFBDevice._modes.values():
                message.mode = list(MideaFBDevice._modes.keys())[
                    list(MideaFBDevice._modes.values()).index(str(value))
                ]
        else:
            message = MessageSet(self._message_protocol_version, self.subtype)
            setattr(message, str(attr), value)
        self.build_send(message)

    def set_target_temperature(
        self,
        target_temperature: float,
        mode: int | None,  # noqa: ARG002
        zone: int | None = None,  # noqa: ARG002
    ) -> None:
        """Midea FB device set target temperature."""
        message = MessageSet(self._message_protocol_version, self.subtype)
        setattr(message, DeviceAttributes.target_temperature, target_temperature)
        self.build_send(message)


class MideaAppliance(MideaFBDevice):
    """Midea FB appliance."""
