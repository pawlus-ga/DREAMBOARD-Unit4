from django import forms
from .models import Project, Scene
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'artist_name',
            'song_title',
            'cover_art',
            'description',
            'genre',
            'shoot_date',
            'shoot_days',
            'project_status',
            'payment_status',
            'deliverables_status',
            'requires_social_content',
            'requires_cover_art',
            'requires_photography',
        ]
        exclude = ['equipment']

        widgets = {
            'shoot_date': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
        }

class SceneForm(forms.ModelForm):
    class Meta:
        model = Scene
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    display_name = forms.CharField(max_length=100, required=True)
    business_name = forms.CharField(max_length=150, required=False)
    location = forms.CharField(max_length=100, required=True)
    role = forms.CharField(max_length=100, required=False)
    website = forms.URLField(required=False)
    services_offered = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'business_name', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'display_name',
            'business_name',
            'email',
            'location',
            'role',
            'website',
            'services_offered',
        ]