"""wip URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url, include
from datainput import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('datainput.urls')),
    url(r'^add_data_form_submission/$', views.add_data_form_submission, name='add_data_form_submission'),
    url(r'^login_attempt/$', views.login_attempt),
    url(r'^add_data/$', views.add_data),
    url(r'^logout/$', views.userlogout),
    url(r'^teach_a_classifier/$', views.which_classifier_to_teach),
    url(r'^visual_rec_teach/$', views.visual_rec_teach),
    url(r'^visual_rec_menu/$', views.visual_rec_menu),
    url(r'^visual_rec_create_classifier_setup/$', views.visual_rec_create_classifier),
    url(r'^visual_rec_create_classifier_setup2/$', views.visual_rec_create_classifier2),
    url(r'^visual_rec_choose_classifier/$', views.choose_classifier),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)