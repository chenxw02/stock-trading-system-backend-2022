# 股票交易系统后端

注意，我们完成的是前后端分离的股票交易系统，你不需要从flask返回任何html。response body统一为application/json。由前端请求获得数据后自行渲染。

## 运行

你可以使用jetbrains的pycharm运行，也可以直接`python app.py`，默认在本机`localhost:5000`开启RESTful服务。依赖列表：

```shell
pip install flask
pip install pyjwt
```

你可以自由选择vsc或者pycharm来编写代码，但个人觉得jb家的IDE都还挺好用的（，所以选择了pycharm。

[免费教育许可证 - 社区支持 (jetbrains.com.cn)](https://www.jetbrains.com.cn/community/education/#students) 你可以从这里获取到免费的JetBrains全家桶，需要从学信网获取学籍认证（zju教育邮箱因为失信被拉黑了）。

## 代码规范

请使用全小写+下划线的方式给任意变量/函数命名（如admin\_id），其中类的私有变量（python并没有实际的private功能）请使用下划线作为开头（如\_admin\_id），以提示此为私有。

类名使用大驼峰，如AdminService。

## 异常处理

在controller/下，为你的api创建一个对应的errorhandler，errorhandler也需要注册到蓝图（Blueprint），可参考admin\_api.py和admin\_errorhandler.py。

如何创建一个异常？你需要首先在error/下定义一个异常类，里面可以啥也不写直接pass，参考InvalidAccountError。然后，在你的service方法中在需要的时候raise这个异常。然后，errorhandler就可以捕获到这个类型的异常，并根据异常的类型返回相应的错误码和信息。

```python
prefix = "10" # 请为你的那项服务的错误码定义一个唯一的前缀

@admin_api.errorhandler(InvalidAccountError)
def invalid_account_error(error):
    return Result.error(prefix+"1", "账号密码错误")
```

```python
class AdminService:
	def login(self, admin_id, password):
    	# print(admin_id)
    	# print(password)
    	# TODO:用self._admin_dao从数据库核验是否正确,如果不正确抛出异常/直接返回空
    	raise InvalidAccountError()
    	# raise 以返回账号密码错误
        ...
```

这里无条件抛了一个异常，在正确配置和编写errorhandler后，我们便可以发送请求得到如下结果：

![image-20220516092007296](https://beetpic.oss-cn-hangzhou.aliyuncs.com/img/image-20220516092007296.png)

## 模块

姑且分为Controller，Service，Dao三个。Java项目中常用这样的结构，搬到Python也足够清晰。Dao中编写单纯的数据库交互，用传入的参数Insert/Select等等。Service层中调用各个Dao层完成业务逻辑处理。Controller层负责过滤、调用Service和统一的结果返回（包装成信息码/错误码+数据的形式）。

### Controller

在其中编写你的HTTP api响应模块，并在根目录的app.py中用蓝图注册，可以参考demo_api.py。

#### 统一结果返回

在util/result.py中，定义了统一结果类，其中有两个静态方法：Result.error(code, message)和Result.success(data)。

Controller中，你只需要返回Result.success(data)来对你的返回data进行包装。

而异常中，你需要返回Result.error(code, message)，前端将message渲染给用户，让用户感知到错误原因。

### Service

待补充。

### Dao

待补充。

