from rest_framework import routers
from .api import MeasureViewSet

router = routers.DefaultRouter()
router.register('api/measures', MeasureViewSet, 'measures')

urlpatterns = router.urls