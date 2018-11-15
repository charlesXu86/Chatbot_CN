# Tutorial 6:ViewSets & Routers

REST framework包含一个抽象概念来处理`ViewSets`，它使得开发者可以集中精力对
API的state和interactions建模，留下URL构造被自动处理，基于共同约定。

`ViewSet`类几乎和`View`类一样，除了它们提供像`read`或`update`操作，但没有处理`get`和`put`的方法。

一个`ViewSet`类只是绑定到一组方法处理程序在最后一刻，在它被实例化到一组视图的时候，通常是使用一个`Router`类——为你处理定义URL conf的复杂性。

## 使用ViewSets来重构

让我们取出当前集合的views，使用view sets将它们重构。

首先让我们重构我们的`UserListView`和`UserDetailView`views成一个`UserViewSet`。我们可以移除两个views，用一个类来替换它们。

    class UserViewSet(viewsets.ReadOnlyModelViewSet):
        """
        This viewset automatically provides `list` and `detail` actions.
        """
        queryset = User.objects.all()
        serializer_class = UserSerializer

在这里我们将使用`ReadOnlyModelViewSet类`来自动地提供默认的'read-only'操作。正如我们在使用常规的views做的，我们还是会设置`queryset`和`serializer_class`属性，但我们不再需要提供相同的信息给两个独立的类。

下一步我们将替换`SnippetList`,`SnippetDetial`和`SnippetHighlight`view类。我们可以移除这三个views，再次用一个类来替换它们。

    from rest_framework import viewsets
    from rest_framework.decorators import link
    
    class SnippetViewSet(viewsets.ModelViewSet):
        """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    
        Additionally we also provide an extra `highlight` action. 
        """
        queryset = Snippet.objects.all()
        serializer_class = SnippetSerializer
        permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                              IsOwnerOrReadOnly,)
    
        @link(renderer_classes=[renderers.StaticHTMLRenderer])
        def highlight(self, request, *args, **kwargs):
            snippet = self.get_object()
            return Response(snippet.highlighted)
    
        def pre_save(self, obj):
            obj.owner = self.request.user

这次我们将使用`ModelViewSet`类为了得到默认read和write操作的完整集合。

注意我们还使用`@link`修饰符来创建一个自定义动作名为`highlight`。这个修饰符可以用来添加任何自定义endpoints，不用符合标准的`create`/`update`/`delete`样式。

用`@link`修饰符创建的自定义动作将会对`GET`请亲做出响应。我们也可以使用`@action`修饰符代替如果我们想要一个对`POST`请求做出响应的动作。

## 明确地绑定ViewSets到URLs

handler method仅仅在我们定义URLConf的时候绑定到动作(actions)上。去看看盖子下发生了什么首先从我们的ViewSets明确地创建一个views集合。

在urls.py文件中我们绑定了我们的ViewSet类到一个具体views的集合。

    from snippets.views import SnippetViewSet, UserViewSet
    
    snippet_list = SnippetViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })
    snippet_detail = SnippetViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })
    snippet_highlight = SnippetViewSet.as_view({
        'get': 'highlight'
    })
    user_list = UserViewSet.as_view({
        'get': 'list'
    })
    user_detail = UserViewSet.as_view({
        'get': 'retrieve'
    })

注意我们怎么样从每个ViewSet类创建多样的views，通过绑定http methods到每个view所需的动作(by binding the http methods to the required aciotn for each view)

现在我们已经绑定我们的资源到具体的views，我们可以像往常一样注册views和URL conf。

    urlpatterns = format_suffix_patterns(patterns('snippets.views',
        url(r'^$', 'api_root'),
        url(r'^snippets/$', snippet_list, name='snippet-list'),
        url(r'^snippets/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet-detail'),
        url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highlight'),
        url(r'^users/$', user_list, name='user-list'),
        url(r'^users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail')
    ))

## 使用Routers

因为我们使用`ViewSet`类而不是`View`类，我们实际上不用自己设计URL conf。连接resources到views和urls的约定可以使用`Router`类自动处理。我们要做的仅仅是用一个router注册适当的view集合，and let it do the rest

这里我们重连接`urls.py`文件

    from snippets import views
    from rest_framework.routers import DefaultRouter
    
    # Create a router and register our viewsets with it.
    router = DefaultRouter()
    router.register(r'snippets', views.SnippetViewSet)
    router.register(r'users', views.UserViewSet)
    
    # The API URLs are now determined automatically by the router.
    # Additionally, we include the login URLs for the browseable API.
    urlpatterns = patterns('',
        url(r'^', include(router.urls)),
        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    )
    
用router注册viewsets和提供一个urlpattern很像。我们有两个参数——给views的URL前缀和viewset自身。

`DefaultRouter`类自动为我们创建API root vies，所以我们现在可以从我们的`views`方法中删除`api_root`方法。

## 权衡views VS viewsets

使用viewset可以是一个真正有用的抽象。它帮助确保URL约定可以对你的API始终如一，使你需要编写的代码数量最小化，使得你可以集中精力在你API的交互和表现上，而不是URL conf的细节上。

这并不意味着它总是正确的方法。有一个类似的权衡在使用class-based views代替function-based views上。单独构建views比使用viewsets更加清楚。

回顾我们的工作
如果我们打开浏览器来看看之前的API，会发现它们可以用链接的方式工作了。

当你查看snippet实例的 'highlight' 链接时，你会直接看到代码高亮的HTML呈现。

我们目前已经完成了全套的Web API。可以浏览，支持认证，对象粒度的权限，以及多种返回格式。

我们已经完成了流程中的所有步骤，了解了如何从基本的Django View出发，根据需求逐步定义我们的工作方式。

你能从GitHub上得到教程的最终代码： tutorial code ，或者直接访问在线示例： the sandbox.

##总结与后续工作

我们的教程已经到此结束，如果你还想更多的了解 REST framework，可以从下面这些地方开始：

为 GitHub 做贡献，审查、提交内容或提出新要求。
参加讨论组 REST framework discussion group, 帮助创建更好的线上社区.
Follow the author 作者的 Twitter，打打招呼。
让我们去大展身手吧.

