import json
import requests

from .utils.exceptions import AccessTokenError
from .utils.request import parse_response_data
from .abstracts import Requestable


class Share(Requestable):
    def create(
        self,
        share_name: str,
        share_expire: int,
        file_id_list: list,
        share_pwd: str = "",
        traffic_switch: bool = False,
        traffic_limit_switch: bool = False,
        traffic_limit: int = 0,
    ):
        data: dict = {
            "shareName": share_name,
            "shareExpire": share_expire,
            "fileIDList": file_id_list,
        }
        if share_pwd:
            data["sharePwd"] = share_pwd
        data = Share.apply_traffic_settings(
            data,
            traffic_switch,
            traffic_limit_switch,
            traffic_limit,
        )
        response = requests.post(
            self.use_url("/api/v1/share/create"),
            data=data,
            headers=self.header,
        )
        response_data = json.loads(response.text)
        parse_response_data(response, AccessTokenError)
        return {
            "shareID": response_data["data"]["shareID"],
            "shareLink": f"https://www.123pan.com/s/{response_data['data']['shareKey']}",
            "shareKey": response_data["data"]["shareKey"],
        }

    def list_info(
        self,
        share_id_list: list,
        traffic_switch: bool = False,
        traffic_limit_switch: bool = False,
        traffic_limit: int = 0,
    ):
        data: dict = Share.apply_traffic_settings(
            {"shareIdList": share_id_list},
            traffic_switch,
            traffic_limit_switch,
            traffic_limit,
        )
        return parse_response_data(
            requests.put(
                self.use_url("/api/v1/share/list/info"),
                data=data,
                headers=self.header,
            )
        )

    def list(self, limit: int, last_share_id: int = 0):
        data = {"limit": limit}
        if last_share_id:
            data["lastShareId"] = last_share_id
        return parse_response_data(
            requests.get(
                self.use_url("/api/v1/share/list"), data=data, headers=self.header
            )
        )

    @staticmethod
    def apply_traffic_settings(
        data: dict,
        traffic_switch: bool = False,
        traffic_limit_switch: bool = False,
        traffic_limit: int = 0,
    ) -> dict:
        data = data.copy()
        data["trafficSwitch"] = bool(traffic_switch) + 1  # True=1,False=0
        data["trafficLimitSwitch"] = bool(traffic_limit_switch) + 1
        if traffic_limit_switch and traffic_limit <= 0:
            raise ValueError("需要限制流量时，限制值必须大于0")
        return data
