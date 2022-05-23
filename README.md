# 股票交易系统后端

注意，我们完成的是前后端分离的股票交易系统，你不需要从flask返回任何html。response body统一为application/json。由前端请求获得数据后自行渲染。

## 运行

你可以使用jetbrains的pycharm运行，也可以直接`python app.py`，默认在本机`localhost:5000`开启RESTful服务。依赖列表：

```shell
pip install flask
pip install pyjwt # 登录功能鉴权使用jwt（json web token）
pip install bcrypt # 数据库中存储密码使用bcrypt加密
pip install pymysql # mysql驱动
pip install flask-sqlalchemy # flask和sql的框架（ORM）
pip install flask-cors # 允许跨域请求
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

参考AdminService(/service/admin_service.py)，将你的业务逻辑写成一个个静态方法。

### Dao

参考AdminDao(/dao/admin_dao.py)，使用flask-sqlalchemy创建的db来执行插入和commit，使用model中自己创建的表类来执行查询。

## 我应该做什么？

对后台开发经验不多的同学可能看完上面这一堆还是不知所措，这里总结一下。

如果你需要开发一个服务，比如这里以管理员的相关服务为例，也就是我已经写好的admin：

1. 仿照/controller/admin_api.py，将一个变量如`admin_api`注册到Blueprint中，也就是注册到了整个flask服务里。然后在下面创建你的http服务接口:

   ```python
   # 这里的admin_api就是你刚注册到Blueprint的变量名，/admin是这个请求的路由，也可以叫链接。这里的语义即：url/admin收到post请求时，调用如下函数
   @admin_api.route("/admin", methods=["POST"])
   def register():
       # 从收到的请求的请求体（request body）中，读取json数据，转换为一个list或map
       data = json.loads(request.get_data(as_text=True))
       # print(data)
       # 调用你的服务类的静态方法，对这个数据进行工作
       AdminService.register(data)
       # 返回结果，无需返回数据则使用None，否则将数据填入Result.success()
       return Result.success(None)
   ```

2. 上面用到了服务类（AdminService），所以这里你需要创建一个服务类，如/service/admin_service.py。在里面实现你的业务。

   ```python
   @staticmethod
       def register(admins_data):
           admins = []
           for admin_data in admins_data:
               password = admin_data["password"].encode('utf-8')
               encrypted_password = bcrypt.hashpw(password, bcrypt.gensalt())
               # print(encrypted_password)
               admins.append(Admin(admin_id=admin_data["admin_id"], password=encrypted_password))
           # 这里最后调用了AdminDao，也就是数据库操作类，插入了一堆admins
           AdminDao.insert(admins)
   ```

3. 上面用到了数据库操作类（AdminDao），所以这里你需要创建一个数据库操作类，如/dao/admin_dao.py。

   ```python
   from exts import db
   from admin import Admin
   
   # 将一个表的所有简单操作集中成一个dao数据库类
   class AdminDao:
       @staticmethod
       def insert(admins):
           db.session.add_all(admins)
           db.session.commit()
   
       @staticmethod
       def get(admin_id):
           admin = Admin.query.get(admin_id)
           return admin
   ```

   如上就是一个插入一个查找。db是全局注册好的数据库连接，你只需要import就可以用，不需要自己编写代码。Admin则是映射到数据库中的admin表的类，需要在下一步定义它。

   更细的操作还有很多，我只看了一个csdn的介绍，[(8条消息) Flask连接数据库mysql_秀玉轩晨的博客-CSDN博客_flask连接mysql数据库](https://blog.csdn.net/qq_40552152/article/details/121196396)，如果你找到了更好的文档可以直接编辑这个README.md。

4. 如/model/admin.py，需要定义一个和数据库中的表完全相符的类：

   ```python
   from exts import db
   
   
   class Admin(db.Model):
       __tablename__ = "admin"
       admin_id = db.Column(db.String(20), nullable=False, primary_key=True)
       password = db.Column(db.String(200), nullable=False)
   ```

   它既是表的抽象（可以执行Admin.query.get(admin_id)这样的查询）， 也是一个实体数据的抽象，你可以从admin = Admin.query.get(admin_id)得到一个Admin类的实体，从admin.password直接获取到刚查到的数据。

   

tips: 为了方便直接运行，我还是把mysql密码直接写在了config.py里，最后上线时会进行修改。
