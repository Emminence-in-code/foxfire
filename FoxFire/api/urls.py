from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TaskViewSet,
    CategoryViewSet,
    SurveyViewSet,
    QuestionViewSet,
    UserResponseViewSet,
    SurveyCompletionViewSet,
    AnnouncementViewSet,
    WithdrawRequestViewSet,
    ExchangeRateViewSet,
)

router = DefaultRouter()
router.register(r"tasks", TaskViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"surveys", SurveyViewSet)
router.register(r"questions", QuestionViewSet)
router.register(r"user-responses", UserResponseViewSet)
router.register(r"survey-completions", SurveyCompletionViewSet)
router.register(r"announcements", AnnouncementViewSet)
router.register(r"withdraw-requests", WithdrawRequestViewSet)
router.register(r"exchange-rates", ExchangeRateViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
