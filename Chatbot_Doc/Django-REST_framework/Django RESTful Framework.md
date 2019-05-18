# Python3 开发以及部署 RESTful API项目（Python3 + Django2.0 + Django REST FrameWork + Centos7 + uWsgi + Nginx）
文档分为两个部分，分别从开发和部署两个方面先介绍项目流程，然后会说明项目中最常遇到的问题以及解决方案。如果项目中有什么处理不正确的地方，也希望大家给予指正、交流。

1. 开发环境采用Python3.6.3版本，项目采用Django2.0，Django REST FrameWork3.7.7去搭建。

2. 部署的时候，系统版本为Centos7，uWsgi版本使用本文发布时最新的2.0.15，Nginx版本1.13.7

## 第一部分 开发流程以及问题说明
由于项目本身基于 Token 的身份验证，另外有些接口不只是处理一个表里的数据，直接通过ORM不太好映射，所以并没有完全按照Django REST FrameWork进行开发，并且只采用GET和POST方法。

### 一、开发步骤
首先搭建开发环境并且创建一个新的项目。
#### 1. 安装Python3：如果使用的是 Mac OS X ，系统可能已经预装了 Python 。我们可以通过homebrew安装Python3。
``` shell
$ brew install python3
```
安装了Python3之后，会有pip3，使用pip install XXX 新安装的库会放在这个目录下面python2.7/site-packages使用pip3 install XXX 新安装的库会放在这个目录下面python3.6/site-packages如果使用python3执行程序，那么就不能import python2.7/site-packages中的库
#### 2. 安装Django和Django REST FrameWork：可以下载django最新版本,若想指定版本,请在命令后面加上版本号。
``` shell {.line-numbers}
$ pip3 install django
$ pip3 install djangorestframework
```
``` shell {.line-numbers}
$ pip3 install django==版本号
$ pip3 install djangorestframework==版本号
```
#### 3. 创建一个新的项目。
``` shell {.line-numbers}
$ cd ~
$ django-admin.py startproject attendances
$ cd attendances
$ python manage.py startapp user apps/user
```
#### 4. 将新user应用和rest_framework应用添加到配置文件attendances/settings.py文件的INSTALLED_APPS。
``` python {.line-numbers}
INSTALLED_APPS = (
    ...
    'rest_framework',
    'apps.user',
)
```
#### 5. 写接口代码前的一点准备。
做完以上步骤，我们就把项目开发需要的环境搭建完成了，接下来就可以在我们的项目中添加接口了。

另外还有一点要说明的是，为了给我们的api增加版本控制，我们的文件目录和路由是这样处理的，这样我们就可以通过添加新的版本文件并且修改配置，同时运行多个版本的接口：

**文件目录结构**
<ul style='list-style:none;'>
<li style='color:red;'>> apis</li>
<li>
    <ul style='list-style:none;'>
        <li style='color:red;'>> api_v1</li>
        <li>
            <ul style='list-style:none'>
            <li style='color:red;'>> user</li>
            <li>> base</li>
            <li>> enum</li>
            <li>> setting</li>
            <li style='color:red;'>> urls</li>
            </ul>
        </li>
    </ul>
</li>
<li>> apps</li>
<li>> attendances</li>
<li>
    <ul style='list-style:none'>
    <li>> setting</li>
    <li style='color:red;'>> urls</li>
    <li>> wsgi</li>
    </ul>
</li>
<li>> static</li>
<li>> attendances.xml</li>
<li>> manage.py</li>
<li>> requirements.txt</li>
<li>> test.py</li>
</ul>

**路由**
``` python {.line-numbers}
# 项目路由
urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^api/v1/', include('apis.api_v1.urls', namespace='api-v1')),
]
```
``` python {.line-numbers}
# apis下面的路由
from apis.api_v1.user import views as api_user

urlpatterns = [
    # user
    url(r'^user/$', api_user.user, name='user'),
]

app_name = 'api-v1'
```
**调用地址：** https://{Domain}/api/v1/user

**请求方法：** GET-获取用户信息 POST-修改用户信息

> 文件说明：apis存放的是api接口文件，app存放的是应用或者可以说是模块，attendances是项目文件存放一些项目配置，static静态文件，attendances.xml是uWsgi的配置文件，requirements.txt是一些项目相关的依赖，test.py是为了测试uWsgi是否配置成功的文件。
#### 6. 创建一个可以使用的模型以及Serializer类、Django视图。
**在apps/user/models.py创建User模型**
``` python {.line-numbers}
"""
用户模块
"""
from django.db import models, transaction

class User(models.Model):
    """
    用户信息表
    """
    user_id = models.AutoField(primary_key=True, verbose_name='用户id')
    user_guid = models.CharField(max_length=150, verbose_name='用户guid')
    user_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name='用户名')
    real_name = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='真实姓名')
    avatar = models.CharField(
        max_length=250, blank=True, null=True, verbose_name='头像')
    mobile = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='手机')
    balance = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='账户余额')
    available_balance = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='可用金额')
    frozen_balance = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='冻结金额')
    all_balance = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='累计金额')
    wx_open_id = models.CharField(max_length=150, verbose_name='微信OpenID')
    wx_union_id = models.CharField(
        max_length=150, blank=True, null=True, verbose_name='微信UnionID')
    create_date = models.FloatField(blank=True, null=True, verbose_name='创建时间')
    last_login_date = models.FloatField(
        blank=True, null=True, verbose_name='最后登录时间')
    ip_address = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='IP地址')
    gender = models.IntegerField(blank=True, null=True, verbose_name='性别')
    province = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='省份')
    city = models.CharField(
        max_length=50, blank=True, null=True, verbose_name='城市')
    session_key = models.CharField(
        max_length=150, blank=True, null=True, verbose_name='会话秘钥')
    is_notify = models.IntegerField(blank=True, null=True, verbose_name='是否开启打卡通知')

    @classmethod
    def update_user_balance(cls, user_id, amount):
        # 手动让select for update和update语句发生在一个完整的事务里面
        with transaction.atomic():
            user = (
                cls.objects
                .select_for_update()
                .get(user_id=user_id)
            )
            user.available_balance += amount 
            user.balance = user.available_balance + user.frozen_balance
            if amount > 0:
                user.all_balance += amount
            user.save()
        return user

    class Meta:
        managed = False
        db_table = 'user'
        ordering = ['-create_date']
        verbose_name = '用户'
        verbose_name_plural = '用户'
```
**在apis/api_v1/user/serializers.py创建Serializer类**
``` python {.line-numbers}
"""
用户模块
"""
from rest_framework import serializers
from apps.user.models import User
from apis.api_v1.enum import ErrorCode
from apis.api_v1.base import BaseApi


class GetUserSerializer(serializers.Serializer):
    """
    获取用户信息
    """
    token = serializers.CharField(max_length=150)
    user_id = serializers.IntegerField()

    def get_user(self, validated_data):
        result = dict()
        base_api = BaseApi()
        # 获取用户
        try:
            user = User.objects.get(user_id=validated_data["user_id"])
        except User.DoesNotExist:
            result["error_code"] = ErrorCode.用户不存在.value
            result["error"] = "用户不存在"
            return result
        # 认证
        if not base_api.authenticate_user(validated_data["token"], user.user_guid):
            result["error_code"] = ErrorCode.认证错误.value
            result["error"] = "认证错误"
            return result
        result["nick_name"] = user.user_name
        result["avatar"] = user.avatar
        result["error_code"] = ErrorCode.正确.value
        result["error"] = ""
        return result

```
**在apis/api_v1/user/view.py创建视图**
``` python {.line-numbers}
"""
用户模块
"""
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apis.api_v1.user.serializers import *
from apis.api_v1.enum import ErrorCode


@api_view(['GET', 'POST'])
def user(request):
    """
    GET:获取用户信息
    POST:更新用户信息
    """
    if request.method == 'GET':
        param = dict()
        param["token"] = request.GET.get("token", None)
        param["user_id"] = request.GET.get("user_id", 0)
        serializer = GetUserSerializer(data=param)
        if serializer.is_valid():
            result = serializer.get_user(serializer.validated_data)
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(dict(error_code=ErrorCode.参数错误.value, error=json.dumps(serializer.errors, ensure_ascii=False)), status=status.HTTP_400_BAD_REQUEST)
    # elif request.method == 'POST':
    #     serializer = PostUserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         result = serializer.update_user(serializer.validated_data)
    #         return Response(result, status=status.HTTP_201_CREATED)
    #     return Response(dict(error_code=ErrorCode.参数错误.value, error=json.dumps(serializer.errors, ensure_ascii=False)), status=status.HTTP_400_BAD_REQUEST)
```
到目前为止，我们已经完成了一个简单接口的创建，接下来可以对项目进行测试
#### 4. 测试我们的Web API。首先启动一个开发服务器，之后在浏览器里输入地址访问我们的接口。
启动开发服务器
``` shell {.line-numbers}
python manage.py runserver

Validating models...

0 errors found
Django version 2.0, using settings 'attendances.settings'
Development server is running at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
在浏览器里输入接口地址，获取到接口数据：http://127.0.0.1:8000/api/v1/user/?token=21cd4161-2a78-451e-8979-5fbd8538935e&user_id=4
``` python {.line-numbers}
GET /api/v1/user/?token=21cd4161-2a78-451e-8979-5fbd8538935e&user_id=4
```
``` python {.line-numbers}
HTTP 201 Created
Allow: POST, GET, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "nick_name": "Band",
    "avatar": "http://wx.qlogo.cn/mmopen/vi_32/aSKcBBPpibyKNicHNTMM0qJVh8Kjgiak2AHWr8MHM4WgMEm7GFhsf8OYrySdbvAMvTsw3mo8ibKicsnfN5pRjl1p8HQ/0",
    "error_code": 0,
    "error": ""
}
```
### 二、相关问题说明
#### 1. 在配置文件里记得修改成本地时区以及将语言设置成中文。
``` python {.line-numbers}
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
```
#### 2. 在安装python3之后，使用pip安装依赖的时候记得使用pip3,或者改掉python和pip的。
``` shell {.line-numbers}
$ alias python='/usr/bin/python3'
```
为了不混淆项目，并且大家在项目中遇到的问题可能各不一样，暂时不列出更多的问题，如果有疑问可以留言。
## 第二部分 部署流程以及问题说明
部署的时候建议大家安装docker容器，如果你没有太多的时间了解docker，可以先不用安装，直接按下面的流程去部署，部署的方式都是一样的，只是运行的地方不一样而已。这里就不列出docker的安装以及使用了。
### 一、部署步骤
#### 1. 安装python3
首先安装依赖包。libxml模块是为了让uwsig支持使用“-x"选项，能通过xml文件启动项目
``` shell {.line-numbers}
$ yum gcc-c++
$ yum install wget openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel
$ yum install libxml*
```
下载python3的压缩包之后，解压并安装到/usr/local/python3/路径下，ln命令是为了方便在终端中直接使用python3和pip3命令。
``` shell {.line-numbers}
$ wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz
$ tar -zxvf Python-3.6.3.tar.gz
$ ./configure --prefix=/usr/local/python3
$ make -j2
$ make install -j2
$ ln -s /usr/local/python3/bin/python3.5 /usr/bin/python3
$ ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3
```
#### 2. 安装uWsgi
``` shell {.line-numbers}
$ pip3 install uwsgi
```
为了在终端中使用uwsgi命令，执行以下命令
``` shell {.line-numbers}
$ ln -s /usr/local/python3/bin/uwsgi /usr/bin/uwsgi3
```
编写一个简单的wsgi应用测试uwsgi是否能正常使用,创建一个test.py文件。
``` python {.line-numbers}
# test.py
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return [b"Hello World"] # python3
```
运行uwsgi,http :8000表示使用http协议，端口号为8000，wigi-file则表示要运行的wsgi应用程序文件。
``` shell {.line-numbers}
# test.py
$ uwsgi --http :8000 --wsgi-file test.py
```
uwsgi运行后打开浏览器，访问http://127.0.0.1:8000/ ，或者是相应服务器地址的8000端口，就可以看到hello world 页面了。
#### 3. 安装Django以及项目依赖，通过uWsgi测试项目是否能正常运行
安装依赖
``` shell {.line-numbers}
$ pip3 install django
$ pip3 install djangorestframework
$ pip3 install pycrypto
```
Django通过uWsgi测试，如果能正常浏览则运行成功，静态文件无法访问的话，我们这里先忽略，后面会通过Nginx配置静态资源访问
#### 4. 安装MySQL,也可以直接使用SQLite或PostgreSQL、Oracle数据库，Django支持多种数据库，根据配置安装不同的驱动，本项目采用MySQL，数据表结构以及链接配置请参考文档
``` shell {.line-numbers}
$ pip3 install mysql
$ pip3 install mysql-server
$ pip3 install mysql-devel
```
MySQL的安装可以参考文档：[MySQL 安装 | 菜鸟教程](http://www.runoob.com/mysql/mysql-install.html)
#### 5. 连接uwsgi与Django
该步骤只是检测Django项目能否在uwsgi下运行，下面我们将配置xml的启动配置文件
``` shell {.line-numbers}
$ uwsgi3 --http :8000 --module attendances.wsgi
```
xml的启动配置文件
``` python {.line-numbers}
<uwsgi>
    <socket>127.0.0.1:8000</socket><!-- 内部端口，自定义 -->
        <chdir>/root/web/attendances/attendances</chdir><!-- 项目路径 -->
            <module>attendances.wsgi</module>
                <processes>4</processes> <!-- 进程数 --> 
    <daemonize>uwsgi.log</daemonize><!-- 日志文件 -->
</uwsgi>
```
进入项目执行以下命令
``` shell {.line-numbers}
$ uwsgi3 -x attendances.xml
```
#### 6. 安装nginx
``` shell {.line-numbers}
$ wget http://nginx.org/download/nginx-1.13.7.tar.gz
$ tar -zxvf nginx-1.13.7.tar.gz
$ ./configure
$ make
$ make install
$ nginx
```
通过链接查看nginx是否启动成功:http://192.168.2.110
#### 6. 通过配置nginx.conf文件连接Django、uWsgi与Nginx
在/etc/nginx/nginx.conf修改nginx.conf
``` shell {.line-numbers}
    server {
        listen       80 default_server;#暴露给外部访问的端口
        listen       [::]:80 default_server;
        server_name  127.0.0.1;
	    index  index.py index.html;
        root         /root/web/attendances/attendances;

        location / {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:8000;#外部访问80就转发到内部8000
        }

    	location /static/ {
            alias /root/web/attendances/attendances/static/;#项目静态路径设置
    	}
    }
```
保存nginx.conf执行nginx -t命令先检查配置文件是否有错，没有错就执行以下命令：nginx启动nginx，可以通过链接查看nginx是否启动成功,之前启动过的话重启nginx.
重启nginx
``` shell {.line-numbers}
$ nginx -t
$ nginx -s reload
```
以上步骤都没有出错的话，打开你的浏览器，输入以下链接，记得关闭系统防火墙或者开放8000端口
http://192.168.2.110/api/v1/user/?token=21cd4161-2a78-451e-8979-5fbd8538935e&user_id=4 （请将该ip替换成你的服务器ip）
网站访问成功！
### 二、相关问题说明
#### 1. Nginx和Django静态文件处理
Django项目可以正常打开，但是静态文件引用路径还有问题，在Django开发时Django自己可以正确处理静态文件的路径，但是部署后Nginx去无法找到静态文件路径。

检查Nginx配置文件夹sites-enabled里的nginx-pro文件，确保里面默认的try_files要删掉或者注释掉，否则Nginx会因此检查静态文件是否存在。

将Django的静态文件集中起来，Django为此有专门的工具

现在Django的Settings文件中加上StATIC_ROOT，把静态文件都集中到这个路径下

``` shell
STATIC_ROOT = os.path.join(BASE_DIR, "static/")
```
执行命令

``` shell {.line-numbers}
$ python3 ./manage.py collectstatic
```
这样所有Django前后台的静态文件都会集中到项目文件夹pro下static中，另外nginx-pro其中一个配置location /static即可让Nginx来处理静态内容。
#### 2. Nginx权限问题(Nginx 403 forbidden)
如果nginx用户没有web目录的权限，则会导致该错误。解决办法：修改web目录的读写权限。或者是把nginx的启动用户改成目录的所属用户，重起一下就能解决，在nginx.conf头部加入一行：user  root;因为项目是在root用户下建立的，通过这个用户去访问资源就可以访问。
``` shell
chmod -R 766 /web
```
#### 3. Nginx转发出现错误(502 BAD GATEWAY)

``` shell
$ setsebool -P httpd_can_network_connect 1
```
> 如果访问不了可以查看Nginx下的error.log文件，查看具体的问题，再找解决方法。
## 分享一些中文文档资料
> 有关Python、Django以及Django REST FrameWork的学习可以参考官方文档，以及以下中文文档，在网上找了很久，感觉以下这几个中文文档还是写的很不错的。

[**Python：** 廖雪峰老师Python教程，基于最新的Python 3版本](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)

[**Django：**  The Django Book 2.0--中文版](http://docs.30c.org/djangobook2/index.html)

[**Django REST FrameWork：** Django REST FrameWork中文文档目录](http://www.chenxm.cc/post/299.html)
