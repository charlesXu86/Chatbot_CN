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
# from rest_framework.schemas import get_schema_view
from django.contrib import admin
from rest_framework import routers

from Chatbot_Web.impl.view import welcome_view,ie_view,index_ERform_view,tagging_view,dp_view,cws_view,sp_view,semantic_retrieval_view
from Chatbot_Web.impl.view import word2vec_view
from Chatbot_Web.impl.view import info_extraction_view
from Chatbot_Web.impl.info_extraction import entity_extraction
from Chatbot_Web.impl.info_extraction import event_extraction
from Chatbot_Web.impl.info_extraction import relation_extraction

from Chatbot_Web.impl.view import kg_view, relation_search_view, kg_overview
from Chatbot_Web.impl.view import dialogue_view
from Chatbot_Web.impl.view import settings_view
from Chatbot_Web.impl.view import specification_view
from Chatbot_Web.impl.view import decisions_making_view
from Chatbot_KG.kbqa import question_answering         # 这个在KG大模块下的kb-qa下


from Chatbot_Web.impl.view import dialogue_view
from Chatbot_Web.impl.view import intent_detection_view  # 意图识别
from Chatbot_Web.impl.dialogue import intent_detection   # 意图识别数据交互方法

from Chatbot_Web.impl.view import wx_view     # 接入微信视图跳转



urlpatterns = [
    # path('welcome_views/', welcome_view.welcome_views, name='welcome_views'), # 欢迎页
    # path('^', router.urls),
    # path('admin/', admin.site.urls),


    # ================================== #
    #                                    #
    #         页面跳转                    #
    #                                    #
    # ================================== #
    path('', index, name='index'),   # 欢迎页
    path('register/', welcome_view.register, name='register'),   # 注册
    path('do_login/', welcome_view.do_login, name='do_login'),       # 登录
    path('cws_view/', cws_view.cws_view, name='cws_view'),   # 中文分词
    path('tagging_view/', tagging_view.tagging_page, name='tagging_view'),   # 词性标注
    path('word2vec_view/', word2vec_view.word2vec_view, name='word2vec_view'),    # 词向量

    path('info_extraction_view/', ie_view.info_extraction_view, name='info_extraction_view'),  # 信息抽取
    path('entity_extraction', info_extraction_view.entity_extraction_page, name='entity_extraction'), # 实体抽取页面
    path('event_extraction', info_extraction_view.event_extraction_page, name='event_extraction'), # 实体抽取页面
    path('relation_extraction', info_extraction_view.relation_extraction_page, name='relation_extraction'), # 实体抽取页面
    path('dp_view/', dp_view.dp_page, name='dp_view'),  # 句法分析页面
    path('sp_view/', sp_view.sp_view, name='sp_view'),  # 语义分析页面

    # 人机对话模块
    path('dialogue/', dialogue_view.dialogue_page, name='dialogue'),  # 人机对话页面
    path('intent_detect/', intent_detection_view.intent_view, name='intent_detect'),   # 意图识别
    path('intent_post/', intent_detection.intent_post, name='intent_post'),             # 意图识别数据交互



    path('send_msg/', dialogue_view.send_msg, name='send_msg'),  # 发送消息
    path('get_new_msgs/', dialogue_view.get_new_msgs, name='get_new_msgs'),  # 发送消息

    path('settings/', settings_view.settings_page, name='settings'),  # 系统设置页面
    path('specification/', specification_view.specification_page, name='specification'),  # 系统说明
    path('semantic_retrieval_view/', semantic_retrieval_view.semantic_retrieval_view, name='semantic_retrieval_view'), # 信息检索页面
    path('search/', semantic_retrieval_view.search, name='search'),     # 语义搜索的搜索方法

    # 知识图谱模块
    path('kg_view/', kg_view.knowledge_graph_view, name='kg_view'),  # kg预览页面
    path('search_relation/', relation_search_view.search_relation, name='search_relation'),  # 关系查询
    path('search_entity/', relation_search_view.search_entity, name='search_entity'), # 实体查询页面
    path('qa/', question_answering.question_answering, name='qa'),
    path('decision/', decisions_making_view.decisions_making_page, name='decision'), # 辅助决策页面
    # path('kg_overview/', kg_overview.show_overview, name='kg_overview'),   # 概览页面
    # url(r'^overview', kg_overview.show_overview),

    # path('logout/', logout, name='logout'),


    # path('weixin/', wx_view.wechat, name='weixin'),    # 接入微信


    # ================= 接口url ===========================
    # web interface
    # path('docs/', get_schema_view()),   # 自动化接口文档
    # path('api/getjson', ReturnJson.as_view(), name='getjson'),  # 接口测试
    # path('users/', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('ER-post/',index_ERform_view.ER_post, name='ER_post'),  # 中文分词及词性标注接口
    path('sentence_entity/', entity_extraction.sentence_post, name='sentence_entity'),   # 实体抽取接口
    path('event', event_extraction.event_post, name='event'),   #事件抽取接口
    path('relation', relation_extraction.relation_post, name='relation'),   # 关系抽取接口





    #     ======================     #
    #                                #
    #       包含Api下面的路由          #
    #                                #
    #     ======================     #

    # path('admin/', admin.site.urls),
    path('api/v1/', include("Chatbot_Rest.urls")),   # 包含Chatbot_Rest（接口模块）下的所有url,api接口url
]
