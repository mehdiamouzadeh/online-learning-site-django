from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
user = get_user_model()
from django_currentuser.middleware import (
    get_current_user, get_current_authenticated_user)
# As model field:
from django_currentuser.db.models import CurrentUserField

# Create your models here.
def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.mp4']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

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

class Comment(models.Model):
    post = models.ForeignKey('Course',on_delete=models.CASCADE,verbose_name='مربوط به پست',related_name='comments')
    user = CurrentUserField(verbose_name='کاربر')
    body = models.TextField(verbose_name='متن نظر')
    created_on = models.DateTimeField(auto_now_add=True,verbose_name='اضافه شده در')
    active = models.BooleanField(default=False,verbose_name='وضعیت انتشار')

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user)        


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
    video = models.FileField(upload_to='media/',verbose_name='ویدیوی جلسه',validators=[validate_file_extension])
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