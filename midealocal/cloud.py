"""Midea Local cloud."""

import base64
import json
import logging
import re
import time
from datetime import UTC, datetime
from http import HTTPStatus
from secrets import token_hex
from threading import Lock
from typing import Any, cast

import aiofiles
from aiohttp import ClientConnectionError, ClientSession
from commonregex import CommonRegex

from midealocal.exceptions import ElementMissing

from .security import (
    CloudSecurity,
    MeijuCloudSecurity,
    MideaAirSecurity,
    MSmartCloudSecurity,
)

SN8_MIN_SERIAL_LENGTH = 17

_LOGGER = logging.getLogger(__name__)

SUPPORTED_CLOUDS = {
    "美的美居": {
        "class_name": "MeijuCloud",
        "app_id": "900",
        "app_key": "46579c15",
        "login_key": "ad0ee21d48a64bf49f4fb583ab76e799",
        "iot_key": bytes.fromhex(
            format(9795516279659324117647275084689641883661667, "x"),
        ).decode(),
        "hmac_key": bytes.fromhex(
            format(117390035944627627450677220413733956185864939010425, "x"),
        ).decode(),
        "api_url": "https://mp-prod.smartmidea.net/mas/v5/app/proxy?alias=",
    },
    "MSmartHome": {
        "default": True,
        "class_name": "MSmartHomeCloud",
        "app_id": "1010",
        "app_key": "ac21b9f9cbfe4ca5a88562ef25e2b768",
        "iot_key": bytes.fromhex(format(7882822598523843940, "x")).decode(),
        "hmac_key": bytes.fromhex(
            format(117390035944627627450677220413733956185864939010425, "x"),
        ).decode(),
        "api_url": "https://mp-prod.appsmb.com/mas/v5/app/proxy?alias=",
    },
    "Midea Air": {
        "class_name": "MideaAirCloud",
        "app_id": "1117",
        "app_key": "ff0cf6f5f0c3471de36341cab3f7a9af",
        "api_url": "https://mapp.appsmb.com",  # codespell:ignore
    },
    "NetHome Plus": {
        "class_name": "MideaAirCloud",
        "app_id": "1017",
        "app_key": "3742e9e5842d4ad59c2db887e12449f9",
        "api_url": "https://mapp.appsmb.com",  # codespell:ignore
    },
    "Ariston Clima": {
        "class_name": "MideaAirCloud",
        "app_id": "1005",
        "app_key": "434a209a5ce141c3b726de067835d7f0",
        "api_url": "https://mapp.appsmb.com",  # codespell:ignore
    },
    "Toshiba Iolife": {
        "class_name": "ToshibaIOLife",
        "app_id": "1203",
        "app_key": "09c4d09f0da1513bb62dc7b6b0af9c11",
        "api_url": "https://toshiba-app.smartmidea.net",  # codespell:ignore
    },
}

DEFAULT_KEYS = {
    99: {
        "token": "ee755a84a115703768bcc7c6c13d3d629aa416f1e2fd798beb9f78cbb1381d09"
        "1cc245d7b063aad2a900e5b498fbd936c811f5d504b2e656d4f33b3bbc6d1da3",
        "key": "ed37bd31558a4b039aaf4e7a7a59aa7a75fd9101682045f69baf45d28380ae5c",
    },
}

PRESET_ACCOUNT_DATA = [
    39182118275972017797890111985649342047468653967530949796945843010512,
    29406100301096535908214728322278519471982973450672552249652548883645,
    39182118275972017797890111985649342050088014265865102175083010656997,
]


def get_default_cloud() -> str:
    """Return default cloud."""
    for key, value in SUPPORTED_CLOUDS.items():
        if cast(dict, value).get("default"):
            return key
    raise ElementMissing


def get_preset_account_cloud() -> dict[str, str]:
    """Return preset account data for cloud login."""
    username: str = bytes.fromhex(
        format((PRESET_ACCOUNT_DATA[0] ^ PRESET_ACCOUNT_DATA[1]), "X"),
    ).decode("ASCII")
    password: str = bytes.fromhex(
        format((PRESET_ACCOUNT_DATA[0] ^ PRESET_ACCOUNT_DATA[2]), "X"),
    ).decode("ASCII")

    return {
        "username": username,
        "password": password,
        "cloud_name": get_default_cloud(),
    }


block = "\u2588"


def _redact_data(data: str) -> str:
    """Redact sensitive data."""
    cr = CommonRegex(data)
    token_list = (
        getattr(cr, "phones", [])
        + getattr(cr, "emails", [])
        + getattr(cr, "credit_cards", [])
        + getattr(cr, "btc_addresses", [])
        + getattr(cr, "street_addresses", [])
    )
    for token in token_list:
        m = len(token)
        elm = r"\b" + token + r"\b"
        data = re.sub(elm, block * m, data)
    return data


class MideaCloud:
    """Midea Cloud."""

    def __init__(
        self,
        session: ClientSession,
        security: CloudSecurity,
        app_id: str,
        app_key: str,
        account: str,
        password: str,
        api_url: str,
    ) -> None:
        """Initialize Midea Cloud."""
        self._device_id = CloudSecurity.get_deviceid(account)
        self._session = session
        self._security = security
        self._api_lock = Lock()
        self._app_id = app_id
        self._app_key = app_key
        self._account = account
        self._password = password
        self._api_url = api_url
        self._access_token: str | None = None
        self._uid: str | None = None
        self._login_id = ""

    def _make_general_data(self) -> dict[Any, Any]:
        return {}

    async def _api_request(
        self,
        endpoint: str,
        data: dict[str, Any],
        header: dict[str, Any] | None = None,
    ) -> dict | None:
        header = header or {}
        if not data.get("reqId"):
            data.update({"reqId": token_hex(16)})
        if not data.get("stamp"):
            data.update(
                {"stamp": datetime.now(tz=UTC).strftime("%Y%m%d%H%M%S")},
            )
        random = str(int(time.time()))
        url = self._api_url + endpoint
        dump_data = json.dumps(data)
        sign = self._security.sign("", dump_data, random)
        header.update(
            {
                "content-type": "application/json; charset=utf-8",
                "secretVersion": "1",
                "sign": sign,
                "random": random,
            },
        )
        if self._uid is not None:
            header.update({"uid": self._uid})
        if self._access_token is not None:
            header.update({"accessToken": self._access_token})
        response: dict = {"code": -1}
        for _ in range(3):
            try:
                with self._api_lock:
                    r = await self._session.request(
                        "POST",
                        url,
                        headers=header,
                        data=dump_data,
                        timeout=10,
                    )
                    raw = await r.read()
                    _LOGGER.debug(
                        "Midea cloud API url: %s, data: %s, response: %s",
                        url,
                        _redact_data(str(data)),
                        _redact_data(str(raw)),
                    )
                    response = json.loads(raw)
                    break
            except (TimeoutError, ClientConnectionError, json.JSONDecodeError) as e:
                _LOGGER.warning(
                    "Midea cloud API error, url: %s, error: %s",
                    url,
                    repr(e),
                )
        if int(response["code"]) == 0 and "data" in response:
            return cast(dict, response["data"])
        return None

    async def _get_login_id(self) -> str | None:
        data = self._make_general_data()
        data.update({"loginAccount": f"{self._account}"})
        if response := await self._api_request(
            endpoint="/v1/user/login/id/get",
            data=data,
        ):
            return response.get("loginId")
        return None

    async def login(self) -> bool:
        """Authenticate."""
        raise NotImplementedError

    @staticmethod
    async def get_default_keys() -> dict[int, dict[str, Any]]:
        """Get default cloud keys."""
        return DEFAULT_KEYS

    async def get_cloud_keys(self, appliance_id: int) -> dict[int, dict[str, Any]]:
        """Get keys for device."""
        result = {}
        for method in [1, 2]:
            udp_id = self._security.get_udp_id(appliance_id, method)
            data = self._make_general_data()
            data.update({"udpid": udp_id})
            response = await self._api_request(
                endpoint="/v1/iot/secure/getToken",
                data=data,
            )
            _LOGGER.debug(
                "Response from get_keys() for appliance_id %s with method %s: %s",
                appliance_id,
                method,
                response,
            )
            if response and "tokenlist" in response:
                for token in response["tokenlist"]:
                    if token["udpId"] == udp_id:
                        result[method] = {
                            "token": token["token"].lower(),
                            "key": token["key"].lower(),
                        }
        return result

    @staticmethod
    async def get_cloud_servers() -> dict[int, str]:
        """Get available cloud servers."""
        return {i: cloud for i, cloud in enumerate(SUPPORTED_CLOUDS, start=1)}

    async def list_home(self) -> dict[int, Any] | None:
        """List homes."""
        return {1: "My home"}

    async def list_appliances(
        self,
        home_id: str | None,
    ) -> dict[int, dict[str, Any]] | None:
        """List appliances."""
        raise NotImplementedError

    async def get_device_info(self, device_id: int) -> dict[str, Any] | None:
        """Get device information."""
        if (response := await self.list_appliances(home_id=None)) and (
            int(device_id) in response
        ):
            return cast(dict, response[device_id])
        return None

    async def download_lua(
        self,
        path: str,
        device_type: int,
        sn: str,
        model_number: str | None = None,
        manufacturer_code: str = "0000",
    ) -> str | None:
        """Download lua integration."""
        raise NotImplementedError


class MeijuCloud(MideaCloud):
    """Meiju Cloud."""

    def __init__(
        self,
        cloud_name: str,
        session: ClientSession,
        account: str,
        password: str,
    ) -> None:
        """Initialize Meiju Cloud."""
        cloud_data = cast(dict[str, Any], SUPPORTED_CLOUDS[cloud_name])
        super().__init__(
            session=session,
            security=MeijuCloudSecurity(
                login_key=cloud_data["login_key"],
                iot_key=cloud_data["iot_key"],
                hmac_key=cloud_data["hmac_key"],
            ),
            app_id=cloud_data["app_id"],
            app_key=cloud_data["app_key"],
            account=account,
            password=password,
            api_url=cloud_data["api_url"],
        )

    async def login(self) -> bool:
        """Authenticate to Meiju Cloud."""
        if login_id := await self._get_login_id():
            self._login_id = login_id
            stamp = datetime.now(tz=UTC).strftime("%Y%m%d%H%M%S")
            data = {
                "iotData": {
                    "clientType": 1,
                    "deviceId": self._device_id,
                    "iampwd": self._security.encrypt_iam_password(
                        self._login_id,
                        self._password,
                    ),
                    "iotAppId": self._app_id,
                    "loginAccount": self._account,
                    "password": self._security.encrypt_password(
                        self._login_id,
                        self._password,
                    ),
                    "reqId": token_hex(16),
                    "stamp": stamp,
                },
                "data": {
                    "appKey": self._app_key,
                    "deviceId": self._device_id,
                    "platform": 2,
                },
                "timestamp": stamp,
                "stamp": stamp,
            }
            if response := await self._api_request(
                endpoint="/mj/user/login",
                data=data,
            ):
                self._access_token = response["mdata"]["accessToken"]
                self._security.set_aes_keys(
                    self._security.aes_decrypt_with_fixed_key(response["key"]),
                    b"0",
                )

                return True
        _LOGGER.warning("Meiju Cloud login failed for device %s", self._device_id)
        return False

    async def list_home(self) -> dict[int, Any] | None:
        """List Meiju Cloud homes."""
        if response := await self._api_request(
            endpoint="/v1/homegroup/list/get",
            data={},
        ):
            homes = {}
            for home in response["homeList"]:
                homes.update({int(home["homegroupId"]): home["name"]})
            return homes
        return None

    async def list_appliances(
        self,
        home_id: str | None,
    ) -> dict[int, dict[str, Any]] | None:
        """List Meiju Cloud devices."""
        data = {"homegroupId": home_id}
        if response := await self._api_request(
            endpoint="/v1/appliance/home/list/get",
            data=data,
        ):
            appliances = {}
            for home in response.get("homeList") or []:
                for room in home.get("roomList") or []:
                    for appliance in room.get("applianceList"):
                        try:
                            model_number = int(appliance.get("modelNumber", 0))
                        except (ValueError, TypeError):
                            model_number = 0
                        device_info = {
                            "name": appliance.get("name"),
                            "type": int(appliance.get("type"), 16),
                            "sn": (
                                self._security.aes_decrypt(appliance.get("sn"))
                                if appliance.get("sn")
                                else ""
                            ),
                            "sn8": appliance.get("sn8", "00000000"),
                            "model_number": model_number,
                            "manufacturer_code": appliance.get(
                                "enterpriseCode",
                                "0000",
                            ),
                            "model": appliance.get("productModel"),
                            "online": appliance.get("onlineStatus") == "1",
                        }
                        sn8 = device_info.get("sn8")
                        if not sn8 or len(sn8) == 0:
                            device_info["sn8"] = "00000000"
                        model = device_info.get("model")
                        if not model or len(model) == 0:
                            device_info["model"] = device_info["sn8"]
                        appliances[int(appliance["applianceCode"])] = device_info
            return appliances
        return None

    async def get_device_info(self, device_id: int) -> dict[str, Any] | None:
        """Get device information."""
        data = {"applianceCode": device_id}
        if response := await self._api_request(
            endpoint="/v1/appliance/info/get",
            data=data,
        ):
            try:
                model_number = int(response.get("modelNumber", 0))
            except (ValueError, TypeError):
                model_number = 0
            model_type = response.get("type")
            device_info = {
                "name": response.get("name"),
                "type": int(model_type, 16) if model_type else 0,
                "sn": self._security.aes_decrypt(response.get("sn") or ""),
                "sn8": response.get("sn8", "00000000"),
                "model_number": model_number,
                "manufacturer_code": response.get("enterpriseCode", "0000"),
                "model": response.get("productModel"),
                "online": response.get("onlineStatus") == "1",
            }
            sn8 = device_info.get("sn8")
            if sn8 is None or len(sn8) == 0:
                device_info["sn8"] = "00000000"
            model = device_info.get("model")
            if model is None or len(model) == 0:
                device_info["model"] = device_info["sn8"]
            return device_info
        return None

    async def download_lua(
        self,
        path: str,
        device_type: int,
        sn: str,
        model_number: str | None = None,  # noqa: ARG002
        manufacturer_code: str = "0000",
    ) -> str | None:
        """Download lua integration."""
        data = {
            "applianceSn": sn,
            "applianceType": f".{f'x{device_type:02x}'}",
            "applianceMFCode": manufacturer_code,
            "version": "0",
            "iotAppId": self._app_id,
        }
        fnm = None
        if response := await self._api_request(
            endpoint="/v1/appliance/protocol/lua/luaGet",
            data=data,
        ):
            res = await self._session.get(response["url"])
            if res.status == HTTPStatus.OK:
                lua = await res.text()
                if lua:
                    stream = (
                        'local bit = require "bit"\n'
                        + self._security.aes_decrypt_with_fixed_key(lua)
                    )
                    stream = stream.replace("\r\n", "\n")
                    fnm = f"{path}/{response['fileName']}"
                    async with aiofiles.open(fnm, "w") as fp:
                        await fp.write(stream)
        return str(fnm) if fnm else None


class MSmartHomeCloud(MideaCloud):
    """MSmart Home Cloud."""

    def __init__(
        self,
        cloud_name: str,
        session: ClientSession,
        account: str,
        password: str,
    ) -> None:
        """Initialize MSmart Cloud."""
        cloud_data = cast(dict[str, Any], SUPPORTED_CLOUDS[cloud_name])
        super().__init__(
            session=session,
            security=MSmartCloudSecurity(
                login_key=cloud_data["app_key"],
                iot_key=cloud_data["iot_key"],
                hmac_key=cloud_data["hmac_key"],
            ),
            app_id=cloud_data["app_id"],
            app_key=cloud_data["app_key"],
            account=account,
            password=password,
            api_url=cloud_data["api_url"],
        )
        self._auth_base = base64.b64encode(
            f"{self._app_key}:{cloud_data['iot_key']}".encode(
                "ascii",
            ),
        ).decode("ascii")

    def _make_general_data(self) -> dict[str, Any]:
        return {
            "src": self._app_id,
            "format": "2",
            "stamp": datetime.now(tz=UTC).strftime("%Y%m%d%H%M%S"),
            "platformId": "1",
            "deviceId": self._device_id,
            "reqId": token_hex(16),
            "uid": self._uid,
            "clientType": "1",
            "appId": self._app_id,
        }

    async def _api_request(
        self,
        endpoint: str,
        data: dict[str, Any],
        header: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        header = header or {}
        header.update(
            {"x-recipe-app": self._app_id, "authorization": f"Basic {self._auth_base}"},
        )

        return await super()._api_request(endpoint, data, header)

    async def _re_route(self) -> None:
        data = self._make_general_data()
        data.update({"userType": "0", "userName": f"{self._account}"})
        if (
            response := await self._api_request(
                endpoint="/v1/multicloud/platform/user/route",
                data=data,
            )
        ) and (api_url := response.get("masUrl")):
            self._api_url = api_url

    async def login(self) -> bool:
        """Authenticate to MSmart Cloud."""
        await self._re_route()
        if login_id := await self._get_login_id():
            self._login_id = login_id
            iot_data = self._make_general_data()
            iot_data.pop("uid")
            stamp = datetime.now(tz=UTC).strftime("%Y%m%d%H%M%S")
            iot_data.update(
                {
                    "iampwd": self._security.encrypt_iam_password(
                        self._login_id,
                        self._password,
                    ),
                    "loginAccount": self._account,
                    "password": self._security.encrypt_password(
                        self._login_id,
                        self._password,
                    ),
                    "stamp": stamp,
                },
            )
            data = {
                "iotData": iot_data,
                "data": {
                    "appKey": self._app_key,
                    "deviceId": self._device_id,
                    "platform": "2",
                },
                "stamp": stamp,
            }
            if response := await self._api_request(
                endpoint="/mj/user/login",
                data=data,
            ):
                self._uid = response["uid"]
                self._access_token = response["mdata"]["accessToken"]
                self._security.set_aes_keys(
                    response["accessToken"],
                    response["randomData"],
                )
                return True
        _LOGGER.warning("MSmartHome Cloud login failed for device %s", self._device_id)
        return False

    async def list_appliances(
        self,
        home_id: str | None,  # noqa: ARG002
    ) -> dict[int, dict[str, Any]] | None:
        """List MSmart Cloud Devices."""
        data = self._make_general_data()
        if response := await self._api_request(
            endpoint="/v1/appliance/user/list/get",
            data=data,
        ):
            appliances = {}
            for appliance in response["list"]:
                try:
                    model_number = int(appliance.get("modelNumber", 0))
                except ValueError:
                    model_number = 0
                device_info = {
                    "name": appliance.get("name"),
                    "type": int(appliance.get("type"), 16),
                    "sn": self._security.aes_decrypt(appliance.get("sn") or ""),
                    "sn8": "",
                    "model_number": model_number,
                    "manufacturer_code": appliance.get("enterpriseCode", "0000"),
                    "model": "",
                    "online": appliance.get("onlineStatus") == "1",
                }
                serial_num = device_info.get("sn")
                device_info["sn8"] = (
                    serial_num[9:17]
                    if (serial_num and len(serial_num) > SN8_MIN_SERIAL_LENGTH)
                    else ""
                )
                device_info["model"] = device_info.get("sn8")
                appliances[int(appliance["id"])] = device_info
            return appliances
        return None

    async def download_lua(
        self,
        path: str,
        device_type: int,
        sn: str,
        model_number: str | None = None,
        manufacturer_code: str = "0000",
    ) -> str | None:
        """Download lua integration."""
        data = {
            "clientType": "1",
            "appId": self._app_id,
            "format": "2",
            "deviceId": self._device_id,
            "iotAppId": self._app_id,
            "applianceMFCode": manufacturer_code,
            "applianceType": hex(device_type),
            "applianceSn": self._security.aes_encrypt_with_fixed_key(
                sn.encode("ascii"),
            ).hex(),
            "version": "0",
            "encryptedType ": "2",
        }
        if model_number is not None:
            data["modelNumber"] = model_number
        fnm = None
        if response := await self._api_request(
            endpoint="/v2/luaEncryption/luaGet",
            data=data,
        ):
            res = await self._session.get(response["url"])
            if res.status == HTTPStatus.OK:
                lua = await res.text()
                if lua:
                    stream = (
                        'local bit = require "bit"\n'
                        + self._security.aes_decrypt_with_fixed_key(lua)
                    )
                    stream = stream.replace("\r\n", "\n")
                    fnm = f"{path}/{response['fileName']}"
                    async with aiofiles.open(fnm, "w") as fp:
                        await fp.write(stream)
        return str(fnm) if fnm else None


class MideaAirCloud(MideaCloud):
    """Midea Air Cloud."""

    def __init__(
        self,
        cloud_name: str,
        session: ClientSession,
        account: str,
        password: str,
    ) -> None:
        """Initialize Midea Air Cloud."""
        cloud_data = cast(dict[str, Any], SUPPORTED_CLOUDS[cloud_name])
        super().__init__(
            session=session,
            security=MideaAirSecurity(login_key=cloud_data["app_key"]),
            app_id=cloud_data["app_id"],
            app_key=cloud_data["app_key"],
            account=account,
            password=password,
            api_url=cloud_data["api_url"],
        )
        self._session_id: str | None = None

    def _make_general_data(self) -> dict[str, Any]:
        data = {
            "src": self._app_id,
            "format": "2",
            "stamp": datetime.now(tz=UTC).strftime("%Y%m%d%H%M%S"),
            "deviceId": self._device_id,
            "reqId": token_hex(16),
            "clientType": "1",
            "appId": self._app_id,
        }
        if self._session_id is not None:
            data.update({"sessionId": self._session_id})
        return data

    async def _api_request(
        self,
        endpoint: str,
        data: dict[str, Any],
        header: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        header = header or {}
        url = self._api_url + endpoint

        sign = self._security.sign(url, data, "")
        data.update({"sign": sign})
        if self._uid is not None:
            header.update({"uid": self._uid})
        if self._access_token is not None:
            header.update({"accessToken": self._access_token})
        response: dict = {"errorCode": -1}
        for _ in range(3):
            try:
                with self._api_lock:
                    r = await self._session.request(
                        "POST",
                        url,
                        headers=header,
                        data=data,
                        timeout=10,
                    )
                    raw = await r.read()
                    _LOGGER.debug(
                        "Midea cloud API url: %s, data: %s, response: %s",
                        url,
                        data,
                        raw,
                    )
                    response = json.loads(raw)
                    break
            except (TimeoutError, ClientConnectionError, json.JSONDecodeError) as e:
                _LOGGER.warning(
                    "Midea cloud API error, url: %s, error: %s",
                    url,
                    repr(e),
                )
        if int(response["errorCode"]) == 0 and "result" in response:
            return cast(dict[str, Any], response["result"])
        return None

    async def login(self) -> bool:
        """Authenticate to Midea Air Cloud."""
        if login_id := await self._get_login_id():
            self._login_id = login_id
            data = self._make_general_data()
            data.update(
                {
                    "loginAccount": self._account,
                    "password": self._security.encrypt_password(
                        self._login_id,
                        self._password,
                    ),
                },
            )
            if response := await self._api_request(
                endpoint="/v1/user/login",
                data=data,
            ):
                self._access_token = response["accessToken"]
                self._uid = response["userId"]
                self._session_id = response["sessionId"]
                return True
        _LOGGER.warning("Midea Air Cloud login failed for device %s", self._device_id)
        return False

    async def list_appliances(
        self,
        home_id: str | None,  # noqa: ARG002
    ) -> dict[int, dict[str, Any]] | None:
        """List Midea Air devices."""
        data = self._make_general_data()
        if response := await self._api_request(
            endpoint="/v1/appliance/user/list/get",
            data=data,
        ):
            appliances = {}
            for appliance in response["list"]:
                try:
                    model_number = int(appliance.get("modelNumber", 0))
                except ValueError:
                    model_number = 0
                device_info = {
                    "name": appliance.get("name"),
                    "type": int(appliance.get("type"), 16),
                    "sn": appliance.get("sn"),
                    "sn8": "",
                    "model_number": model_number,
                    "manufacturer_code": appliance.get("enterpriseCode", "0000"),
                    "model": "",
                    "online": appliance.get("onlineStatus") == "1",
                }
                serial_num = device_info.get("sn")
                device_info["sn8"] = (
                    serial_num[9:17]
                    if (serial_num and len(serial_num) > SN8_MIN_SERIAL_LENGTH)
                    else ""
                )
                device_info["model"] = device_info.get("sn8")
                appliances[int(appliance["id"])] = device_info
            return appliances
        return None


class ToshibaIOLife(MideaAirCloud):
    """Toshiba IOLife"""

    async def list_appliance_types(
        self,
    ) -> dict[int, dict[str, Any]] | None:
        """List Toshiba IOLife device types"""
        data = self._make_general_data()
        data.update({"applianceType": "0xFF"})
        if response := await self._api_request(
            endpoint="/v1/appliance/type/list/get",
            data=data,
        ):
            return data
        return None

    async def list_appliances(
        self,
    ) -> dict[int, dict[str, Any]] | None:
        """Get Toshiba IOLife devices."""
        data = self._make_general_data()
        if response := await self._api_request(
            endpoint="/v2/appliance/user/list/get",
            data=data,
        ):
            appliances = {}
            for appliance in response["list"]:
                try:
                    model_number = int(appliance.get("modelNumber", 0))
                except ValueError:
                    model_number = 0

                # Skip virtual batch devices:
                if appliance.get("type") == "0x_BATCH_AC":
                    continue
                if appliance.get("id") == "virtual_ag_0xAC":
                    continue
                device_info = {
                    "name": appliance.get("name"),
                    "type": int(appliance.get("type"), 16),
                    "sn": appliance.get("sn"),
                    "sn8": "",
                    "model_number": model_number,
                    "manufacturer_code": appliance.get("enterpriseCode", "0000"),
                    "model": "",
                    "online": appliance.get("onlineStatus") == "1",
                }
                serial_num = device_info.get("sn")
                device_info["sn8"] = (
                    serial_num[9:17]
                    if (serial_num and len(serial_num) > SN8_MIN_SERIAL_LENGTH)
                    else ""
                )
                device_info["model"] = device_info.get("sn8")
                appliances[int(appliance["id"])] = device_info
            return appliances
        return None

    # FIXME: this isn't working:
    async def download_lua(
        self,
        path: str,
        device_type: int,
        sn: str,
        model_number: str | None = None,
        manufacturer_code: str = "0000",
    ) -> str | None:
        """Download lua integration."""
        data = self._make_general_data()
        data.update(
            {
                "appId": self._app_id,
                "appKey": self._app_key,
                "applianceMFCode": manufacturer_code,
                "applianceType": hex(device_type),
                "modelNumber": "",
                "applianceSn": sn,
                "version": "0",
            }
        )
        if model_number is not None:
            data["modelNumber"] = model_number
        fnm = None
        if response := await self._api_request(
            endpoint="/v1/appliance/protocol/lua/luaGet",  # FIXME: Wrong URL?
            data=data,
        ):
            res = await self._session.get(response["url"])
            if res.status == HTTPStatus.OK:
                lua = await res.text()
                if lua:
                    stream = (
                        'local bit = require "bit"\n'
                        + self._security.aes_decrypt_with_fixed_key(lua)
                    )
                    stream = stream.replace("\r\n", "\n")
                    fnm = f"{path}/{response['fileName']}"
                    async with aiofiles.open(fnm, "w") as fp:
                        await fp.write(stream)
        return str(fnm) if fnm else None


def get_midea_cloud(
    cloud_name: str,
    session: ClientSession,
    account: str,
    password: str,
) -> MideaCloud:
    """Get Midea Cloud implementation."""
    if cloud_name not in SUPPORTED_CLOUDS:
        raise ElementMissing(
            f"Unsupported Cloud specified: {cloud_name}",
        )

    cloud_data = cast(dict[str, Any], SUPPORTED_CLOUDS[cloud_name])
    return cast(
        MideaCloud,
        globals()[cloud_data["class_name"]](
            cloud_name=cloud_name,
            session=session,
            account=account,
            password=password,
        ),
    )
