"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    
    url(r'^rdbms/edit-model.html$', TemplateView.as_view(template_name="rdbms/edit-model.html"), name='rdbms-edit-model'),
    url(r'^rdbms/create-model.html$', TemplateView.as_view(template_name="rdbms/create-model.html"), name='rdbms-create-model'),
    url(r'^rdbms/database-setup.html$', TemplateView.as_view(template_name="rdbms/database-setup.html"), name='rdbms-database-setup'),
    url(r'^rdbms/er.html$', TemplateView.as_view(template_name="rdbms/er.html"), name='rdbms-er'),
    url(r'^rdbms/table.html$', TemplateView.as_view(template_name="rdbms/table.html"), name='rdbms-table'),
    url(r'^rdbms/list.html$', TemplateView.as_view(template_name="rdbms/list.html"), name='rdbms-list'),
    url(r'^rdbms/$', TemplateView.as_view(template_name="rdbms/rdbms.html"), name='rdbms-home'),
    
    url(r'^$', TemplateView.as_view(template_name="index.html"), name='home'),
    
    url(r'^swagger/', include('rest_framework_swagger.urls')),
    url(r'^docs/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.DOCS_STATIC_ROOT,}),
]
