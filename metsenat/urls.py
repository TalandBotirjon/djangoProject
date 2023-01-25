from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.SponsorCreateViews.as_view()),
    # Dashboard
    path('dashboard/', views.DashboardViews.as_view()),
    # Sponsor
    path('sponsor/', views.SponsorListViews.as_view()),
    path('sponsor/<int:pk>/detail/', views.SponsorDetailViews.as_view()),
    # Student
    path('student/', views.StudentListViews.as_view()),
    path('student/create/', views.StudentCreateViews.as_view()),
    path('student/<int:pk>/detail/', views.StudentViews.as_view()),
    # Metsenat
    path('metsenat/', views.MentanetViews.as_view()),
]
