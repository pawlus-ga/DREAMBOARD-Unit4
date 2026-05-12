from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.project_index, name='project-index'),
    path('projects/<int:project_id>/', views.project_detail, name='project-detail'),
    path('projects/create/', views.ProjectCreate.as_view(), name='project-create'),
    path('projects/<int:pk>/update/', views.ProjectUpdate.as_view(), name='project-update'),
    path('projects/<int:pk>/delete/', views.ProjectDelete.as_view(), name='project-delete'),
    path('projects/<int:project_id>/add-scene/',
    views.add_scene,
    name='add-scene'),
    path('equipment/create/', views.EquipmentCreate.as_view(), name='equipment-create'),
    path('equipment/<int:pk>/', views.EquipmentDetail.as_view(), name='equipment-detail'),
    path('equipment/', views.EquipmentList.as_view(), name='equipment-index'),
    path('equipment/<int:pk>/updated/', views.EquipmentUpdate.as_view(), name='equipment-update'),
    path('equipment/<int:pk>/delete/', views.EquipmentDelete.as_view(), name='equipment-delete'),
    path('projects/<int:project_id>/associate-equipment/<int:equipment_id>/', views.associate_equipment, name='associate-equipment'),
    path('projects/<int:project_id>/remove-equipment/<int:equipment_id>/', views.remove_equipment, name='remove-equipment'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', views.profile_detail, name='profile-detail'),
    path('profile/edit/', views.profile_update, name='profile-update'),
    path('profile/delete/', views.profile_delete, name='profile-delete'),

    

]
