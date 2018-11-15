#Tutorial 4: Authentication & Permissions

[src](http://django-rest-framework.org/tutorial/4-authentication-and-permissions.html)

目前为止，我们的API对谁能编辑或删除snippet（代码片段）还没有任何限制。我们将增加一些扩展功能来确保以下：

* snippets总关联一个创建者；
* 只有认证后的用户才能创建一个snippets.
* 只有创建者才能更新或删除snippet；
* 非认证请求只拥有只读权限。

##1. 为model增加信息

我们先需要对`Snippet`的model做些修改。首先，增加一些fields. 其中一个用来表示创建者，另一个用来存储代码中的HTML高亮。

在模型中增加这两个字段。

    owner = models.ForeignKey('auth.User', related_name='snippets')
    highlighted = models.TextField()

我们还需要确保model存储时，我们能生成高亮字段内容，这里使用 `pygments` 代码高亮库。

首先需要一些额外的imports:

    from pygments.lexers import get_lexer_by_name
    from pygments.formatters.html import HtmlFormatter
    from pygments import highlight

我们现在为模型增加一个 `.save()` 方法：

    def save(self, *args, **kwargs):
        """
        Use the `pygments` library to create a highlighted HTML
        representation of the code snippet.
        """
        lexer = get_lexer_by_name(self.language)
        linenos = self.linenos and 'table' or False
        options = self.title and {'title': self.title} or {}
        formatter = HtmlFormatter(style=self.style, linenos=linenos,
                                  full=True, **options)
        self.highlighted = highlight(self.code, lexer, formatter)
        super(Snippet, self).save(*args, **kwargs)

 

这些完成后还需要更新一下数据库里面的表。通常我们要创建一个数据库迁移（database migration）来完成，但教程中，我们就只是删除数据库然后重新创建：

    rm tmp.db
    python ./manage.py syncdb 

你可能想创建一些其他用户来测试这些API，最快捷的方式是利用 `createsuperuser` 命令。

    python ./manage.py createsuperuser 

##2. 为用户模型增加endpoints

现在我们需要一些用户，我们最好把用户呈现也增加到API上，创建一个新的serializer很容易：

    from django.contrib.auth.models import User
    
    class UserSerializer(serializers.ModelSerializer):
        snippets = serializers.PrimaryKeyRelatedField(many=True)
    
        class Meta:
            model = User
            fields = ('id', 'username', 'snippets')

因为 `'snippets'` 和用户model是反向关联（reverse relationship，即多对一），所以在使用 `ModelSerializer`时并不会缺省加入，所以我们需要显式的来实现。

我们还需要创建一些views，对用户呈现而言，我们最好使用只读的view，所以使用 `ListAPIView` 和 `RetrieveAPIView` 泛型类Views。

    class UserList(generics.ListAPIView):
        model = User
        serializer_class = UserSerializer
    
    class UserDetail(generics.RetrieveAPIView):
        model = User
        serializer_class = UserSerializer

最后，我们需要修改URL conf：

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()), 

##3. 把Snippets与Users关联

现在，如果我们创建一个code snippet，还没有方法指定其创建者。User并没有作为序列化内容的一部分发送，而是作为request的一个属性。

这里的处理方法是重载snippet view中的 `.pre_save()` 方法，它可以让我们处理request中隐式的信息。

在 `SnippetList` 和 `SnippetDetail` 的view类中，都需要添加如下的方法：

    def pre_save(self, obj):
        obj.owner = self.request.user
 
##4. 更新 serializer

现在snippets已经和创建者关联起来了，我们接下来还需要更新`SnippetSerializer`，在其定义中增加一个新的字段：

    owner = serializers.Field(source='owner.username')

Note: 确定你在嵌入类`Meta`的字段列表中也加入了 `'owner'`。

这个字段所做的十分有趣。`source` 参数表明增加一个新字段，可以指定序列化实例任何属性。它可以采用如上的点式表示（dotted notation），这时他可以直接遍历到指定的属性。在Django's template中使用时，也可以采用类似的方式。

我们增加字段是一个无类型 `Field` 类，而我们之前的字段都是有类型的，例如 `CharField`, `BooleanField` etc... 无类型字段总是只读的，它们只用在序列化表示中，而在反序列化时（修改model）不被使用。 

##5. 给view增加权限控制
现在代码片段 snippets 已经关联了用户，我们需要确保只有认证用户才能增、删、改snippets.

REST framework 包括许多权限类可用于view的控制。这里我们使用 `IsAuthenticatedOrReadOnly`, 它可确保认证的request获取read-write权限，而非认证的request只有read-only 权限.

现需要在views模块中增加 import。

    from rest_framework import permissions
	
然后需要在 `SnippetList` 和 `SnippetDetail` view类中都增加如下属性：

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,) 

##6. 为可浏览API（Browseable API）增加login

如果你打开浏览器，访问可浏览API，你会发现只有登录后才能创建新的snippet了。

我们可以编辑URLconf来增加一个登录view。首先增加新的import：

    from django.conf.urls import include

然后，在文件末尾增加一个pattern来为browsable API增加 login 和 logout views.

    urlpatterns += patterns('',
        url(r'^api-auth/', include('rest_framework.urls',
                                   namespace='rest_framework')),
    )
 

具体的， `r'^api-auth/'` 部分可以用任何你想用的URL来替代。这里唯一的限制就是 urls 必须使用`'rest_framework'` 命名空间。

现在如果你打开浏览器，刷新页面会看到页面右上方的 'Login' 链接。如果你用之前的用户登录后，你就又可以创建 snippets了。

一旦你创建了一些snippets，当导航至'/users/'时，你会看到在每个user的snippets字段都包含了一系列snippet的pk。

##7. 对象级别的权限

我们希望任何人都可以浏览snippets，但只有创建snippet的用户才能编辑或删除它。

为了实现这个需求，我们需要创建定制的权限（custom permission）。

在 snippets 应用中，创建一个新文件： `permissions.py`

    from rest_framework import permissions
    
    class IsOwnerOrReadOnly(permissions.BasePermission):
        """
        Custom permission to only allow owners of an object to edit it.
        """
    
        def has_object_permission(self, request, view, obj):
            # Read permissions are allowed to any request,
            # so we'll always allow GET, HEAD or OPTIONS requests.
            if request.method in permissions.SAFE_METHODS:            
                return True
    
            # Write permissions are only allowed to the owner of the snippet
            return obj.owner == request.user 

现在我们可以为snippet实例增加定制权限了，需要编辑 `SnippetDetail` 类的 `permission_classes` 属性：

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

别忘了import 这个`IsOwnerOrReadOnly` 类。

    from snippets.permissions importIsOwnerOrReadOnly 

现在打开浏览器，你可以看见 'DELETE' 和 'PUT' 动作只会出现在那些你的登录用户创建的snippet页面上了.

##8. 通过API认证

我们已经有了一系列的权限，如果我们需要编辑任何snippet，我们需要认证我们的request。因为我们还没有建立任何 [authentication classes][authentication_class], 所以目前是默认的`SessionAuthentication` 和` BasicAuthentication`在起作用。

[authentication_class]: http://django-rest-framework.org/api-guide/authentication.html

当我们通过Web浏览器与API互动时，我们登录后、然后浏览器session可以为所有的request提供所需的验证。

如果我们使用程序访问这些API，我们则需要显式的为每个request提供认证凭证（authentication credentials）。

如果我们试图未认证就创建一个snippet，将得到错误如下：

    curl -i -X POST http://127.0.0.1:8000/snippets/ -d "code=print 123"
    {"detail": "Authentication credentials were not provided."}
 
如果我们带着用户名和密码来请求时则可以成功创建：

    curl -X POST http://127.0.0.1:8000/snippets/ -d "code=print 789" -u tom:password
    {"id": 5, "owner": "tom", "title": "foo", "code": "print 789", "linenos": false, "language": "python", "style": "friendly"}

##9. 小结

我们已经为我们的Web API创建了相当细粒度的权限控制和相应的系统用户。

在教程第5部分 part 5 ，我们将把所有的内容串联起来，为我们的高亮代码片段创建HTML节点，并利用系统内的超链接关联来提升API的一致性表现。
