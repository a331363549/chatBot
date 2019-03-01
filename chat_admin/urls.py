from django.conf.urls import url
from chat_admin import views

urlpatterns = [
    url(r'^chatter/$', views.user_chat),
    url(r'^index/$', views.index),
    url(r'^delete/.*?$', views.delete_item),
    url(r'^create_kg/$', views.create_KnowledgeGraph),
    url(r'^add_dish/$', views.test_add_dishlist),
    url(r'^test/$', views.test_print),
    # url(r'^userinfo/(?P<pk>[0-9]+)/$', views.user_detail),
    # url(r'^register/$', views.create_user),
    # url(r'^login/$', views.login),
    # url(r'^update/$', views.update_info),
    # url(r'^uploaddata/$', views.upload_data),
    # url(r'^userdata/(?P<pk>[0-9]+)/$', views.show_data),
]
