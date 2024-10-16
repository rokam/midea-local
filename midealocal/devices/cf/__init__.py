"""Midea local CF device."""

import logging
from enum import StrEnum
from typing import Any

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice
from midealocal.exceptions import ValueWrongType

from .message import MessageCFResponse, MessageQuery, MessageSet

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    """Midea CF device attributes."""

    power = "power"
    mode = "mode"
    target_temperature = "target_temperature"
    aux_heating = "aux_heating"
    current_temperature = "current_temperature"
    max_temperature = "max_temperature"
    min_temperature = "min_temperature"


class MideaCFDevice(MideaDevice):
    """Midea CF device."""

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
        """Initialize Midea CF device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.CF,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.power: False,
                DeviceAttributes.mode: 0,
                DeviceAttributes.target_temperature: None,
                DeviceAttributes.aux_heating: False,
                DeviceAttributes.current_temperature: 0,
                DeviceAttributes.max_temperature: 55,
                DeviceAttributes.min_temperature: 5,
            },
        )

    def build_query(self) -> list[MessageQuery]:
        """Midea CF device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea CF device process message."""
        message = MessageCFResponse(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        for status in self._attributes:
            if hasattr(message, str(status)):
                self._attributes[status] = getattr(message, str(status))
                new_status[str(status)] = getattr(message, str(status))
        return new_status

    def set_target_temperature(
        self,
        target_temperature: float,
        mode: int | None,
        zone: int | None = None,  # noqa: ARG002
    ) -> None:
        """Midea CF device set target temperature."""
        message = MessageSet(self._message_protocol_version)
        message.power = True
        message.mode = self._attributes[DeviceAttributes.mode]
        message.target_temperature = target_temperature
        if mode is not None:
            message.mode = mode
        self.build_send(message)

    def set_attribute(self, attr: str, value: bool | int | str) -> None:
        """Midea CF device set attribute."""
        if not isinstance(value, bool):
            raise ValueWrongType("[cf] Expected bool")
        message = MessageSet(self._message_protocol_version)
        message.power = True
        message.mode = self._attributes[DeviceAttributes.mode]
        if attr == DeviceAttributes.power:
            message.power = value
        elif attr == DeviceAttributes.mode:
            message.power = True
            message.mode = value
        elif attr == DeviceAttributes.target_temperature:
            message.target_temperature = value
        elif attr == DeviceAttributes.aux_heating:
            message.aux_heating = value
        self.build_send(message)


class MideaAppliance(MideaCFDevice):
    """Midea CF appliance."""
