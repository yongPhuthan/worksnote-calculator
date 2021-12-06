"""projectCalculator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from os import name
from django.contrib import admin
from django.urls import path
from django.urls.resolvers import URLPattern
from calculator import views
from django.conf import settings
from django.conf.urls.static import static

# for google login
from django.views.generic import TemplateView 
from django.urls import path, include 
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.home ,name="home"),
    path('', views.select ,name="select"),
    
    # social login
    path('login', views.loginPage, name='login'),
    path('login', auth_views.LoginView.as_view()),

    path('accounts/', include('allauth.urls')),
    path('logout', views.log_out, name='logout'),
    
    
    path('fol_input', views.folding_input ,name="fol_input_page"),
    path('form_input',views.form_input, name='form_input'),
    path('folding/formular', views.folding_formular ,name="folding-formular"),
    path('cost/folding/all',views.folding_allcost, name="fol_all_cost"),
    path('cost/folding', views.folding_cost,  name="fol_cost_add"),
    path('cost/folding/glass', views.glass_cost, name="glass_cost_add"),
    path('cost/folding/other', views.other_cost, name="other_cost_add"),
    path('cost/show', views.folding_cost_show, name="fol_cost_show"),
    path('cost/edit', views.folding_cost_edit, name="fol_cost_edit"),
    path('glas/cost/edit', views.glass_cost_edit, name="glass_cost_edit"),
    path('other/cost/edit', views.other_cost_edit, name="other_cost_edit"),
    path('cost/update/<int:id>', views.folding_cost_update, name="fol_cost_update"),
    path('glass/cost/update/<int:id>', views.glass_cost_update, name="glass_cost_update"),
    path('other/cost/update/<int:id>', views.other_cost_update, name="other_cost_update"),


]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
