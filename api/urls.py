from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SignupViewSet,
    ContactViewSet,
    NewsletterViewSet,
    TrainerViewSet,
    TrainingViewSet,
    ProjectViewSet,
    ArticleViewSet
)


router = DefaultRouter()
router.register(r'signups', SignupViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'newsletters', NewsletterViewSet)
router.register(r'trainers', TrainerViewSet)
router.register(r'trainings', TrainingViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'articles', ArticleViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
