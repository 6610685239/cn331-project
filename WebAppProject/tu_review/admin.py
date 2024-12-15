from django.contrib import admin
from .models import *

@admin.register(Dormitory)
class DormitoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'average_rating')

@admin.register(DormReview)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'dormitory', 'user', 'rating', 'created_at')

#study
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_th', 'established_date')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'faculty')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'created_at')

admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(StudyReview, ReviewAdmin)

#resturant
admin.site.register(Restaurant)
admin.site.register(RestaurantReview)