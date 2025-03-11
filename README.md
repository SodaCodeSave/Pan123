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
from pan123 import get_access_token, Pan123
# 如果已经获取了access_token，则可以直接导入Pan123模块
from pan123 import Pan123
```
### 模块文档
**阅读须知** 暂时没有覆盖到全部函数，请查看[123云盘开放文档](https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced/ppsuasz6rpioqbyt)

[docs.md](https://github.com/SodaCodeSave/Pan123/blob/main/docs.md)

### 已经实现的内容
- 分享链接
- 文件管理
- 用户管理
- 离线下载
- 直链
### 正在编写的内容
- 视频转码 
- 图床