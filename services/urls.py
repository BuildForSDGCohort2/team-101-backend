from rest_framework.routers import DefaultRouter

import services.views as views

router = DefaultRouter()
router.register('category', views.CategoryViewset, basename='category')

urlpatterns = [

] + router.urls
