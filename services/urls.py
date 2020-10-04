from rest_framework.routers import DefaultRouter

import services.views as views

router = DefaultRouter()
router.register('category', views.CategoryViewset, basename='category')
router.register('tag', views.TagViewset, basename='tag')
router.register('item', views.ItemViewset, basename='item')

urlpatterns = router.urls
