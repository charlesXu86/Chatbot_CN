# Tutorial 2: Requests and Response

[src](http://django-rest-framework.org/tutorial/2-requests-and-responses.html) 

从本节我们开始真正接触rest framework的核心部分。首先我们学习一下一些必备知识。

##1. Request Object  ——Request对象

rest framework 引入了一个继承自`HttpRequest`的`Request`对象，该对象提供了对请求的更灵活解析。`request`对象的核心部分是`request.DATA`属性，类似于`request.POST`, 但在使用WEB API时，`request.DATA`更有效。

   request.POST  # Only handles form data.  Only works for 'POST' method.
   request.DATA  # Handles arbitrary data.  Works any HTTP request with content.

##2. Response Object ——Response对象

rest framework引入了一个`Response` 对象，它继承自`TemplateResponse`对象。它获得未渲染的内容并通过内容协商content negotiation 来决定正确的content type返回给client。

    return Response(data)  # Renders to content type as requested by the client.

##3. Status Codes

在views当中使用数字化的HTTP状态码，会使你的代码不宜阅读，且不容易发现代码中的错误。rest framework为每个状态码提供了更明确的标识。例如`HTTP_400_BAD_REQUEST`在`status` module。相比于使用数字，在整个views中使用这类标识符将更好。

##4. 封装API views

在编写API views时，REST Framework提供了两种wrappers：

1. `@api_viwe`decorator for working with *function based* views.
2. `APIView` class for working with *class based* views.

这两种封装器提供了许多功能，例如，确保在view当中能够接收到`Request`实例；往`Response`中增加内容以便内容协商content negotiation 机制能够执行。

封装器也提供一些行为，例如在适当的时候返回`405 Methord Not Allowed`响应；在访问多类型的输入`request.DATA`时，处理任何的`ParseError`异常。

##5. 汇总

我们开始用这些新的组件来写一些views。

我们不在需要`JESONResponse` 类（在前一篇中创建），将它删除。删除后我们开始稍微重构下我们的view

    from rest_framework import status
    from rest_framework.decorators import api_view
    from rest_framework.response import Response
    from snippets.models import Snippet
    from snippets.serializers import SnippetSerializer
    
    @api_view(['GET', 'POST'])
    def snippet_list(request):
        """
        List all snippets, or create a new snippet.
        """
        if request.method == 'GET':
            snippets = Snippet.objects.all()
            serializer = SnippetSerializer(snippets)
            return Response(serializer.data)
    
        elif request.method == 'POST':
            serializer = SnippetSerializer(data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

上面的代码是对我们之前代码的改进。看上去更简洁，也更类似于django的forms api形式。我们也采用了状态码，使返回值更加明确。
下面是对单个snippet操作的view更新：

    @api_view(['GET', 'PUT', 'DELETE'])
    def snippet_detail(request, pk):
        """
        Retrieve, update or delete a snippet instance.
        """              
        try:
            snippet = Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
        if request.method == 'GET':
            serializer = SnippetSerializer(snippet)
            return Response(serializer.data)
    
        elif request.method == 'PUT':
            serializer = SnippetSerializer(snippet, data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        elif request.method == 'DELETE':
            snippet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

注意，我们并没有明确的要求requests或者responses给出content type。`request.DATA`可以处理输入的`json`请求，也可以输入`yaml`和其他格式。类似的在response返回数据时，REST Framework返回正确的content type给client。

##6. 给URLs增加可选的格式后缀

利用在response时不需要指定content type这一事实，我们在API端增加格式的后缀。使用格式后缀，可以明确的指出使用某种格式，意味着我们的API可以处理类似http://example.com/api/items/4.json.的URL。

增加`format`参数在views中，如：

    def snippet_list(request, format=None):

and

    def snippet_detail(request, pk, format=None):

现在稍微改动`urls.py`文件，在现有的URLs中添加一个格式后缀pattterns (`format_suffix_patterns`):

    from django.conf.urls import patterns, url
    from rest_framework.urlpatterns import format_suffix_patterns
    
    urlpatterns = patterns('snippets.views',
        url(r'^snippets/$', 'snippet_list'),
        url(r'^snippets/(?P<pk>[0-9]+)$', 'snippet_detail'),
    )

urlpatterns = format_suffix_patterns(urlpatterns)
这些额外的url patterns并不是必须的。

##7. How's it looking?

Go ahead and test the API from the command line, as we did in tutorial part 1. Everything is working pretty similarly, although we've got some nicer error handling if we send invalid requests.

We can get a list of all of the snippets, as before.

    curl http://127.0.0.1:8000/snippets/
    [{"id": 1, "title": "", "code": "foo = \"bar\"\n", "linenos": false, "language": "python", "style": "friendly"}, {"id": 2, "title": "", "code": "print \"hello, world\"\n", "linenos": false, "language": "python", "style": "friendly"}]

We can control the format of the response that we get back, either by using the Accept header:

    curl http://127.0.0.1:8000/snippets/ -H 'Accept: application/json'  # Request JSON
    curl http://127.0.0.1:8000/snippets/ -H 'Accept: text/html'         # Request HTML

Or by appending a format suffix:

    curl http://127.0.0.1:8000/snippets/.json  # JSON suffix
    curl http://127.0.0.1:8000/snippets/.api   # Browsable API suffix

Similarly, we can control the format of the request that we send, using the Content-Type header.

    # POST using form data
    curl -X POST http://127.0.0.1:8000/snippets/ -d "code=print 123"
    {"id": 3, "title": "", "code": "123", "linenos": false, "language": "python", "style": "friendly"}
    
    # POST using JSON
    curl -X POST http://127.0.0.1:8000/snippets/ -d '{"code": "print 456"}' -H "Content-Type: application/json"
    {"id": 4, "title": "", "code": "print 456", "linenos": true, "language": "python", "style": "friendly"}

Now go and open the API in a web browser, by visiting http://127.0.0.1:8000/snippets/.

##8. Browsability

Because the API chooses the content type of the response based on the client request, it will, by default, return an HTML-formatted representation of the resource when that resource is requested by a web browser. This allows for the API to return a fully web-browsable HTML representation.

Having a web-browsable API is a huge usability win, and makes developing and using your API much easier. It also dramatically lowers the barrier-to-entry for other developers wanting to inspect and work with your API.

See the [browsable api][browsable api] topic for more information about the browsable API feature and how to customize it.

[browsable api]: http://django-rest-framework.org/topics/browsable-api.html
