# Tutorial 1: 序列化 Serialization

[src](http://django-rest-framework.org/tutorial/1-serialization.html)

##1. 设置一个新的环境

在我们开始之前， 我们首先使用[virtualenv][virtualenv]要创建一个新的虚拟环境，以使我们的配置和我们的其他项目配置彻底分开。


    $mkdir ~/env
    $virtualenv  ~/env/tutorial
    $source ~/env/tutorial/bin/avtivate

现在我们处在一个虚拟的环境中，开始安装我们的依赖包

    $pip install django
    $pip install djangorestframework
    $pip install pygments   ////使用这个包，做代码高亮显示

需要退出虚拟环境时，运行`deactivate`。更多信息，[virtualenv document][virtualenv_doc]

[virtualenv]: http://www.virtualenv.org/en/latest/index.html
[virtualenv_doc]: http://www.virtualenv.org/en/latest/index.html

##2. 开始

环境准备好只好，我们开始创建我们的项目

    $ cd ~
    $ django-admin.py startproject tutorial
    $ cd tutorial

项目创建好后，我们再创建一个简单的app

    $python manage.py startapp snippets

我们使用`sqlite3`来运行我们的项目tutorial，编辑`tutorial/settings.py`, 将数据库的默认引擎`engine`改为`sqlite3`, 数据库的名字`NAME`改为`tmp.db`

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'tmp.db',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

同时更改`settings.py`文件中的`INSTALLD_APPS`,添加我们的APP `snippets`和`rest_framework`

    INSTALLED_APPS = (
        ...
        'rest_framework',
        'snippets',
    )

在`tutorial/urls.py`中，将snippets app的url包含进来

    urlpatterns = patterns('',
        url(r'^', include('snippets.urls')),
    )

##3. 创建Model

这里我们创建一个简单的`snippets` model，目的是用来存储代码片段。

    from django.db import models
    from pygments.lexers import get_all_lexers
    from pygments.styles import get_all_styles
    
    LEXERS = [item for item in get_all_lexers() if item[1]]
    LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
    STYLE_CHOICES = sorted((item, item) for item in get_all_styles())
    
    class Snippet(models.Model):
        created = models.DateTimeField(auto_now_add=True)
        title = models.CharField(max_length=100, default='')
        code = models.TextField()
        linenos = models.BooleanField(default=False)
        language = models.CharField(choices=LANGUAGE_CHOICES,
                                    default='python',
                                    max_length=100)
        style = models.CharField(choices=STYLE_CHOICES,
                                 default='friendly',
                                 max_length=100)
    
        class Meta:
            ordering = ('created',)

完成model时，记得sync下数据库

    python manage.py syncdb

##4. 创建序列化类

我们要使用我们的web api，要做的第一件事就是序列化和反序列化， 以便snippets实例能转换为可表述的内容，例如`json`. 我们声明一个可有效工作的串行器serializer。在`snippets`目录下面，该串行器与django 的表单形式很类似。创建一个`serializers.py` ，并将下面内容拷贝到文件中。

    from django.forms import widgets
    from rest_framework import serializers
    from snippets.models import Snippet
    
    class SnippetSerializer(serializers.Serializer):
        pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
        title = serializers.CharField(required=False,
                                      max_length=100)
        code = serializers.CharField(widget=widgets.Textarea,
                                     max_length=100000)
        linenos = serializers.BooleanField(required=False)
        language = serializers.ChoiceField(choices=models.LANGUAGE_CHOICES,
                                           default='python')
        style = serializers.ChoiceField(choices=models.STYLE_CHOICES,
                                        default='friendly')
    
        def restore_object(self, attrs, instance=None):
            """
            Create or update a new snippet instance.
            """
            if instance:
                # Update existing instance
                instance.title = attrs['title']
                instance.code = attrs['code']
                instance.linenos = attrs['linenos']
                instance.language = attrs['language']
                instance.style = attrs['style']
                return instance
    
            # Create new instance
            return Snippet(**attrs)

该序列化类的前面部分，定义了要序列化和反序列化的类型，`restore_object` 方法定义了如何通过反序列化数据，生成正确的对象实例。

Notice that we can also use various attributes that would typically be used on form fields, such as `widget=widgets.Textarea`. These can be used to control how the serializer should render when displayed as an HTML form. This is particularly useful for controlling how the browsable API should be displayed, as we'll see later in the tutorial.

我们也可以使用`ModelSerializer`来快速生成，后面我们将节省如何使用它。

##5. 使用 Serializers

在我们使用我们定义的SnippetsSerializers之前，我们先熟悉下Snippets. 

    $python manage.py shell

进入shell终端后，输入以下代码：

    from snippets.models import Snippet
    from snippets.serializers import SnippetSerializer
    from rest_framework.renderers import JSONRenderer
    from rest_framework.parsers import JSONParser
    
    snippet = Snippet(code='print "hello, world"\n')
    snippet.save()

我们现在获得了一个Snippets的实例，现在我们对他进行以下序列化

    serializer = SnippetSerializer(snippet)
    serializer.data
    # {'pk': 1, 'title': u'', 'code': u'print "hello, world"\n', 'linenos': False, 'language': u'python', 'style': u'friendly'}

这时，我们将该实例转成了python原生的数据类型。下面我们将该数据转换成`json`格式，以完成序列化：

    content = JSONRenderer().render(serializer.data)
    content
    # '{"pk": 1, "title": "", "code": "print \\"hello, world\\"\\n", "linenos": false, "language": "python", "style": "friendly"}'

反序列化也很简单，首先我们要将一个输入流（content），转换成python的原生数据类型

    import StringIO
    
    stream = StringIO.StringIO(content)
    data = JSONParser().parse(stream)

然后我们将该原生数据类型，转换成对象实例

    serializer = SnippetSerializer(data=data)
    serializer.is_valid()
    # True
    serializer.object
    # <Snippet: Snippet object>

注意这些API和django表单的相似处。这些相似点， 在我们讲述在view中使用serializers时将更加明显。

We can also serialize querysets instead of model instances. To do so we simply add a `many=True` flag to the serializer arguments.

    serializer = SnippetSerializer(Snippet.objects.all(), many=True)
    serializer.data
    # [{'pk': 1, 'title': u'', 'code': u'foo = "bar"\n', 'linenos': False, 'language': u'python', 'style': u'friendly'}, {'pk': 2, 'title': u'', 'code': u'print "hello, world"\n', 'linenos': False, 'language': u'python', 'style': u'friendly'}]

##6. 使用 ModelSerializers

`SnippetSerializer`使用了许多和`Snippet`中相同的代码。如果我们能把这部分代码去掉，看上去将更佳简洁。

类似与django提供`Form`类和`ModelForm`类，Rest Framework也包含了`Serializer` 类和 `ModelSerializer`类。

打开`snippets/serializers.py` ,修改`SnippetSerializer`类：

    class SnippetSerializer(serializers.ModelSerializer):
        class Meta:
            model = Snippet
            fields = ('id', 'title', 'code', 'linenos', 'language', 'style')

##7. 通过Serializer编写Django View

让我们来看一下，如何通过我们创建的serializer类编写django view。这里我们不使用rest framework的其他特性，仅编写正常的django view。

我们创建一个HttpResponse 子类，这样我们可以将我们返回的任何数据转换成`json`。

在`snippet/views.py`中添加以下内容：

    from django.http import HttpResponse
    from django.views.decorators.csrf import csrf_exempt
    from rest_framework.renderers import JSONRenderer
    from rest_framework.parsers import JSONParser
    from snippets.models import Snippet
    from snippets.serializers import SnippetSerializer
    
    class JSONResponse(HttpResponse):
        """
        An HttpResponse that renders it's content into JSON.
        """
        def __init__(self, data, **kwargs):
            content = JSONRenderer().render(data)
            kwargs['content_type'] = 'application/json'
            super(JSONResponse, self).__init__(content, **kwargs)

我们API的目的是，可以通过view来列举全部的Snippet的内容，或者创建一个新的snippet

    @csrf_exempt
    def snippet_list(request):
        """
        List all code snippets, or create a new snippet.
        """
        if request.method == 'GET':
            snippets = Snippet.objects.all()
            serializer = SnippetSerializer(snippets)
            return JSONResponse(serializer.data)
    
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = SnippetSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data, status=201)
            else:
                return JSONResponse(serializer.errors, status=400)

注意，因为我们要通过client向该view post一个请求，所以我们要将该view 标注为`csrf_exempt`, 以说明不是一个CSRF事件。

Note that because we want to be able to POST to this view from clients that won't have a CSRF token we need to mark the view as `csrf_exempt`. This isn't something that you'd normally want to do, and REST framework views actually use more sensible behavior than this, but it'll do for our purposes right now.

我们也需要一个view来操作一个单独的Snippet，以便能更新／删除该对象。


    @csrf_exempt
    def snippet_detail(request, pk):
        """
        Retrieve, update or delete a code snippet.
        """
        try:
            snippet = Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            return HttpResponse(status=404)
    
        if request.method == 'GET':
            serializer = SnippetSerializer(snippet)
            return JSONResponse(serializer.data)
    
        elif request.method == 'PUT':
            data = JSONParser().parse(request)
            serializer = SnippetSerializer(snippet, data=data)
            if serializer.is_valid():
                serializer.save()
                return JSONResponse(serializer.data)
            else:
                return JSONResponse(serializer.errors, status=400)
    
        elif request.method == 'DELETE':
            snippet.delete()
            return HttpResponse(status=204)

将views.py保存，在Snippets目录下面创建`urls.py`,添加以下内容：

    urlpatterns = patterns('snippets.views',
        url(r'^snippets/$', 'snippet_list'),
        url(r'^snippets/(?P<pk>[0-9]+)/$', 'snippet_detail'),
    )

注意我们有些边缘事件没有处理，服务器可能会抛出500异常。

It's worth noting that there are a couple of edge cases we're not dealing with properly at the moment. If we send malformed json, or if a request is made with a method that the view doesn't handle, then we'll end up with a 500 "server error" response. Still, this'll do for now.

##8. 测试

现在我们启动server来测试我们的Snippet。

在python mange.py shell终端下执行（如果前面进入还没有退出）

  quit()

执行下面的命令， 运行我们的server：

    python manage.py runserver

    Validating models...

    0 errors found
    Django version 1.4.3, using settings 'tutorial.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

新开一个terminal来测试我们的server

序列化：

    curl http://127.0.0.1:8000/snippets/
    >>[{"id": 1, "title": "", "code": "print \"hello, world\"\n", "linenos": false, "language": "python", "style": "friendly"}]
    
    curl http://127.0.0.1:8000/snippets/1/
    >>{"id": 1, "title": "", "code": "print \"hello, world\"\n", "linenos": false, "language": "python", "style": "friendly"}

