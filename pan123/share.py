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
        url = self.base_url + "/api/v1/share/create"
        data = {
            "shareName": share_name,
            "shareExpire": share_expire,
            "fileIDList": file_id_list,
        }
        if share_pwd:
            data["sharePwd"] = share_pwd
        data["trafficSwitch"] = bool(traffic_switch) + 1
        data["trafficLimitSwitch"] = bool(traffic_limit_switch) + 1
        if traffic_limit_switch and traffic_limit <= 0:
            return ValueError("需要限制流量时，限制值不能为空")
        r = requests.post(url, data=data, headers=self.header)
        rdata = json.loads(r.text)
        if r.status_code == 200:
            if rdata["code"] == 0:
                return {
                    "shareID": rdata["data"]["shareID"],
                    "shareLink": f"https://www.123pan.com/s/{rdata['data']['shareKey']}",
                    "shareKey": rdata["data"]["shareKey"],
                }
            else:
                raise AccessTokenError(rdata)
        else:
            raise requests.HTTPError

    def list_info(
        self,
        share_id_list: list,
        traffic_switch: bool = False,
        traffic_limit_switch: bool = False,
        traffic_limit: int = 0,
    ):
        url = self.base_url + "/api/v1/share/list/info"
        data = {"shareIdList": share_id_list}
        if traffic_switch:
            if traffic_switch:
                data["trafficSwitch"] = 2
            elif not traffic_switch:
                data["trafficSwitch"] = 1
        if traffic_limit_switch:
            if traffic_limit_switch:
                data["trafficLimitSwitch"] = 2
                if traffic_limit:
                    data["trafficLimit"] = traffic_limit
                else:
                    return ValueError("流量限制开关为True时，流量限制不能为空")
            elif not traffic_limit_switch:
                data["trafficLimitSwitch"] = 1
        r = requests.put(url, data=data, headers=self.header)
        return parse_response_data(r)

    def list(self, limit: int, last_share_id: int = None):

        url = self.base_url + "/api/v1/share/list"

        data = {"limit": limit}

        if last_share_id:
            data["lastShareId"] = last_share_id

        r = requests.get(url, data=data, headers=self.header)

        return check_status_code(r)
