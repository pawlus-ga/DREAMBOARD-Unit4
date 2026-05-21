from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import User

# user = models.ForeignKey(User, on_delete=models.CASCADE)

# Create your models here.
PROJECT_STATUS = (
    ('pre-production', 'Pre-Production'),
    ('production', 'Production'),
    ('post-production', 'Post-Production'),
    ('completed', 'Completed'),
)

PAYMENT_STATUS = (
    ('no-payment', 'No Payment'),
    ('down-payment', 'Down Payment'),
    ('half-paid', 'Half Paid'),
    ('fully-paid', 'Fully Paid'),
)

DELIVERABLES_STATUS = (
    ('planning-stage', 'Planning Stage'),
    ('content-shot', 'Content Shot'),
    ('editing-stage', 'Editing Stage'),
    ('promotional-content-delivered', 'Promotional Content Delivered'),
    ('accessory-content-delivered', 'Accessory Content Delivered'),
    ('all-content-delivered', 'All Content Delivered'),
)

EQUIPMENT_CATEGORY = (
    ('camera', 'Camera'),
    ('lighting', 'Lighting'),
    ('set_design', 'Set Design'),
    ('props', 'Props'),
    ('camera_accessory', 'Camera Accessory'),
    ('audio', 'Audio'),
    ('stabilization', 'Stabilization'),
    ('backdrop', 'Backdrop'),
    ('other', 'Other'),
)

class Equipment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=50, choices=EQUIPMENT_CATEGORY, blank=True)
    description = models.TextField(blank=True)
    owned = models.BooleanField(default=True)
    rental_required = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('equipment-detail', kwargs={'pk': self.id})


class Project(models.Model):
    artist_name = models.CharField(max_length=150)
    song_title = models.CharField(max_length=150)
    cover_art = models.ImageField(upload_to='project_cover_art/', blank=True, null=True)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=100, blank=True)
    shoot_date = models.DateField(blank=True, null=True)
    shoot_days = models.IntegerField(blank=True, null=True)
    project_status = models.CharField(max_length=50, choices=PROJECT_STATUS, default=PROJECT_STATUS[0][0])
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS, default=PAYMENT_STATUS[0][0])
    deliverables_status = models.CharField(max_length=100, choices=DELIVERABLES_STATUS, default=DELIVERABLES_STATUS[0][0])
    requires_social_content = models.BooleanField(default=False)
    requires_cover_art = models.BooleanField(default=False)
    requires_photography = models.BooleanField(default=False)
    equipment = models.ManyToManyField(Equipment)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.song_title} - {self.artist_name}"

    def get_absolute_url(self):
        return reverse("project-detail", kwargs={'project_id': self.id})
    

class Scene(models.Model):
    scene_title = models.CharField(max_length=200)
    location = models.CharField(
        max_length=150, blank=True)
    mood = models.CharField(
        max_length=150, blank=True)
    notes = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ['scene_title']

    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    display_name = models.CharField(max_length=100, blank=True)
    business_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    services_offered = models.TextField(blank=True)

    def __str__(self):
        return self.display_name
