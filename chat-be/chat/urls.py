from django.urls import path
from .views import ChatView, DialogView, SchedDialogView


urlpatterns = [
    path('', ChatView.as_view()),
    path('dialog', DialogView.as_view()),
    path('dialog/sched', SchedDialogView.as_view()),
]