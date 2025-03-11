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
## get_access_token(client_id, client_secret, base_url, header)
- 输入: 
    - client_id
    - client_secret
    - base_url
    - header

- 输出：

## check_status_code(r)
- 输入: 
    - r

- 输出：

## get_file_md5(file_path)
- 输入: 
    - file_path

- 输出：

## __init__(self, r)
- 输入: 
    - self
    - r

- 输出：

## __init__(self, r)
- 输入: 
    - self
    - r

- 输出：

## __init__(self, access_token)
- 输入: 
    - self
    - access_token

- 输出：

## create_share(self, share_name, share_expire, file_id_list, share_pwd)
- 输入: 
    - self
    - share_name
    - share_expire
    - file_id_list
    - share_pwd

- 输出：

## share_list_info(self, share_id_list, traffic_switch, traffic_limit_switch, traffic_limit)
- 输入: 
    - self
    - share_id_list
    - traffic_switch
    - traffic_limit_switch
    - traffic_limit

- 输出：

## share_list(self, limit, last_share_id)
- 输入: 
    - self
    - limit
    - last_share_id

- 输出：

## file_list(self, parent_file_id, limit)
- 输入: 
    - self
    - parent_file_id
    - limit

- 输出：

## file_mkdir(self, name, parent_id)
- 输入: 
    - self
    - name
    - parent_id

- 输出：

## file_create(self, preupload_id, filename, etag, size, duplicate)
- 输入: 
    - self
    - preupload_id
    - filename
    - etag
    - size
    - duplicate

- 输出：

## file_get_upload_url(self, preupload_id, slice_no)
- 输入: 
    - self
    - preupload_id
    - slice_no

- 输出：

## file_list_upload_parts(self, preupload_id)
- 输入: 
    - self
    - preupload_id

- 输出：

## file_upload_complete(self, preupload_id)
- 输入: 
    - self
    - preupload_id

- 输出：

## file_upload_async_result(self, preupload_id)
- 输入: 
    - self
    - preupload_id

- 输出：

## file_upload(self, preupload_id, file_path)
- 输入: 
    - self
    - preupload_id
    - file_path

- 输出：

## file_rename(self, rename_dict)
- 输入: 
    - self
    - rename_dict

- 输出：

## file_move(self, file_id_list, to_parent_file_id)
- 输入: 
    - self
    - file_id_list
    - to_parent_file_id

- 输出：

## file_trash(self, file_ids)
- 输入: 
    - self
    - file_ids

- 输出：

## file_recover(self, file_ids)
- 输入: 
    - self
    - file_ids

- 输出：

## file_delete(self, file_ids)
- 输入: 
    - self
    - file_ids

- 输出：

## file_detail(self, file_id)
- 输入: 
    - self
    - file_id

- 输出：

## user_info(self)
- 输入: 
    - self

- 输出：

## offline_download(self, download_url, file_name, save_path, call_back_url)
- 输入: 
    - self
    - download_url
    - file_name
    - save_path
    - call_back_url

- 输出：

## offline_download_process(self, task_id)
- 输入: 
    - self
    - task_id

- 输出：

## query_transcode(self, ids)
- 输入: 
    - self
    - ids

- 输出：

## do_transcode(self, ids)
- 输入: 
    - self
    - ids

- 输出：

## get_direct_link_m3u8(self, file_id)
- 输入: 
    - self
    - file_id

- 输出：

## direct_link_enable(self, file_id)
- 输入: 
    - self
    - file_id

- 输出：

## direct_link_disable(self, file_id)
- 输入: 
    - self
    - file_id

- 输出：

## direct_list_url(self, file_id)
- 输入: 
    - self
    - file_id

- 输出：

