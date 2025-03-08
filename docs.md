# Pan123 Python 模块文档

**阅读须知** 由于时间原因，文档由AI编写，尽请谅解，也欢迎pr来完善文档和代码

## 异常类
### `ClientKeyError`
- **描述**：当 `client_id` 或 `client_secret` 错误时抛出的异常。
- **参数**：
  - `r`：API 返回的错误信息。

### `AccessTokenError`
- **描述**：当 `access_token` 错误时抛出的异常。
- **参数**：
  - `r`：API 返回的错误信息。

## 函数

### `get_access_token(client_id: str, client_secret: str, base_url: str = "https://open-api.123pan.com", header: dict = None)`
- **描述**：获取访问令牌。
- **参数**：
  - `client_id`：客户端 ID。
  - `client_secret`：客户端密钥。
  - `base_url`：API 请求的基础 URL，默认为 `https://open-api.123pan.com`。
  - `header`：请求头，默认为 `{"Content-Type": "application / json", "Platform": "open_platform"}`。
- **返回值**：访问令牌。
- **异常**：
  - `ClientKeyError`：当 `client_id` 或 `client_secret` 错误时抛出。
  - `requests.HTTPError`：当 HTTP 请求失败时抛出。

### `check_status_code(r)`
- **描述**：检查 HTTP 响应状态码和 API 返回的 `code`。
- **参数**：
  - `r`：HTTP 响应对象。
- **返回值**：响应数据中的 `data` 部分。
- **异常**：
  - `AccessTokenError`：当 `access_token` 错误时抛出。
  - `requests.HTTPError`：当 HTTP 请求失败时抛出。

### `get_file_md5(file_path)`
- **描述**：计算文件的 MD5 哈希值。
- **参数**：
  - `file_path`：文件的路径。
- **返回值**：文件的 MD5 哈希值（十六进制字符串）。

## 类

### `Pan123(access_token: str)`
- **描述**：与 123 云盘开放平台进行交互的客户端类。
- **参数**：
  - `access_token`：访问令牌。

#### 方法

##### `create_share(share_name: str, share_expire: int, file_id_list: list, share_pwd=None)`
- **描述**：创建分享链接。
- **参数**：
  - `share_name`：分享名称。
  - `share_expire`：分享有效期。
  - `file_id_list`：文件 ID 列表。
  - `share_pwd`：分享密码，可选。
- **返回值**：包含分享 ID、分享链接和分享密钥的字典。
- **异常**：
  - `AccessTokenError`：当 `access_token` 错误时抛出。
  - `requests.HTTPError`：当 HTTP 请求失败时抛出。

##### `share_list_info(shareIdList: list, trafficSwitch: bool = None, trafficLimitSwitch: bool = None, trafficLimit: int = None)`
- **描述**：修改分享链接信息。
- **参数**：
  - `shareIdList`：分享 ID 列表。
  - `trafficSwitch`：流量开关，可选。
  - `trafficLimitSwitch`：流量限制开关，可选。
  - `trafficLimit`：流量限制，可选。
- **返回值**：响应数据中的 `data` 部分。
- **异常**：
  - `AccessTokenError`：当 `access_token` 错误时抛出。
  - `requests.HTTPError`：当 HTTP 请求失败时抛出。
  - `ValueError`：当流量限制开关为 `True` 但流量限制未提供时抛出。

##### `share_list(limit: int, lastShareId: int = None)`
- **描述**：获取分享列表信息。
- **参数**：
  - `limit`：每页返回的分享数量。
  - `lastShareId`：上一页最后一个分享的 ID，用于分页查询，可选。
- **返回值**：响应数据中的 `data` 部分。
- **异常**：
  - `AccessTokenError`：当 `access_token` 错误时抛出。
  - `requests.HTTPError`：当 HTTP 请求失败时抛出。

##### `file_list(parent_file_id: int, limit: int)`
- **描述**：获取文件列表。
- **参数**：
  - `parent_file_id`：父文件 ID。
  - `limit`：每页返回的文件数量。
- **返回值**：响应数据中的 `data` 部分。
- **异常**：
  - `AccessTokenError`：当 `access_token` 错误时抛出。
  - `requests.HTTPError`：当 HTTP 请求失败时抛出。

##### `file_mkdir(name: str, parent_id: int)`
- **描述**：创建文件夹。
- **参数**：
  - `name`：文件夹名称。
  - `parent_id`：父文件夹 ID。
- **返回值**：响应数据中的 `data` 部分。
- **异常**：
  - `AccessTokenError`：当 `access_token` 错误时抛出。
  - `requests.HTTPError`：当 HTTP 请求失败时抛出。

##### `file_create(parentFileID: int, filename: str, etag: str, size: int, duplicate: int = None)`
- **描述**：创建文件。
- **参数**：
  - `parentFileID`：父文件 ID。
  - `filename`：文件名。
  - `etag`：文件的 etag。
  - `size`：文件大小。
  - `duplicate`：重复处理方式，可选。
- **返回值**：响应数据中的 `data` 部分。
- **异常**：
  - `AccessTokenError`：当 `access_token` 错误时抛出。
  - `requests.HTTPError`：当 HTTP 请求失败时抛出。

##### `file_get_upload_url(preuploadID: str, sliceNo: int)`
- **描述**：获取文件上传 URL。
- **参数**：
  - `preuploadID`：预上传 ID。
  - `sliceNo`：切片编号。
- **返回值**：预签名的上传 URL。
- **异常**：
  - `AccessTokenError`：当 `access_token` 错误时抛出。
  - `requests.HTTPError`：当 HTTP 请求失败时抛出。

##### `file_upload(url: str, data: bytes)`
- **描述**：上传文件切片。
- **参数**：
  - `url`：上传 URL。
  - `data`：文件切片数据。
- **返回值**：HTTP 响应对象。

##### `file_list_upload_parts(preuploadID: str)`
- **描述**：列出已上传的文件切片。
- **参数**：
  - `preuploadID`：预上传 ID。
- **返回值**：响应数据中的 `data` 部分。
- **异常**：
  - `AccessTokenError`：当 `access_token` 错误时抛出。
  - `requests.HTTPError`：当 HTTP 请求失败时抛出。

##### `file_upload_complete(preuploadID: str)`
- **描述**：完成文件上传。
- **参数**：
  - `preuploadID`：预上传 ID。
- **返回值**：响应数据中的 `data` 部分。
- **异常**：
  - `AccessTokenError`：当 `access_token` 错误时抛出。
  - `requests.HTTPError`：当 HTTP 请求失败时抛出。

##### `file_upload_async_result(preuploadID: str)`
- **描述**：获取文件异步上传结果。
- **参数**：
  - `preuploadID`：预上传 ID。
- **返回值**：响应数据中的 `data` 部分。
- **异常**：
  - `AccessTokenError`：当 `access_token` 错误时抛出。
  - `requests.HTTPError`：当 HTTP 请求失败时抛出。

##### `file_upload_one(parentFileID, file_path)`
- **描述**：一键上传文件。
- **参数**：
  - `parentFileID`：父文件 ID。
  - `file_path`：文件路径。
- **异常**：
  - `requests.HTTPError`：当 HTTP 请求失败时抛出。

## 使用示例
```python
# 获取访问令牌
client_id = "your_client_id"
client_secret = "your_client_secret"
access_token = get_access_token(client_id, client_secret)

# 创建 Pan123 客户端实例
pan = Pan123(access_token)

# 创建分享链接
share_name = "My Share"
share_expire = 3600
file_id_list = [123, 456]
share_info = pan.create_share(share_name, share_expire, file_id_list)
print(share_info)

# 上传文件
parentFileID = 789
file_path = "path/to/your/file"
pan.file_upload_one(parentFileID, file_path)