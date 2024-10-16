"""Midea local devices."""

from importlib import import_module
from typing import cast

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice


def device_selector(
    name: str,
    device_id: int,
    device_type: int,
    ip_address: str,
    port: int,
    token: str,
    key: str,
    device_protocol: ProtocolVersion,
    model: str,
    subtype: int,
    customize: str,
) -> MideaDevice:
    """Select and load device."""
    try:
        if device_type < DeviceType.A0:
            device_path = f".{f'x{device_type:02x}'}"
        else:
            device_path = f".{f'{device_type:02x}'}"
        module = import_module(device_path, __package__)
        device = module.MideaAppliance(
            name=name,
            device_id=device_id,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            customize=customize,
        )
    except ModuleNotFoundError:
        device = None
    return cast(MideaDevice, device)
