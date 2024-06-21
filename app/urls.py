from django.urls import path

from app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('predictions/', views.predictions_view, name='predictions'),
    path('finalsprediction/', views.finals_prediction_view, name='finalsprediction'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('predict/<int:match_id>/<str:team_1_name>/<str:team_2_name>/', views.predict_view, name='predict'),
    path('logout/', views.logout_view, name='logout')
]