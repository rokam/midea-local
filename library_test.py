"""Test script for midea-local library."""

import asyncio
import json
import logging
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

import aiohttp
from colorlog import ColoredFormatter

from midealocal.cloud import SUPPORTED_CLOUDS, get_midea_cloud
from midealocal.devices import device_selector
from midealocal.discover import discover

_LOGGER = logging.getLogger("library_test")


def get_arguments() -> tuple[ArgumentParser, Namespace]:
    """Get parsed passed in arguments."""
    parser = ArgumentParser(description="midea-local library test")
    parser.add_argument(
        "--username",
        "-u",
        type=str,
        help="Set Cloud username",
    )
    parser.add_argument("--password", "-p", type=str, help="Set Cloud password")
    parser.add_argument(
        "--cloud_name",
        "-cn",
        type=str,
        help="Set Cloud name, options are: " + ", ".join(SUPPORTED_CLOUDS.keys()),
    )
    parser.add_argument(
        "--configfile",
        "-cf",
        type=str,
        help="Load options from JSON config file. \
        Command line options override those in the file.",
    )
    parser.add_argument("--ip", "-i", type=str, help="Device or broadcast IP Address.")

    arguments = parser.parse_args()
    # Re-parse the command line
    # taking the options in the optional JSON file as a basis
    if arguments.configfile and Path(arguments.configfile).exists():
        with Path(arguments.configfile).open(encoding="utf-8") as f:
            arguments = parser.parse_args(namespace=Namespace(**json.load(f)))

    return parser, arguments


async def main() -> None:
    """Run main."""
    parser, args = get_arguments()

    if not args.password or not args.username or not args.cloud_name:
        _LOGGER.error("All parameters needed: username, password and Cloud name")
        parser.print_help()
        sys.exit(1)

    _LOGGER.info("Starting network discovery...")
    devices = discover(ip_address=args.ip)
    _LOGGER.info("Devices: %s", devices)
    first_device = next(iter(devices.values()))
    _LOGGER.info("First device: %s", first_device)
    # The device type is in hexadecimal as in midealocal/devices/TYPE
    type_code = hex(first_device["type"])[2:]
    _LOGGER.info("First device type: %s", type_code)

    session = aiohttp.ClientSession()
    cloud = get_midea_cloud(
        session=session,
        cloud_name=args.cloud_name,
        account=args.username,
        password=args.password,
    )
    cloud_keys = {}
    if cloud:
        if not await cloud.login():
            msg = f"Cannot login into device {first_device['device_id']} \
[{first_device['ip_address']}]"
            _LOGGER.error(msg)
            await session.close()
            sys.exit(2)
        cloud_keys = await cloud.get_cloud_keys(first_device["device_id"])
    _LOGGER.info("Fist device Cloud info: %s", cloud_keys)

    token = ""
    key = ""
    for v in cloud_keys.values():
        token = v["token"]
        key = v["key"]

    _LOGGER.info("Fist device Cloud token: %s", token)
    _LOGGER.info("Fist device Cloud key:   %s", key)

    # Select the device
    ac = device_selector(
        name=type_code,
        device_id=first_device["device_id"],
        device_type=first_device["type"],
        ip_address=first_device["ip_address"],
        port=first_device["port"],
        token=token,
        key=key,
        device_protocol=first_device["protocol"],
        model=first_device["model"],
        subtype=0,
        customize="",
    )

    # Connect and authenticate
    ac.connect()

    # Getting the attributes
    _LOGGER.info("First device attributes: %s", ac.attributes)

    # Close session
    await session.close()


def set_logging() -> None:
    """Set logging levels."""
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("asyncio").setLevel(logging.INFO)
    logging.getLogger("charset_normalizer").setLevel(logging.INFO)
    fmt = (
        "%(asctime)s.%(msecs)03d %(levelname)s (%(threadName)s) [%(name)s] %(message)s"
    )
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


if __name__ == "__main__":
    set_logging()
    asyncio.run(main())
