#Tutorial 5: Relationships & Hyperlinked APIs

[src](http://django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis.html)

到目前为止，在我们的API中关系（relationship）还是通过主键来表示的。在这部分的教程中，我们将用超链接方式来表示关系，从而提升API的统一性和可发现性。

##1. 为API根创建一个endpoint

到目前为止，我们已经有了'snippets'和'users'的endpoint, 但是我们还没有为我们的API单独创立一个端点入口。我们可以用常规的基于函数的view和之前介绍的 `@api_view` 修饰符来创建。

    from rest_framework import renderers
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    from rest_framework.reverse import reverse
    
    @api_view(('GET',))
    def api_root(request, format=None):
        return Response({
            'users': reverse('user-list', request=request, format=format),
            'snippets': reverse('snippet-list', request=request, format=format)
        })

请注意，我们用 REST framework 的 `reverse` 函数来返回完全合规的URLs.

##2. 为高亮的Snippet创建一个endpoint

我们目前还没有为支持代码高亮的Snippet创建一个endpoints.

与之前的API endpoints不同, 我们将直接使用HTML呈现，而非JSON。在 REST framework中有两种风格的HTML render, 一种使用模板来处理HTML，一种则使用预先处理的方式。在这里我们使用后者。

另一个需要我们考虑的是，对于高亮代码的view并没有具体的泛型view可以直接利用。我们将只返回实例的一个属性而不是对象实例本身。

没有具体泛型view的支持，我们使用基类来表示实例，并创建我们自己的 `.get()` 方法。在你的 snippets.views 中增加：

    from rest_framework import renderers
    from rest_framework.response import Response
    
    class SnippetHighlight(generics.SingleObjectAPIView):
        model = Snippet
        renderer_classes = (renderers.StaticHTMLRenderer,)
    
        def get(self, request, *args, **kwargs):
            snippet = self.get_object()
            return Response(snippet.highlighted) 

和以往一样，我们需要为新的view增加新的URLconf，如下增加urlpatterns:

    url(r'^$','api_root'),

还需要为代码高亮增加一个urlpatterns：

    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view()),
 
##3. API超链接化

在Web API设计中，处理实体间关系是一个有挑战性的工作。我们有许多方式来表示关系：

* 使用主键；
* 使用超链接；
* 使用相关实体唯一标识的字段；
* 使用相关实体的默认字符串表示；
* 在父级表示中嵌入子级实体；
* 其他自定义的表示。

REST framework支持所有这些方式，包括正向或者反向的关系，或者将其应用到自定义的管理类中，例如泛型外键。

在这部分，我们使用超链接方式。为了做到这一点，我们需要在序列化器中用 `HyperlinkedModelSerializer` 来替代之前的 `ModelSerializer`.

`HyperlinkedModelSerializer` 与 `ModelSerializer` 有如下的区别:

* 缺省状态下不包含 `pk` 字段；
* 具有一个 `url` 字段，即`HyperlinkedIdentityField`类型.
* 用`HyperlinkedRelatedField`表示关系，而非`PrimaryKeyRelatedField`.
* 我们可以很方便的改写现有代码来使用超连接方式：

    class SnippetSerializer(serializers.HyperlinkedModelSerializer):
        owner = serializers.Field(source='owner.username')
        highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
    
        class Meta:
            model = models.Snippet
            fields = ('url', 'highlight', 'owner',
                      'title', 'code', 'linenos', 'language', 'style')
    
    class UserSerializer(serializers.HyperlinkedModelSerializer):
        snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail')
    
        class Meta:
            model = User
            fields = ('url', 'username', 'snippets')
    
注意：我们也增加了一个新的 `'highlight'` 字段。该字段与 `url` 字段相同类型。不过它指向了 `'snippet-highlight'`的 url pattern, 而非`'snippet-detail'` 的url pattern.

因为我们已经有一个 `'.json'`的后缀，为了更好的表明`highlight`字段链接的区别，使用一个 `'.html'` 的后缀。

##4. 正确使用URL patterns

如果要使用超链接API，就必须确保正确的命名和使用 URL patterns. 我们来看看我们需要命名的 URL patterns：

* 指向 `'user-list'` 和 `'snippet-list'` 的API根.
* snippet的序列化器，包括一个 `'snippet-highlight'`字段.
* user序列化器，包含一个 `'snippet-detail'`字段.
* snippet 和user的序列化器，包含 `'url'` 字段（会缺省指向`'snippet-detail'` 和 `'user-detail'`.

一番工作之后，最终的 `'urls.py'` 文件应该如下所示：

    # API endpoints
    urlpatterns = format_suffix_patterns(patterns('snippets.views',
        url(r'^$', 'api_root'),
        url(r'^snippets/$',
            views.SnippetList.as_view(),
            name='snippet-list'),
        url(r'^snippets/(?P<pk>[0-9]+)/$',
            views.SnippetDetail.as_view(),
            name='snippet-detail'),
        url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
            views.SnippetHighlight.as_view(),
            name='snippet-highlight'),
        url(r'^users/$',
            views.UserList.as_view(),
            name='user-list'),
        url(r'^users/(?P<pk>[0-9]+)/$',
            views.UserDetail.as_view(),
            name='user-detail')
    ))
    
    # Login and logout views for the browsable API
    urlpatterns += patterns('',    
        url(r'^api-auth/', include('rest_framework.urls',
                                   namespace='rest_framework')),
    ) 

##5. 添加分页

列表view有时会返回大量的实例结果，所以我们应该把结果分页显示，以便用户使用。

通过在 `settings.py` 中添加如下配置，我们就能在结果列表中增加分页的功能:

    REST_FRAMEWORK ={'PAGINATE_BY':10}

请注意REST framework的所有配置信息都是存放在一个叫做 'REST_FRAMEWORK'的dictionary中，以便于其他配置区分。

如有必要，你也可以自定义分页的方式，这里不再赘述。

##6. Browsing the API

If we open a browser and navigate to the browsable API, you'll find that you can now work your way around the API simply by following links.

You'll also be able to see the 'highlight' links on the snippet instances, that will take you to the highlighted code HTML representations.

In part 6 of the tutorial we'll look at how we can use ViewSets and Routers to reduce the amount of code we need to build our API.

