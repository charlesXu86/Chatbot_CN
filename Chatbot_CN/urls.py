"""Chatbot_CN URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from Chatbot_Web.impl.views import index, login, logout, register2
from django.urls import path

from Chatbot_Web.impl.view import welcome_view,ie_view,index_ERform_view,tagging_view,dp_view,cws_view,sp_view,semantic_retrieval_view


urlpatterns = [
    # path('', view.hello)
    # path(r'^admin/', admin.site.urls),
    # path(r'index/$', index, name='index'),
    # path('', index_view.index_view),
    path('welcome_view/', welcome_view.welcome_view, name='welcome_view'), # 欢迎页
    path('register/', welcome_view.register, name='register'),   # 注册
    path('do_login/', welcome_view.do_login, name='do_login'),       # 登录
    path('', index, name='index'),   # 首页
    path('cws_view/', cws_view.cws_view, name='cws_view'),   # 中文分词
    path('tagging_view/', tagging_view.tagging_view, name='tagging_view'),   # 词性标注
    path('info_extraction_view/', ie_view.info_extraction_view, name='info_extraction_view'),  # 信息抽取
    path('ER-post/',index_ERform_view.ER_post, name='ER_post'),
    path('dp_view/', dp_view.dp_view, name='dp_view'),  # 句法分析
    path('sp_view/', sp_view.sp_view, name='sp_view'),  # 语义分析
    path('semantic_retrieval_view/', semantic_retrieval_view.semantic_retrieval_view, name='semantic_retrieval_view'), # 信息检索
    path('search/', semantic_retrieval_view.search, name='search'),
    path('logout/', logout, name='logout'),
]
