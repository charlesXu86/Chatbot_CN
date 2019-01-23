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
from Chatbot_Web.impl.views import index, logout
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.contrib import admin
from rest_framework import routers

from Chatbot_Web.impl.view import welcome_view,ie_view,index_ERform_view,tagging_view,dp_view,cws_view,sp_view,semantic_retrieval_view
from Chatbot_Web.impl.view import kg_view, relation_search_view

from Chatbot_Web.impl.view import wx_view     # 接入微信视图跳转

# web interface
from Chatbot_Web.web_interface.test_interface import ReturnJson
# from Chatbot_Web.impl.view import user_view


# router = routers.DefaultRouter()
# router.register('users', user_view.UserViewSet)
# router.register('groups', user_view.GroupViewSet)

urlpatterns = [
    # path('welcome_views/', welcome_view.welcome_views, name='welcome_views'), # 欢迎页
    # path('^', router.urls),
    # path('admin/', admin.site.urls),

    path('', index, name='index'),   # 欢迎页
    path('register/', welcome_view.register, name='register'),   # 注册
    path('do_login/', welcome_view.do_login, name='do_login'),       # 登录
    path('cws_view/', cws_view.cws_view, name='cws_view'),   # 中文分词
    path('tagging_view/', tagging_view.tagging_view, name='tagging_view'),   # 词性标注
    path('info_extraction_view/', ie_view.info_extraction_view, name='info_extraction_view'),  # 信息抽取
    path('ER-post/',index_ERform_view.ER_post, name='ER_post'),
    path('dp_view/', dp_view.dp_page, name='dp_view'),  # 句法分析页面
    path('sp_view/', sp_view.sp_view, name='sp_view'),  # 语义分析页面
    path('semantic_retrieval_view/', semantic_retrieval_view.semantic_retrieval_view, name='semantic_retrieval_view'), # 信息检索页面
    path('search/', semantic_retrieval_view.search, name='search'),     # 语义搜索的搜索方法

    # 知识图谱模块
    path('kg_view/', kg_view.knowledge_graph_view, name='kg_view'),  # kg预览页面
    path('relation_view/', kg_view.relation_search_view, name='relation_view'), # 关系查询页面
    path('search_relation/', relation_search_view.search_relation, name='search_relation'),
    path('entity_view/', kg_view.entity_search_view, name='entity_view'), # 实体查询页面
    path('kg_overview/', kg_view.overview, name='kg_overview'),   # 概览页面


    path('logout/', logout, name='logout'),


    path('weixin/', wx_view.wechat, name='weixin'),    # 接入微信


    # ================= 接口url ===========================
    # web interface
    path('docs/', get_schema_view()),   # 自动化接口文档
    path('api/getjson', ReturnJson.as_view(), name='getjson'),  # 接口测试
    # path('users/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))




 ]
