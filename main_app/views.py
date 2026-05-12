from django.shortcuts import render, redirect
from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView,TemplateView
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from datetime import datetime
from .models import Project, Equipment, Profile
from .forms import ProjectForm, SceneForm, CustomUserCreationForm, ProfileForm
from django.contrib.auth.views import LoginView


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')


# class Project:
#     def __init__(
#         self, 
#         artist_name,
#         song_title, 
#         description,
#         genre,
#         shoot_date,
#         shoot_days,
#         project_status,
#         payment_status,
#         deliverables_status,
#         requires_social_content,
#         requires_cover_art,
#         requires_photography
#     ):
#         self.artist_name = artist_name
#         self.song_title = song_title
#         self.description = description
#         self.genre = genre
#         self.shoot_date = shoot_date
#         self.shoot_days = shoot_days
#         self.project_status = project_status
#         self.payment_status = payment_status
#         self.deliverables_status = deliverables_status
#         self.requires_social_content = requires_social_content
#         self.requires_cover_art = requires_cover_art
#         self.requires_photography = requires_photography


# projects = [
#     Project(
#         'Kersarge', 'Quick Fling', 'Travel Shoot. Austin, TX.', 
#         'Cloud Rap', datetime(2026, 5, 26), 2, 'pre-production', 'down-payment', 'no content currently', True, False, True
#     ),
#     Project(
#         'Nick Casso', 'Rain', 'Travel Shoot. Denver, CO.', 
#         'R&B', datetime(2026, 6, 12), 3, 'pre-production', 'First-Half', 'no content currently', True, True, True
#     ),
# ]

@login_required
def project_index(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'projects/index.html', {'projects': projects})

@login_required
def project_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    scene_form = SceneForm()

    project_equipment = project.equipment.all()
    available_equipment = Equipment.objects.filter(user=request.user).exclude(
    id__in=project_equipment.values_list('id', flat=True)
    )

    return render(request, 'projects/detail.html', {
        'project': project, 
        'scene_form': scene_form, 
        'project_equipment': project_equipment,
        'available_equipment': available_equipment, })

class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm

class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = '/projects/'

@login_required
def add_scene(request, project_id):
    form = SceneForm(request.POST)
    if form.is_valid():
        new_scene = form.save(commit=False)
        new_scene.project_id = project_id
        new_scene.save()
    return redirect('project-detail', project_id=project_id)

class EquipmentCreate(LoginRequiredMixin, CreateView):
    model = Equipment
    fields = ['name', 'category', 'description', 'owned', 'rental_required', 'notes']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EquipmentList(LoginRequiredMixin, ListView):
    model = Equipment

    def get_queryset(self):
        return Equipment.objects.filter(user=self.request.user)
    

class EquipmentDetail(LoginRequiredMixin, DetailView):
    model = Equipment

    def get_queryset(self):
        return Equipment.objects.filter(user=self.request.user)

class EquipmentUpdate(LoginRequiredMixin, UpdateView):
    model = Equipment
    fields = ['name', 'category', 'description', 'owned', 'rental_required', 'notes']

    def get_queryset(self):
        return Equipment.objects.filter(user=self.request.user)

class EquipmentDelete(LoginRequiredMixin, DeleteView):
    model = Equipment
    success_url = '/equipment/'

    def get_queryset(self):
        return Equipment.objects.filter(user=self.request.user)

@login_required
def associate_equipment(request, project_id, equipment_id):
    Project.objects.get(id=project_id).equipment.add(equipment_id)
    return redirect('project-detail', project_id=project_id)


@login_required
def remove_equipment(request, project_id, equipment_id):
    project = Project.objects.get(id=project_id)
    equipment = Equipment.objects.get(id=equipment_id)

    project.equipment.remove(equipment)

    return redirect('project-detail', project_id=project.id)

class Home(TemplateView):
    template_name = 'home.html'

def signup(request):
    print("SIGNUP VIEW HIT")
    print("REQUEST METHOD:", request.method)
    print("POST DATA:", request.POST)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print("FORM IS VALID:", form.is_valid())
        print("FORM ERRORS:", form.errors)

        if form.is_valid():
            user = form.save()
            print("USER SAVED:", user)

            Profile.objects.create(
                user=user,
                display_name=user.username,
                business_name=form.cleaned_data['business_name'],
                email=form.cleaned_data['email'],
                location=form.cleaned_data['location'],
            )

            login(request, user)
            return redirect('project-index')
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})

@login_required
def profile_detail(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            'display_name': request.user.username,
            'email': request.user.email,
        }
    )
    return render(request, 'profile/detail.html', {'profile': profile})


@login_required
def profile_update(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile-detail')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile/form.html', {'form': form})


@login_required
def profile_delete(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')

    return render(request, 'profile/confirm_delete.html')