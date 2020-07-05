from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
user = get_user_model()
# Create your models here.


class Course(models.Model):
    username = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length = 70)
    # slug = models.SlugField()
    image = models.ImageField(upload_to='media/')
    created = models.DateTimeField(auto_now = True)
    updated = models.DateTimeField(auto_now_add = True)
    description = models.TextField()
    category = models.ForeignKey('Category', verbose_name="Category",on_delete=models.CASCADE)
    publish = models.BooleanField(default=False)
    # tutor = models.ManyToManyField('مربی' , null = True, blank = True , related_name = _('Tutor courses'))


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = ('درس')
        verbose_name_plural = ('درس ها')


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="عنوان دسته بندی")
    class Meta:
        verbose_name = ('دسته بندی')
        verbose_name_plural = ('دسته بندی ها')
    def __str__(self):
        return self.title    

class Session(models.Model):
    username = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=255, verbose_name="عنوان جلسه")
    video = models.FileField(upload_to='media/',verbose_name='ویدیوی جلسه')
    course = models.ForeignKey(Course, verbose_name="مرتبط با کدام دوره",on_delete=models.CASCADE,null=True)
    class Meta:
        verbose_name = ('جلسه دروس')
        verbose_name_plural = ('جلسه های دروس')

    def __str__(self):
        return self.title    

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username         
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()        