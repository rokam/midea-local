"""Midea local B3 device."""

import logging
from enum import StrEnum
from typing import Any, ClassVar

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice

from .message import MessageB3Response, MessageQuery

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    """Midea local B3 device attributes."""

    top_compartment_status = "top_compartment_status"
    top_compartment_mode = "top_compartment_mode"
    top_compartment_temperature = "top_compartment_temperature"
    top_compartment_remaining = "top_compartment_remaining"
    top_compartment_door = "top_compartment_door"
    top_compartment_preheating = "top_compartment_preheating"
    top_compartment_cooling = "top_compartment_cooling"
    middle_compartment_status = "middle_compartment_status"
    middle_compartment_mode = "middle_compartment_mode"
    middle_compartment_temperature = "middle_compartment_temperature"
    middle_compartment_remaining = "middle_compartment_remaining"
    middle_compartment_door = "middle_compartment_door"
    middle_compartment_preheating = "middle_compartment_preheating"
    middle_compartment_cooling = "middle_compartment_cooling"
    bottom_compartment_status = "bottom_compartment_status"
    bottom_compartment_mode = "bottom_compartment_mode"
    bottom_compartment_temperature = "bottom_compartment_temperature"
    bottom_compartment_remaining = "bottom_compartment_remaining"
    bottom_compartment_door = "bottom_compartment_door"
    bottom_compartment_preheating = "bottom_compartment_preheating"
    bottom_compartment_cooling = "bottom_compartment_cooling"
    lock = "lock"


class MideaB3Device(MideaDevice):
    """Midea local B3 device."""

    _status: ClassVar[dict[int, str]] = {
        0x00: "Off",
        0x01: "Standby",
        0x02: "Working",
        0x03: "Delay",
        0x04: "Finished",
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
        """Initialize Midea local B3 device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.B3,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.top_compartment_status: None,
                DeviceAttributes.top_compartment_mode: None,
                DeviceAttributes.top_compartment_temperature: None,
                DeviceAttributes.top_compartment_remaining: None,
                DeviceAttributes.top_compartment_door: False,
                DeviceAttributes.top_compartment_preheating: False,
                DeviceAttributes.top_compartment_cooling: False,
                DeviceAttributes.middle_compartment_status: None,
                DeviceAttributes.middle_compartment_mode: None,
                DeviceAttributes.middle_compartment_temperature: None,
                DeviceAttributes.middle_compartment_remaining: None,
                DeviceAttributes.middle_compartment_door: False,
                DeviceAttributes.middle_compartment_preheating: False,
                DeviceAttributes.middle_compartment_cooling: False,
                DeviceAttributes.bottom_compartment_status: None,
                DeviceAttributes.bottom_compartment_mode: None,
                DeviceAttributes.bottom_compartment_temperature: None,
                DeviceAttributes.bottom_compartment_remaining: None,
                DeviceAttributes.bottom_compartment_door: False,
                DeviceAttributes.bottom_compartment_preheating: False,
                DeviceAttributes.bottom_compartment_cooling: False,
                DeviceAttributes.lock: False,
            },
        )

    def build_query(self) -> list[MessageQuery]:
        """Midea local B3 device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea local B3 process message."""
        message = MessageB3Response(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        for status in self._attributes:
            if hasattr(message, str(status)):
                value = getattr(message, str(status))
                if status in [
                    DeviceAttributes.top_compartment_status,
                    DeviceAttributes.middle_compartment_status,
                    DeviceAttributes.bottom_compartment_status,
                ]:
                    if value in MideaB3Device._status:
                        self._attributes[status] = MideaB3Device._status.get(value)
                    else:
                        self._attributes[status] = None
                else:
                    self._attributes[status] = value
                new_status[str(status)] = self._attributes[status]
        return new_status

    def set_attribute(self, attr: str, value: bool | int | str) -> None:
        """Midea local B3 device set attribute."""


class MideaAppliance(MideaB3Device):
    """Midea local B3 appliance."""
