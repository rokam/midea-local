"""Test cloud."""

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import ClassVar
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, Mock

import pytest
from aiohttp import ClientConnectionError

from midealocal.cloud import (
    DEFAULT_KEYS,
    MeijuCloud,
    MideaAirCloud,
    MideaCloud,
    SmartHomeCloud,
    get_default_cloud,
    get_midea_cloud,
    get_preset_account_cloud,
)
from midealocal.exceptions import ElementMissing


class CloudTest(IsolatedAsyncioTestCase):
    """Cloud test case."""

    responses: ClassVar[dict[str, bytes]] = {}

    def setUp(self) -> None:
        """Set tests up."""
        file_path = Path(__file__)
        for file in Path.iterdir(Path(file_path.parent, "responses")):
            file_path = Path(file)
            with file_path.open(
                encoding="utf-8",
            ) as f:
                self.responses[file_path.name] = bytes(f.read(), encoding="utf-8")

    def test_get_midea_cloud(self) -> None:
        """Test get midea cloud."""
        session = AsyncMock()
        assert isinstance(get_midea_cloud("美的美居", session, "", ""), MeijuCloud)
        assert isinstance(
            get_midea_cloud("SmartHome", session, "", ""),
            SmartHomeCloud,
        )
        assert isinstance(get_midea_cloud("Midea Air", session, "", ""), MideaAirCloud)
        assert isinstance(
            get_midea_cloud("NetHome Plus", session, "", ""),
            MideaAirCloud,
        )
        assert isinstance(
            get_midea_cloud("Ariston Clima", session, "", ""),
            MideaAirCloud,
        )
        with pytest.raises(ElementMissing):
            get_midea_cloud("Invalid", session, "", "")

    async def test_get_default_cloud(self) -> None:
        """Test get default cloud name."""
        default_cloud = get_default_cloud()
        assert default_cloud == "SmartHome"

    async def test_get_cloud_servers(self) -> None:
        """Test get cloud servers."""
        servers = await MideaCloud.get_cloud_servers()
        assert len(servers.items()) == 5

    async def test_get_preset_account_cloud(self) -> None:
        """Test get preset cloud account."""
        credentials = get_preset_account_cloud()
        assert credentials["username"] == "c414e631394b8639@outlook.com"
        assert credentials["password"] == "a0d6e30c94b15"
        assert credentials["cloud_name"] == "SmartHome"

    async def test_midea_cloud_unimplemented(self) -> None:
        """Test unimplemented MideaCloud methods."""
        session = Mock()
        security = Mock()
        cloud = MideaCloud(
            session=session,
            security=security,
            app_id="appid",
            app_key="appkey",
            account="account",
            password="password",
            api_url="http://api.url/",
        )
        with pytest.raises(NotImplementedError):
            await cloud.login()
        with pytest.raises(NotImplementedError):
            await cloud.list_appliances(None)

    async def test_meijucloud_login_success(self) -> None:
        """Test MeijuCloud login."""
        session = Mock()
        response = Mock()
        response.read = AsyncMock(
            side_effect=[
                self.responses["cloud_login_id.json"],
                self.responses["meijucloud_login.json"],
            ],
        )
        session.request = AsyncMock(return_value=response)
        cloud = get_midea_cloud(
            "美的美居",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        assert await cloud.login()

    async def test_meijucloud_login_invalid_user(self) -> None:
        """Test MeijuCloud login invalid user."""
        session = Mock()
        response = Mock()
        response.read = AsyncMock(
            return_value=self.responses["cloud_invalid_response.json"],
        )
        session.request = AsyncMock(return_value=response)
        cloud = get_midea_cloud(
            "美的美居",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        assert not await cloud.login()

    async def test_meijucloud_get_keys(self) -> None:
        """Test MeijuCloud get_cloud_keys."""
        session = Mock()
        response = Mock()
        response.read = AsyncMock(
            side_effect=[
                self.responses["meijucloud_get_keys1.json"],
                self.responses["meijucloud_get_keys2.json"],
                self.responses["meijucloud_get_keys1.json"],
                self.responses["cloud_invalid_response.json"],
                self.responses["cloud_invalid_response.json"],
                self.responses["meijucloud_get_keys2.json"],
                self.responses["cloud_invalid_response.json"],
                self.responses["cloud_invalid_response.json"],
            ],
        )
        session.request = AsyncMock(return_value=response)
        cloud = get_midea_cloud(
            "美的美居",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None

        # test method1 + method2
        keys3: dict = await cloud.get_cloud_keys(100)
        # test response token/key
        assert keys3[1]["token"] == "method1_return_token1"
        assert keys3[1]["key"] == "method1_return_key1"
        assert keys3[2]["token"] == "method2_return_token2"
        assert keys3[2]["key"] == "method2_return_key2"
        # simple test default key with length
        assert len(keys3) == 2

        # test method1
        keys1: dict = await cloud.get_cloud_keys(100)
        # test response token/key
        assert keys1[1]["token"] == "method1_return_token1"
        assert keys1[1]["key"] == "method1_return_key1"
        # simple test default key with length
        assert len(keys1) == 1

        # test method2
        keys2: dict = await cloud.get_cloud_keys(100)
        # test response token/key
        assert keys2[2]["token"] == "method2_return_token2"
        assert keys2[2]["key"] == "method2_return_key2"
        # simple test default key with length
        assert len(keys2) == 1

        # test only default key
        keys = await cloud.get_default_keys()
        assert len(keys) == 1
        assert keys == DEFAULT_KEYS

    async def test_meijucloud_list_home(self) -> None:
        """Test MeijuCloud list_home."""
        session = Mock()
        response = Mock()
        response.read = AsyncMock(
            return_value=self.responses["meijucloud_list_home.json"],
        )
        session.request = AsyncMock(return_value=response)
        cloud = get_midea_cloud(
            "美的美居",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        homes = await cloud.list_home()
        assert homes is not None
        assert len(homes.keys()) == 2
        assert homes[1] == "Home 1"
        assert homes[2] == "Home 2"

        response.read = AsyncMock(
            return_value=self.responses["cloud_invalid_response.json"],
        )
        assert await cloud.list_home() is None

    async def test_meijucloud_list_appliances(self) -> None:
        """Test MeijuCloud list_appliances."""
        session = Mock()
        response = Mock()
        response.read = AsyncMock(
            side_effect=[
                self.responses["cloud_login_id.json"],
                self.responses["meijucloud_login.json"],
                self.responses["meijucloud_list_appliances.json"],
                self.responses["cloud_invalid_response.json"],
            ],
        )
        session.request = AsyncMock(return_value=response)
        cloud = get_midea_cloud(
            "美的美居",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        assert await cloud.login()
        appliances = await cloud.list_appliances("1")
        assert appliances is not None
        assert len(appliances.keys()) == 2
        appliance = appliances.get(1)
        assert appliance is not None
        assert appliance.get("name") == "Appliance Name"
        assert appliance.get("type") == 0xAC
        assert appliance.get("sn") == "mySecretKey"
        assert appliance.get("sn8") == "9d52c159"
        assert appliance.get("model_number") == 10
        assert appliance.get("manufacturer_code") == "1234"
        assert appliance.get("model") == "Product Model"
        assert appliance.get("online")

        appliance = appliances.get(2)
        assert appliance is not None
        assert appliance.get("name") == "Appliance Name 2"
        assert appliance.get("type") == 0xAC
        assert appliance.get("sn") == ""
        assert appliance.get("sn8") == "00000000"
        assert appliance.get("model_number") == 0
        assert appliance.get("manufacturer_code") == "1234"
        assert appliance.get("model") == "00000000"
        assert not appliance.get("online")

        appliances = await cloud.list_appliances("1")
        assert appliances is None

    async def test_meijucloud_get_device_info(self) -> None:
        """Test MeijuCloud get_device_info."""
        session = Mock()
        response = Mock()
        response.read = AsyncMock(
            side_effect=[
                self.responses["cloud_login_id.json"],
                self.responses["meijucloud_login.json"],
                self.responses["meijucloud_get_device_info.json"],
                self.responses["meijucloud_get_device_info_alt.json"],
                self.responses["cloud_invalid_response.json"],
            ],
        )
        session.request = AsyncMock(return_value=response)
        cloud = get_midea_cloud(
            "美的美居",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        assert await cloud.login()

        device = await cloud.get_device_info(1)
        assert device is not None
        assert device.get("name") == "Appliance Name"
        assert device.get("type") == 0xAC
        assert device.get("sn") == "mySecretKey"
        assert device.get("sn8") == "9d52c159"
        assert device.get("model_number") == 10
        assert device.get("manufacturer_code") == "1234"
        assert device.get("model") == "Product Model"
        assert device.get("online")

        device = await cloud.get_device_info(2)
        assert device is not None
        assert device.get("name") == "Appliance Name 2"
        assert device.get("type") == 0xAC
        assert device.get("sn") == ""
        assert device.get("sn8") == "00000000"
        assert device.get("model_number") == 0
        assert device.get("manufacturer_code") == "1234"
        assert device.get("model") == "00000000"
        assert not device.get("online")
        assert device.get("des") is None
        assert device.get("active_status") == 1
        assert device.get("active_time") == "2024-06-12 10:45:45"
        assert device.get("master_id") is None
        assert device.get("wifi_version") == "059009012205"
        assert device.get("enterprise") == "0000"
        assert device.get("is_other_equipment") is None
        assert device.get("attrs") is None
        assert device.get("room_name") is None
        assert device.get("bt_mac") == "54B8740FA801"
        assert device.get("bt_token") is None
        assert device.get("hotspot_name") is None
        assert device.get("is_bluetooth") == 0
        assert device.get("bind_type") is None
        assert device.get("ability") is None
        assert device.get("name_changed") is None
        assert not device.get("support_wot")
        assert device.get("template_of_tsl") is None
        assert device.get("shadow_level") is None
        assert device.get("smart_product_id") == 10004256
        assert device.get("brand") is None

        device = await cloud.get_device_info(99)
        assert device is None

    async def test_meijucloud_download_lua(self) -> None:
        """Test MeijuCloud download_lua."""
        session = Mock()
        response = Mock()
        response.read = AsyncMock(
            side_effect=[
                self.responses["cloud_login_id.json"],
                self.responses["meijucloud_login.json"],
                self.responses["meijucloud_download_lua.json"],
                self.responses["meijucloud_download_lua.json"],
            ],
        )
        session.request = AsyncMock(return_value=response)
        res = Mock()
        res.status = 200
        res.text = AsyncMock(return_value="9d52c159dcdd32bac5109cf54080fca7")
        session.get = AsyncMock(return_value=res)
        cloud = get_midea_cloud(
            "美的美居",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        assert await cloud.login()

        with TemporaryDirectory() as tmpdir:
            file = await cloud.download_lua(tmpdir, 10, "00000000", "0xAC", "0010")
            assert file is not None
            file_path = Path(file)
            assert Path.exists(file_path)
            Path.unlink(file_path)

            res.status = 404
            assert (
                await cloud.download_lua(tmpdir, 10, "00000000", "0xAC", "0010") is None
            )

    async def test_msmartcloud_login_success(self) -> None:
        """Test MSmartCloud login."""
        session = Mock()
        response = Mock()
        response.read = AsyncMock(
            side_effect=[
                self.responses["msmartcloud_reroute.json"],
                self.responses["cloud_login_id.json"],
                self.responses["msmartcloud_login.json"],
            ],
        )
        session.request = AsyncMock(return_value=response)
        cloud = get_midea_cloud(
            "SmartHome",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        assert await cloud.login()

    async def test_msmartcloud_login_invalid_user(self) -> None:
        """Test MSmartCloud login invalid user."""
        session = Mock()
        response = Mock()
        response.read = AsyncMock(
            return_value=self.responses["cloud_invalid_response.json"],
        )
        session.request = AsyncMock(return_value=response)
        cloud = get_midea_cloud(
            "SmartHome",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        assert not await cloud.login()

    async def test_msmartcloud_list_home(self) -> None:
        """Test MSmartCloud list_home."""
        session = Mock()
        cloud = get_midea_cloud(
            "SmartHome",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        homes = await cloud.list_home()
        assert homes is not None
        assert len(homes.keys()) == 1

    async def test_msmartcloud_list_appliances(self) -> None:
        """Test MSmartCloud list_appliances."""
        session = Mock()
        response = Mock()
        response.read = AsyncMock(
            side_effect=[
                self.responses["msmartcloud_reroute.json"],
                self.responses["cloud_login_id.json"],
                self.responses["msmartcloud_login.json"],
                self.responses["msmartcloud_list_appliances.json"],
                self.responses["cloud_invalid_response.json"],
            ],
        )
        session.request = AsyncMock(return_value=response)
        cloud = get_midea_cloud(
            "SmartHome",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        assert await cloud.login()
        appliances = await cloud.list_appliances(None)
        assert appliances is not None
        assert len(appliances.keys()) == 2
        appliance = appliances.get(1)
        assert appliance is not None
        assert appliance.get("name") == "Appliance Name"
        assert appliance.get("type") == 0xAC
        assert appliance.get("sn") == "1234567890abcdef1234567890abcdef"
        assert appliance.get("sn8") == "0abcdef1"
        assert appliance.get("model_number") == 10
        assert appliance.get("manufacturer_code") == "1234"
        assert appliance.get("model") == "0abcdef1"
        assert appliance.get("online")

        appliance = appliances.get(2)
        assert appliance is not None
        assert appliance.get("name") == "Appliance Name 2"
        assert appliance.get("type") == 0xAC
        assert appliance.get("sn") == ""
        assert appliance.get("sn8") == ""
        assert appliance.get("model_number") == 0
        assert appliance.get("manufacturer_code") == "1234"
        assert appliance.get("model") == ""
        assert not appliance.get("online")

        appliances = await cloud.list_appliances(None)
        assert appliances is None

    async def test_msmartcloud_get_device_info(self) -> None:
        """Test MSmartCloud get_device_info."""
        session = Mock()
        response = Mock()
        response.read = AsyncMock(
            side_effect=[
                self.responses["msmartcloud_reroute.json"],
                self.responses["cloud_login_id.json"],
                self.responses["msmartcloud_login.json"],
                self.responses["msmartcloud_list_appliances.json"],
                ClientConnectionError(),
                self.responses["msmartcloud_list_appliances.json"],
            ],
        )
        session.request = AsyncMock(return_value=response)
        cloud = get_midea_cloud(
            "SmartHome",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        assert await cloud.login()

        device = await cloud.get_device_info(1)
        assert device is not None
        assert device.get("name") == "Appliance Name"
        assert device.get("type") == 0xAC
        assert device.get("sn") == "1234567890abcdef1234567890abcdef"
        assert device.get("sn8") == "0abcdef1"
        assert device.get("model_number") == 10
        assert device.get("manufacturer_code") == "1234"
        assert device.get("model") == "0abcdef1"
        assert device.get("online")

        device = await cloud.get_device_info(99)
        assert device is None

    async def test_msmartcloud_download_lua(self) -> None:
        """Test MSmartCloud download_lua."""
        session = Mock()
        response = Mock()
        response.read = AsyncMock(
            side_effect=[
                self.responses["msmartcloud_reroute.json"],
                self.responses["cloud_login_id.json"],
                self.responses["msmartcloud_login.json"],
                self.responses["meijucloud_download_lua.json"],
            ],
        )
        session.request = AsyncMock(return_value=response)
        res = Mock()
        res.status = 200
        res.text = AsyncMock(return_value="4ABE0FE395F3AD3B6BC4D223F1ADFA7C")
        session.get = AsyncMock(return_value=res)
        cloud = get_midea_cloud(
            "SmartHome",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        assert await cloud.login()

        with TemporaryDirectory() as tmpdir:
            file = await cloud.download_lua(tmpdir, 10, "00000000", "0xAC", "0010")
            assert file is not None
            file_path = Path(file)
            assert Path.exists(file_path)
            Path.unlink(file_path)

    async def test_mideaaircloud_login_success(self) -> None:
        """Test MideaAirCloud login."""
        session = Mock()
        response = Mock()
        response.read = AsyncMock(
            side_effect=[
                self.responses["mideaaircloud_login_id.json"],
                self.responses["mideaaircloud_login.json"],
            ],
        )
        session.request = AsyncMock(return_value=response)
        cloud = get_midea_cloud(
            "Midea Air",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        assert await cloud.login()

    async def test_mideaaircloud_login_invalid_user(self) -> None:
        """Test MideaAirCloud login invalid user."""
        session = Mock()
        response = Mock()
        response.read = AsyncMock(
            return_value=self.responses["mideaaircloud_invalid_response.json"],
        )
        session.request = AsyncMock(return_value=response)
        cloud = get_midea_cloud(
            "Midea Air",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        assert not await cloud.login()

    async def test_mideaaircloud_list_home(self) -> None:
        """Test MideaAirCloud list_home."""
        session = Mock()
        cloud = get_midea_cloud(
            "Midea Air",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        homes = await cloud.list_home()
        assert homes is not None
        assert len(homes.keys()) == 1

    async def test_mideaaircloud_list_appliances(self) -> None:
        """Test MideaAirCloud list_appliances."""
        session = Mock()
        response = Mock()
        response.read = AsyncMock(
            side_effect=[
                self.responses["mideaaircloud_login_id.json"],
                self.responses["mideaaircloud_login.json"],
                self.responses["mideaaircloud_list_appliances.json"],
                self.responses["mideaaircloud_invalid_response.json"],
            ],
        )
        session.request = AsyncMock(return_value=response)
        cloud = get_midea_cloud(
            "Midea Air",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        assert await cloud.login()
        appliances = await cloud.list_appliances(None)
        assert appliances is not None
        assert len(appliances.keys()) == 2
        appliance = appliances.get(1)
        assert appliance is not None
        assert appliance.get("name") == "Appliance Name"
        assert appliance.get("type") == 0xAC
        assert appliance.get("sn") == "1234567890abcdef1234567890abcdef"
        assert appliance.get("sn8") == "0abcdef1"
        assert appliance.get("model_number") == 10
        assert appliance.get("manufacturer_code") == "1234"
        assert appliance.get("model") == "0abcdef1"
        assert appliance.get("online")

        appliance = appliances.get(2)
        assert appliance is not None
        assert appliance.get("name") == "Appliance Name 2"
        assert appliance.get("type") == 0xAC
        assert appliance.get("sn") == ""
        assert appliance.get("sn8") == ""
        assert appliance.get("model_number") == 0
        assert appliance.get("manufacturer_code") == "1234"
        assert appliance.get("model") == ""
        assert not appliance.get("online")

        appliances = await cloud.list_appliances(None)
        assert appliances is None

    async def test_mideaaircloud_get_device_info(self) -> None:
        """Test MideaAirCloud get_device_info."""
        session = Mock()
        response1 = Mock()
        response1.read = AsyncMock(
            return_value=self.responses["mideaaircloud_login_id.json"],
        )
        response2 = Mock()
        response2.read = AsyncMock(
            return_value=self.responses["mideaaircloud_login.json"],
        )
        response3 = Mock()
        response3.read = AsyncMock(
            return_value=self.responses["mideaaircloud_list_appliances.json"],
        )

        session.request = AsyncMock(
            side_effect=[
                response1,
                response2,
                response3,
                ClientConnectionError(),
                response3,
            ],
        )
        cloud = get_midea_cloud(
            "Midea Air",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        assert await cloud.login()

        device = await cloud.get_device_info(1)
        assert device is not None
        assert device.get("name") == "Appliance Name"
        assert device.get("type") == 0xAC
        assert device.get("sn") == "1234567890abcdef1234567890abcdef"
        assert device.get("sn8") == "0abcdef1"
        assert device.get("model_number") == 10
        assert device.get("manufacturer_code") == "1234"
        assert device.get("model") == "0abcdef1"
        assert device.get("online")

        device = await cloud.get_device_info(99)
        assert device is None

    async def test_mideaaircloud_download_lua(self) -> None:
        """Test MideaAirCloud download_lua."""
        session = Mock()
        cloud = get_midea_cloud(
            "Midea Air",
            session=session,
            account="account",
            password="password",
        )
        assert cloud is not None
        with pytest.raises(NotImplementedError), TemporaryDirectory() as tmpdir:
            await cloud.download_lua(tmpdir, 10, "00000000", "0xAC", "0010")
