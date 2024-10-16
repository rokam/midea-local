"""Midea local EA device."""

import logging
from enum import StrEnum
from typing import Any, ClassVar

from midealocal.const import DeviceType, ProtocolVersion
from midealocal.device import MideaDevice

from .message import MessageEAResponse, MessageQuery

_LOGGER = logging.getLogger(__name__)


class DeviceAttributes(StrEnum):
    """Midea EA device attributes."""

    cooking = "cooking"
    keep_warm = "keep_warm"
    mode = "mode"
    time_remaining = "time_remaining"
    keep_warm_time = "keep_warm_time"
    top_temperature = "top_temperature"
    bottom_temperature = "bottom_temperature"
    progress = "progress"


class MideaEADevice(MideaDevice):
    """Midea EA device."""

    _mode_list: ClassVar[list[str]] = (
        [
            "smart",
            "reserve",
            "cook_rice",
            "fast_cook_rice",
            "standard_cook_rice",
            "gruel",
            "cook_congee",
            "stew_soup",
            "stewing",
            "heat_rice",
            "make_cake",
            "yoghourt",
            "soup_rice",
            "coarse_rice",
            "five_ceeals_rice",
            "eight_treasures_rice",
            "crispy_rice",
            "shelled_rice",
            "eight_treasures_congee",
            "infant_congee",
            "older_rice",
            "rice_soup",
            "rice_paste",
            "egg_custard",
            "warm_milk",
            "hot_spring_egg",
            "millet_congee",
            "firewood_rice",
            "few_rice",
            "red_potato",
            "corn",
            "quick_freeze_bun",
            "steam_ribs",
            "steam_egg",
            "coarse_congee",
            "steep_rice",
            "appetizing_congee",
            "corn_congee",
            "sprout_rice",
            "luscious_rice",
            "luscious_boiled",
            "fast_rice",
            "fast_boil",
            "bean_rice_congee",
            "fast_congee",
            "baby_congee",
            "cook_soup",
            "congee_coup",
            "steam_corn",
            "steam_red_potato",
            "boil_congee",
            "delicious_steam",
            "boil_egg",
            "rice_wine",
            "fruit_vegetable_paste",
            "vegetable_porridge",
            "pork_porridge",
            "fragrant_rice",
            "assorte_rice",
            "steame_fish",
            "baby_rice",
            "essence_rice",
            "fragrant_dense_congee",
            "one_two_cook",
            "original_steame",
            "hot_fast_rice",
            "online_celebrity_rice",
            "sushi_rice",
            "stone_bowl_rice",
            "no_water_treat",
            "keep_fresh",
            "low_sugar_rice",
            "black_buckwheat_rice",
            "resveratrol_rice",
            "yellow_wheat_rice",
            "green_buckwheat_rice",
            "roughage_rice",
            "millet_mixed_rice",
            "iron_pan_rice",
            "olla_pan_rice",
            "vegetable_rice",
            "baby_side",
            "regimen_congee",
            "earthen_pot_congee",
            "regimen_soup",
            "pottery_jar_soup",
            "canton_soup",
            "nutrition_stew",
            "northeast_stew",
            "uncap_boil",
            "trichromatic_coarse_grain",
            "four_color_vegetables",
            "egg",
            "chop",
        ]
        + ["unknown"] * 98
        + ["clean"]
        + ["unknown"] * 5
        + ["keep_warm"]
    )
    _progress: ClassVar[list[str]] = ["Idle", "Delay", "Cooking", "Keep-warm"]

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
        """Initialize Midea EA device."""
        super().__init__(
            name=name,
            device_id=device_id,
            device_type=DeviceType.EA,
            ip_address=ip_address,
            port=port,
            token=token,
            key=key,
            device_protocol=device_protocol,
            model=model,
            subtype=subtype,
            attributes={
                DeviceAttributes.cooking: False,
                DeviceAttributes.keep_warm: False,
                DeviceAttributes.mode: 0,
                DeviceAttributes.time_remaining: None,
                DeviceAttributes.top_temperature: None,
                DeviceAttributes.bottom_temperature: None,
                DeviceAttributes.keep_warm_time: None,
                DeviceAttributes.progress: "Unknown",
            },
        )

    def build_query(self) -> list[MessageQuery]:
        """Midea EA device build query."""
        return [MessageQuery(self._message_protocol_version)]

    def process_message(self, msg: bytes) -> dict[str, Any]:
        """Midea EA device process message."""
        message = MessageEAResponse(msg)
        _LOGGER.debug("[%s] Received: %s", self.device_id, message)
        new_status = {}
        for status in self._attributes:
            if hasattr(message, str(status)):
                value = getattr(message, str(status))
                if status == DeviceAttributes.progress:
                    if value < len(MideaEADevice._progress):
                        self._attributes[status] = MideaEADevice._progress[value]
                    else:
                        self._attributes[status] = "Unknown"
                elif status == DeviceAttributes.mode:
                    if value < len(MideaEADevice._mode_list):
                        self._attributes[status] = MideaEADevice._mode_list[value]
                    else:
                        self._attributes[status] = "Cloud"
                else:
                    self._attributes[status] = value
                new_status[str(status)] = self._attributes[status]
        return new_status

    def set_attribute(self, attr: str, value: bool | int | str) -> None:
        """Midea EA device set attribute."""


class MideaAppliance(MideaEADevice):
    """Midea EA appliance."""
