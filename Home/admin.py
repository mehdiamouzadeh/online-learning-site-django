from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
from .models import Course,Category,Session,Comment


class SessionAdmin(admin.ModelAdmin):
    # exclude=['username']

    
    def get_queryset(self, request):
        if request.user.is_superuser:
            query = Session.objects.all()
            return query
        elif request.user.is_staff:
            query = Session.objects.filter(username=request.user)
            return query
            
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course" and not request.user.is_superuser:
            kwargs["queryset"] = Course.objects.filter(username=request.user)
            return db_field.formfield(**kwargs)
        return super(SessionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)        
class CourseAdmin(admin.ModelAdmin):
    # exclude=['username']
    def get_queryset(self, request):
        if request.user.is_superuser:
            query = Course.objects.all()
            return query
        elif request.user.is_staff:
            query = Course.objects.filter(username=request.user)
            return query
    def get_exclude(self, request, obj=None):
        excluded = super().get_exclude(request, obj) or [] # get overall excluded fields

        if not request.user.is_superuser: # if user is not a superuser
            return excluded + ['publish']

        return excluded # otherwise return the default excluded fields if any 
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'username':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)

        return super(CourseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    list_display=['name','username','publish']

class CommentAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id
            return db_field.formfield(**kwargs)

        return super(CommentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    list_display = ('user',  'post', 'created_on', 'active')
    # list_filter = ('active', 'created_on')
    # search_fields = ('user', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)               

admin.site.register(Comment,CommentAdmin)
                
admin.site.register(Course,CourseAdmin)
admin.site.register(Category)
admin.site.register(Session,SessionAdmin)