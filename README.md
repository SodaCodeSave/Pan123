# 123Pan
这是一个非官方的123云盘开放平台调用库，可以轻松的在Python中调用123云盘开放平台而不需要多次编写重复的代码
## 安装
使用稳定版
```
pip uninstall 123pan
pip install 123pan
```
## 使用
部分函数可能未编写全面，详细请查看[123云盘开放文档](https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced/ppsuasz6rpioqbyt)
### 导入模块

```python
# 全量导入
from pan123.pan123 import get_access_token, Pan123
# 如果已经获取了access_token，则可以直接导入Pan123模块
from pan123.pan123 import Pan123
```
### 获取 access_token
获取访问令牌。

此函数通过POST请求向指定的API端点获取访问令牌。它需要客户端ID和客户端密钥作为参数，
并可选地接受基础URL和自定义头部信息。

参数:
- client_id (str): 客户端ID。
- client_secret (str): 客户端密钥。
- base_url (str, 可选): API的基础URL，默认为"https://open-api.123pan.com"。
- header (dict, 可选): 请求头部信息，默认包含"Content-Type"和"Platform"字段。

返回:
- str: 成功时返回访问令牌字符串。

异常:
- ClientKeyError: 当API返回的code不为0时抛出。
- HTTPError: 当HTTP响应状态码不是200时抛出。

**注：获取后推荐将access_token存到安全的地方，如在同目录创建一个access_token.txt，需要时读取**

### Pan123 Client
要使用123云盘开放平台，需要先创建一个Pan123的客户端

```python
from pan123.pan123 import Pan123

# 将your_access_token替换为你的访问令牌
pan = Pan123("your_access_token")
```
#### create_share()
创建分享链接。

参数:
- share_name (str): 分享的名称。
- share_expire (int): 分享的过期时间。
- file_id_list (list): 需要分享的文件ID列表。
- share_pwd (str, 可选): 分享的密码，默认为None。

返回:
- dict: 包含分享ID、分享链接和分享密钥的字典。

异常:
- AccessTokenError: 如果接口返回的code不为0。
- HTTPError: 如果HTTP请求的状态码不是200。

#### share_list_info()
修改分享链接信息。

参数:
- shareIdList (list): 分享ID列表。
- trafficSwitch (bool, 可选): 免登录流量包开关 False 关闭免登录流量包 True 打开免登录流量包
- trafficLimitSwitch (bool, 可选): 流量限制开关，免登录流量包开关 False 关闭流量限制 True 打开流量限制
- trafficLimit (int, 可选): 流量限制，默认为None。

返回:
- 无

异常:
- AccessTokenError: 如果接口返回的code不为0。
- HTTPError: 如果HTTP请求的状态码不是200。

#### share_list()
获取分享列表。

参数:
- limit (int): 每页返回的分享数量，最大不超过100。
- lastShareId (int): 如果分页的话翻页查询时需要填写。

返回:
- dict: 包含分享列表信息的字典。

异常:
- AccessTokenError: 如果接口返回的code不为0。
- HTTPError: 如果HTTP请求的状态码不是200。

#### file_list()
获取指定父文件夹下的文件列表。

通过发送GET请求到/api/v2/file/list接口，获取指定父文件夹下的一批文件信息。

参数:
- parent_file_id (int): 父文件夹的ID。
- limit (int): 最多返回的文件数量。

返回:
- list: 文件列表，每个文件的信息以字典形式表示。

异常:
- AccessTokenError: 如果接口返回的code不为0，则抛出AccessTokenError异常。
- HTTPError: 如果HTTP请求的响应状态码不是200，则抛出HTTPError异常。

#### file_mkdir()
创建文件夹

通过发送GET请求到服务器，创建一个新文件夹

参数:
name (str): 要创建的文件夹的名称
parent_id (int): 新文件夹的父目录ID

返回:
新创建文件夹的相关信息，具体结构取决于服务器返回的数据

异常:
AccessTokenError: 当服务器返回的code不为0时抛出
HTTPError: 当HTTP响应状态码不是200时抛出

#### file_create()
创建文件。

通过发送POST请求到 `/upload/v1/file/create` 接口，在指定父文件夹下创建一个新文件。

参数:
- parentFileID (int): 父目录id，上传到根目录时填写 0
- filename (str): 文件名要小于255个字符且不能包含以下任何字符："\/:*?|><。（注：不能重名）
- etag (str): 文件md5
- size (int): 文件大小，单位为 byte 字节
- duplicate (int, 可选): 当有相同文件名时，文件处理策略（1保留两者，新文件名将自动添加后缀，2覆盖原文件）

返回:
- dict: 响应数据中的 `data` 部分，具体结构取决于服务器返回的数据。

异常:
- AccessTokenError: 如果API返回的code不为0，则抛出 `AccessTokenError` 异常。
- HTTPError: 如果HTTP请求的响应状态码不是200，则抛出 `HTTPError` 异常。