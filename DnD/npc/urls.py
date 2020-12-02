from django.urls import path

from . import views

app_name = 'npc'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('add/', views.add_npc, name="add"),
    path('<int:pk>/', views.DamageHistoryView.as_view(), name="history"),
    path('<int:pk>/edit', views.edit_npc, name="edit"),
    path('<int:pk>/del', views.del_npc, name="delete")
]