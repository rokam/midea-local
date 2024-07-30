"""Midea local CLI."""

import asyncio
import contextlib
import inspect
import json
import logging
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, NoReturn

import aiohttp
import platformdirs
from colorlog import ColoredFormatter

from midealocal.cloud import SUPPORTED_CLOUDS, MideaCloud, get_midea_cloud
from midealocal.device import MideaDevice, ProtocolVersion
from midealocal.devices import device_selector
from midealocal.discover import discover
from midealocal.exceptions import ElementMissing
from midealocal.version import __version__

_LOGGER = logging.getLogger("cli")

LOG_FORMAT = (
    "%(asctime)s.%(msecs)03d %(levelname)s (%(threadName)s) [%(name)s] %(message)s"
)


class MideaCLI:
    """Midea CLI."""

    session: aiohttp.ClientSession
    namespace: Namespace

    async def _get_cloud(self) -> MideaCloud:
        """Get cloud instance."""
        if (
            not self.namespace.cloud_name
            or not self.namespace.username
            or not self.namespace.password
        ):
            raise ElementMissing("Missing required parameters for cloud request.")

        if not hasattr(self, "session"):
            self.session = aiohttp.ClientSession()

        return get_midea_cloud(
            cloud_name=self.namespace.cloud_name,
            session=self.session,
            account=self.namespace.username,
            password=self.namespace.password,
        )

    async def _get_keys(self, device_id: int) -> dict[int, dict[str, Any]]:
        cloud = await self._get_cloud()
        cloud_keys = await cloud.get_cloud_keys(device_id)
        default_keys = await cloud.get_default_keys()
        return {**cloud_keys, **default_keys}

    async def discover(self) -> MideaDevice | None:
        """Discover device information."""
        devices = discover(ip_address=self.namespace.host)

        if len(devices) == 0:
            _LOGGER.error("No devices found.")
            return None

        # Dump only basic device info from the base class
        _LOGGER.info("Found %d devices.", len(devices))
        for device in devices.values():
            keys = (
                {0: {"token": "", "key": ""}}
                if device["protocol"] != ProtocolVersion.V3
                else await self._get_keys(device["device_id"])
            )

            for key in keys.values():
                dev = device_selector(
                    name=device["device_id"],
                    device_id=device["device_id"],
                    device_type=device["type"],
                    ip_address=device["ip_address"],
                    port=device["port"],
                    token=key["token"],
                    key=key["key"],
                    protocol=device["protocol"],
                    model=device["model"],
                    subtype=0,
                    customize="",
                )
                _LOGGER.debug("Trying to connect with key: %s", key)
                if dev.connect():
                    _LOGGER.info("Found device:\n%s", dev.attributes)
                    return dev

                _LOGGER.debug("Unable to connect with key: %s", key)
        return None

    def message(self) -> None:
        """Load message into device."""
        device_type = int(self.namespace.message[2])

        device = device_selector(
            device_id=0,
            name="",
            device_type=device_type,
            ip_address="192.168.192.168",
            port=6664,
            protocol=ProtocolVersion.V2,
            model="0000",
            token="",
            key="",
            subtype=0,
            customize="",
        )

        result = device.process_message(self.namespace.message)

        _LOGGER.info("Parsed message: %s", result)

    def save(self) -> None:
        """Save credentials to config file."""
        data = {
            "username": self.namespace.username,
            "password": self.namespace.password,
            "cloud_name": self.namespace.cloud_name,
        }
        json_data = json.dumps(data)
        file = get_config_file_path(not self.namespace.user)
        with file.open(mode="w+", encoding="utf-8") as f:
            f.write(json_data)

    async def download(self) -> None:
        """Download lua from cloud."""
        device_type = int.from_bytes(self.namespace.device_type or bytearray())
        device_sn = str(self.namespace.device_sn)
        model: str | None = None

        if self.namespace.host:
            devices = discover(ip_address=self.namespace.host)

            if len(devices) == 0:
                _LOGGER.error("No devices found.")
                return

            _, device = devices.popitem()
            device_type = device["type"]
            device_sn = device["sn"]
            model = device["model"]

        cloud = await self._get_cloud()
        _LOGGER.debug("Try to authenticate to the cloud.")
        if not await cloud.login():
            _LOGGER.error("Failed to authenticate to the cloud.")
            return

        _LOGGER.debug("Download lua file for %s [%s]", device_sn, hex(device_type))
        lua = await cloud.download_lua(str(Path()), device_type, device_sn, model)
        _LOGGER.info("Downloaded lua file: %s", lua)

    async def set_attribute(self) -> None:
        """Set attribute for device."""
        device = await self.discover()
        if device is None:
            return

        _LOGGER.info(
            "Setting attribute %s for %s [%s]",
            self.namespace.attribute,
            device.device_id,
            device.device_type,
        )
        device.set_attribute(
            self.namespace.attribute,
            self._cast_attr_value(),
        )
        await asyncio.sleep(2)
        device.refresh_status(True)
        _LOGGER.info("New device status:\n%s", device.attributes)

    def _cast_attr_value(self) -> int | bool | str:
        if self.namespace.attr_type == "bool":
            return self.namespace.value not in ["false", "False", "0", ""]
        if self.namespace.attr_type == "int":
            return int(self.namespace.value)
        return str(self.namespace.value)

    def run(self, namespace: Namespace) -> None:
        """Do setup logging, validate args and execute the desired function."""
        self.namespace = namespace
        # Configure logging
        if self.namespace.debug:
            logging.basicConfig(level=logging.DEBUG)
            # Keep httpx as info level
            logging.getLogger("asyncio").setLevel(logging.INFO)
            logging.getLogger("charset_normalizer").setLevel(logging.INFO)
        else:
            logging.basicConfig(level=logging.INFO)
            # Set httpx to warning level
            logging.getLogger("asyncio").setLevel(logging.WARNING)
            logging.getLogger("charset_normalizer").setLevel(logging.WARNING)

        fmt = LOG_FORMAT
        colorfmt = f"%(log_color)s{fmt}%(reset)s"
        logging.getLogger().handlers[0].setFormatter(
            ColoredFormatter(
                colorfmt,
                datefmt="%Y-%m-%d %H:%M:%S",
                reset=True,
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red",
                },
            ),
        )

        with contextlib.suppress(KeyboardInterrupt):
            if inspect.iscoroutinefunction(self.namespace.func):
                asyncio.run(self.namespace.func())
            else:
                self.namespace.func()

        if hasattr(self, "session") and self.session:
            asyncio.run(self.session.close())


def get_config_file_path(relative: bool = False) -> Path:
    """Get the config file path."""
    local_path = Path("midea-local.json")
    if relative or local_path.exists():
        return local_path
    return platformdirs.user_config_path(appname="midea-local").joinpath(
        "midea-local.json",
    )


def main() -> NoReturn:
    """Launch main entry."""
    cli = MideaCLI()
    # Define the main parser to select subcommands
    parser = ArgumentParser(description="Command line utility for midea-local.")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"midea-local version: {__version__}",
    )
    subparsers = parser.add_subparsers(title="Command", dest="command", required=True)

    # Define some common arguments
    common_parser = ArgumentParser(add_help=False)
    common_parser.add_argument(
        "-d",
        "--debug",
        help="Enable debug logging.",
        action="store_true",
    )
    common_parser.add_argument(
        "--username",
        "-u",
        type=str,
        help="Set cloud username",
    )
    common_parser.add_argument(
        "--password",
        "-p",
        type=str,
        help="Set cloud password",
    )
    common_parser.add_argument(
        "--cloud-name",
        "-cn",
        type=str,
        help="Set Cloud name",
        choices=SUPPORTED_CLOUDS.keys(),
    )

    # Setup discover parser
    discover_parser = subparsers.add_parser(
        "discover",
        description="Discover device(s) on the local network.",
        parents=[common_parser],
    )
    discover_parser.add_argument(
        "--host",
        help="Hostname or IP address of a single device to discover.",
        default=None,
    )
    discover_parser.set_defaults(func=cli.discover)

    decode_msg_parser = subparsers.add_parser(
        "decode",
        description="Decode a message received to a device.",
        parents=[common_parser],
    )
    decode_msg_parser.add_argument(
        "message",
        help="Received message",
        type=bytes.fromhex,
    )
    decode_msg_parser.set_defaults(func=cli.message)

    save_parser = subparsers.add_parser(
        "save",
        description="Save config file with cloud parameters.",
        parents=[common_parser],
    )
    save_parser.add_argument(
        "--user",
        help="Save config file in your user config folder.",
        action="store_true",
    )
    save_parser.set_defaults(func=cli.save)

    download_parser = subparsers.add_parser(
        "download",
        description="Download lua scripts from cloud.",
        parents=[common_parser],
    )
    download_parser.add_argument(
        "--device-type",
        help="Device Type",
        type=bytes.fromhex,
    )
    download_parser.add_argument("--device-sn", help="Device SN")
    download_parser.add_argument(
        "--host",
        help="IP Address of the device.",
    )
    download_parser.set_defaults(func=cli.download)

    attribute_parser = subparsers.add_parser(
        "setattr",
        description="Set device attribute after discover.",
        parents=[common_parser],
    )
    attribute_parser.add_argument(
        "host",
        help="Hostname or IP address of a single device.",
        default=None,
    )
    attribute_parser.add_argument(
        "attribute",
        help="Attribute name.",
        default=None,
    )
    attribute_parser.add_argument(
        "value",
        help="Attribute value.",
        default=None,
    )
    attribute_parser.add_argument(
        "--attr-type",
        help="Attribute type.",
        type=str,
        default="int",
        choices=["bool", "int", "str"],
    )
    attribute_parser.set_defaults(func=cli.set_attribute)

    config = get_config_file_path()
    namespace = parser.parse_args()
    if config.exists():
        with config.open(encoding="utf-8") as f:
            config_data = json.load(f)
            for key, value in config_data.items():
                if not getattr(namespace, key):
                    setattr(namespace, key, value)

    # Run with args
    cli.run(namespace)
    sys.exit(0)


if __name__ == "__main__":
    main()
