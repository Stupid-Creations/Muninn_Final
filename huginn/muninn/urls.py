from django.urls import path,include
from .views import *

urlpatterns = [
    path("home/",homepage,name="home"),
    path("revision/", upload_file,name='upload'),
    path("success/",fd,name = "success"),
    path('flashcard/<int:pk>/', fd, name='card_set'),
    path('quiz/<int:pk>/', quizzer, name='quiz'),
    path('flashcard/',flashmenu,name='Menu'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),  
    path("graded/<int:pk>/",graded,name="graded"),
    path("acc_details/",accountstats, name = "acc"),
]
