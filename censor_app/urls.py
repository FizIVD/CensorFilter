from django.conf import settings
# from django.conf.urls.static import static
from django.urls import path
from .views import CensorFilter, CensorView
from django.views.static import serve
urlpatterns = [
    path('', CensorView.as_view()),
    path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('text/', CensorFilter.as_view()),
]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)