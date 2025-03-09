# Pan123文档
## 接入流程
### 1. 申请账号
请前往 [123云盘开放平台](https://www.123pan.cn/developer) 填写问卷申请
### 2. 获取client_id和client_secret
申请通过后，会给你的邮箱发送`client_id`和`client_secret`，请妥善保存，然后使用如下代码获取`access_token`
```python
from pan123 import get_access_token

# 将your_client_id和your_client_secret替换成你的client_id和client_secret
get_access_token("your_client_id", "your_client_secret")
```
> 此函数有访问频率限制。请获取到`access_token`后本地保存使用，并在`access_token`过期前及时重新获取。`access_token`有效期根据返回的`expiredAt`字段判断
## 类
### `Pan123(access_token)`
- 123云盘开放平台客户端。
- 输入：
  - `access_token`:str - 你的access_token
- 输出：
  - 无
## 函数
> 加急编写中（；´д｀）ゞ