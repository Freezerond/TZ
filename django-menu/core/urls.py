from django.urls import path
from django.views.generic import TemplateView
from core.models import *


def menu_item_context(slug):
    try:
        menu_item = MenuItem.objects.get(slug=slug)
        return {'menu_item': menu_item}
    except MenuItem.DoesNotExist:
        return {'menu_item': None}


urlpatterns = [
    path('', TemplateView.as_view(template_name="base.html"), name='home'),
    path('<slug:menu_item_slug>', TemplateView.as_view(template_name="home.html"), name='menu_item'),
]