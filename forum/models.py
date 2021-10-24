from django.db import models
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.template.defaultfilters import slugify
from django.contrib.auth.models import Group, GroupManager, User

class Permission(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class ForumGroup(models.Model):
    group_name = models.CharField(max_length=20, null = False, blank=False)
    color = models.CharField(max_length=7, null=True, blank=True)
    sign = models.CharField(max_length=1, null=True, blank=True)
    slug = models.SlugField(blank=True, null=True)

    permissions = models.ManyToManyField(Permission)
    
    def __str__(self):
        return self.group_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.group_name)
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    group = models.ForeignKey(ForumGroup, on_delete=models.PROTECT, null=True, blank=True)

class Branch(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name
