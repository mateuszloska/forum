from django.db import models
from django.db.models.fields import TextField
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.template.defaultfilters import slugify
from django.contrib.auth.models import Group, GroupManager, User
from django.db.models.signals import post_save
from django.urls import reverse
from PIL import Image
from django.conf import settings

from django.conf import settings


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
    profile_picture = models.ImageField(upload_to="./profile_pictures", default="./profile_pictures/default.jpg" , blank = True, null=True)

class Branch(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(blank = True, null = True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=50)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='categories')
    slug = models.SlugField(blank=True, null=True)

    def get_total_threads(self):
        return self.threads.all().count()

    def get_total_posts(self):
        counter = 0
        for t in self.threads.all():
            counter += t.get_total_posts()
        return counter

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



class Thread(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='threads')
    slug = models.SlugField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def get_total_posts(self):
        return self.posts.all().count()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('thread')

    def last_message(self):
        return self.posts.last().author.username + " on " + str(self.posts.last().date_created.strftime("%a %m.%Y %H:%M"))

    def save(self,*args,**kwargs):
        super().save(*args, **kwargs)

class Post(models.Model):
    author = ForeignKey(User, on_delete = models.PROTECT, related_name="posts")
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return "Post by "+self.author.username

        
    def get_absolute_url(self):
        return reverse('post')

    def save(self,*args,**kwargs):
        super().save(*args, **kwargs)


#generating unique slugs for categories and branches with the same name
def slug_post_save(sender, instance, created, *args, **kwargs):
    if created:
        instance.slug = slugify(instance.name)
        query = sender.objects.filter(slug = instance.slug).exclude(id=instance.id)
        if query.exists():
            instance.slug = instance.slug + "-" + str(query.count())
        instance.save()


def profile_post_save(sender, instance, created, *args, **kwargs):
    im = Image.open(instance.profile_picture)
    path_to_save = str(settings.MEDIA_ROOT) + '/' + str(instance.profile_picture)
    im1 = im.resize((150,150))
    im1.save(fp = path_to_save)
    if created:
        #Moving automatically to the default user group
        q = ForumGroup.objects.get(group_name = "users")
        instance.group = q
        instance.save()

post_save.connect(profile_post_save, sender=UserProfile)
post_save.connect(slug_post_save, sender=Category)
post_save.connect(slug_post_save, sender=Branch)
post_save.connect(slug_post_save, sender=Thread)

