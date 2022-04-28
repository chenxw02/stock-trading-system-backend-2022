# 股票交易系统后端

注意，我们完成的是前后端分离的股票交易系统，你不需要从flask返回任何html。response body统一为application/json。由前端请求获得数据后自行渲染。

## 运行

你可以使用jetbrains的pycharm运行，也可以直接`python app.py`，默认在本机`localhost:5000`开启RESTful服务。当然，在此之前你需要：

```shell
pip install flask
```

你可以自由选择vsc或者pycharm来编写代码，但个人觉得jb家的IDE都还挺好用的（，所以选择了pycharm。

[免费教育许可证 - 社区支持 (jetbrains.com.cn)](https://www.jetbrains.com.cn/community/education/#students) 你可以从这里获取到免费的JetBrains全家桶，需要从学信网获取学籍认证（zju教育邮箱因为失信被拉黑了）。

## 模块

姑且分为Controller，Service，Dao三个。Java项目中常用这样的结构，搬到Python也足够清晰。Dao中编写单纯的数据库交互，用传入的参数Insert/Select等等。Service层中调用各个Dao层完成业务逻辑处理。Controller层负责过滤、调用Service和统一的结果返回（包装成信息码/错误码+数据的形式）。

### Controller

在其中编写你的HTTP api响应模块，并在根目录的app.py中用蓝图注册，可以参考demo_api.py。

### Service

待补充。

### Dao

待补充。