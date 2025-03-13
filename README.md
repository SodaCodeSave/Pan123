# 123Pan
这是一个非官方的123云盘开放平台调用库，可以轻松的在Python中调用123云盘开放平台而不需要多次编写重复的代码
## 安装
使用稳定版
```
pip uninstall 123pan
pip install 123pan
```
### 导入模块
```python
# 全量导入
from pan123 import Pan123
from pan123.auth import get_access_token
# 如果已经获取了access_token，则可以直接导入Pan123模块
from pan123 import Pan123
```
### 模块文档
关于模块清查阅 **[Pan123 Github Page文档](https://sodacodesave.github.io/Pan123-Docs/site/)**

如需了解更多，请查阅[123云盘开放平台官方文档](https://123yunpan.yuque.com/org-wiki-123yunpan-muaork/cr6ced/ppsuasz6rpioqbyt)

### 已经实现的内容
- 分享链接
- 文件管理
- 用户管理
- 离线下载
- 直链
- 视频转码 
- 图床
### 正在编写的内容
- 全都写完啦（啪叽啪叽啪叽）