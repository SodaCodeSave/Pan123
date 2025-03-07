# 123Pan
这是一个非官方的123云盘开放平台调用库，可以轻松的在Python中调用123云盘开放平台而不需要多次编写重复的代码
## 安装
```
pip uninstall 123pan
pip install 123pan
```
## 使用
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
