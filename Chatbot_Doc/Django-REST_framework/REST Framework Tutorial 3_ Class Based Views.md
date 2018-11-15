#Tutorial 3: Class Based Views

[src](http://django-rest-framework.org/tutorial/3-class-based-views.html)

在之前基于函数的View之外，我们还可以用基于类的view来实现我们的API view。正如我们即将看到的那样，这样的方式可以让我们重用公用功能，并使我们保持代码DRY。

用基于类的view重写我们的API
##1. 我们要用基于类的view来重写刚才的根view，如下重构所示：

    from snippets.models import Snippet
    from snippets.serializers import SnippetSerializer
    from django.http import Http404
    from rest_framework.views import APIView
    from rest_framework.response import Response
    from rest_framework import status
    
    class SnippetList(APIView):
        """
        List all snippets, or create a new snippet.
        """
        def get(self, request, format=None):
            snippets = Snippet.objects.all()
            serializer = SnippetSerializer(snippets, many=True)
            return Response(serializer.data)
    
        def post(self, request, format=None):
            serializer = SnippetSerializer(data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

目前看上去不错。它看起来和我们之前写的很相似，但我们在不同的HTTP方法见有了更好的分隔方式，我们还需要把示例的view也重构一下：


    class SnippetDetail(APIView):
        """
        Retrieve, update or delete a snippet instance.
        """
        def get_object(self, pk):
            try:
                return Snippet.objects.get(pk=pk)
            except Snippet.DoesNotExist:
                raise Http404
    
        def get(self, request, pk, format=None):
            snippet = self.get_object(pk)
            serializer = SnippetSerializer(snippet)
            return Response(serializer.data)
    
        def put(self, request, pk, format=None):
            snippet = self.get_object(pk)
            serializer = SnippetSerializer(snippet, data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        def delete(self, request, pk, format=None):
            snippet = self.get_object(pk)
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

做的不错。它和我们之前写的基于函数的view还是有些相像。

我们还需要对URLconf做一些小小的改动：

    from django.conf.urls import patterns, url
    from rest_framework.urlpatterns import format_suffix_patterns
    from snippets import views
    
    urlpatterns = patterns('',
        url(r'^snippets/$', views.SnippetList.as_view()),
        url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
    )
    
    urlpatterns = format_suffix_patterns(urlpatterns)

到目前为止，已经全部完成。你可以运行开发服务器，一切应该表现如初。

##2. 使用mixins

使用基于类的view的最大好处就是可以让我们方便的组合与重用。

刚才我们的create/retrieve/update/delete等函数实现在模型支撑API view下会很类似。其中的公共行为在REST framework's mixin类中实现了。

我们来看看，我们可以用mixin类来吧我们的view组合起来：

    from snippets.models import Snippet
    from snippets.serializers import SnippetSerializer
    from rest_framework import mixins
    from rest_framework import generics
    
    class SnippetList(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):
        model = Snippet
        serializer_class = SnippetSerializer
    
        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)
    
        def post(self, request, *args, **kwargs):
            return self.create(request, *args, **kwargs)

我们将花点时间来解释下这里到底发生了什么。我们用`GenericAPIView`构建了我们的view, 然后加上了`ListModelMixin`和`CreateModelMixin`.

基类提供了核心功能，mixin类提供了 `.list()` 和 `.create()` 动作。我们然后显式的把 `get` 和 `post` 方法与合适的动作绑定在一起，非常简单。

    class SnippetDetail(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        generics.GenericAPIView):
        model = Snippet
        serializer_class = SnippetSerializer
    
        def get(self, request, *args, **kwargs):
            return self.retrieve(request, *args, **kwargs)
    
        def put(self, request, *args, **kwargs):
            return self.update(request, *args, **kwargs)
    
        def delete(self, request, *args, **kwargs):
            return self.destroy(request, *args, **kwargs)

示例部分的实现也非常类似。这次我们用`GenericAPIView`来提供核心功能，然后用mixins来提供`.retrieve()`, `.update()` 和 `.destroy()` actions.

##3. 使用基于泛型类的view

使用mixin类可以让我们重写view时写更少的代码，但我们还可以更进一步，REST framework提供了一系列已经mixed-in的泛型view供我们使用。

    from snippets.models import Snippet
    from snippets.serializers import SnippetSerializer
    from rest_framework import generics
    
    class SnippetList(generics.ListCreateAPIView):
        model = Snippet
        serializer_class = SnippetSerializer
    
    class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
        model = Snippet
        serializer_class = SnippetSerializer

Wow, 非常简洁. 我们轻松了不少，而且代码看起来优美，干净和符合Django的习惯。

在第四部分 part 4 of the tutorial, 我们将看看我们的API如何处理认证和权限。
