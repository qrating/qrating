"""qrating URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from accounts import views as accounts_views
from blog import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.home, name = "home"),
    path('question/<int:pk>', views.detail_question, name = "detail_question"),
    url(r'^create_question/$', views.create_question, name = "create_question"),
    path('question/<int:pk>/remove/', views.question_remove, name='question_remove'),
    path('question/<int:pk>/update/', views.question_update, name='question_update'),
    path('select/<int:qpk>/<int:apk>', views.select_question, name='select_question'),
    path('answer_remove/<int:qpk>/<int:apk>',views.answer_remove, name='answer_remove'),
    path('answer_update/<int:qpk>/<int:apk>',views.answer_update, name='answer_update'),

    path('search', views.search, name='search'),

    # accounts
    url(r'^register/$', accounts_views.register, name='register'),
    url(r'^logout/$', accounts_views.logout, name = 'logout'),
    url(r'^login/$', accounts_views.login, name='login'),
    path('mypage/<int:pk>', accounts_views.mypage, name='mypage'),
    path('change_pw/<int:pk>', accounts_views.change_pw, name='change_pw'),
]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)