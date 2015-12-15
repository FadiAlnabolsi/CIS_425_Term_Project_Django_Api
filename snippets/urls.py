from django.conf.urls import url, include
from django.contrib import admin
from snippets import views

from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'registrations', views.RegistrationListViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.Homepage ),
    url(r'^Application$', views.Application ),
    url(r'^AdminPortal$', views.AdminPortal ),
]