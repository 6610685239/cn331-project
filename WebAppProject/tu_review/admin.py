from django.contrib import admin
from .models import *

@admin.register(Dormitory)
class DormitoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'average_rating')

@admin.register(DormRequest)
class DormRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'status', 'created_at')
    list_filter = ('status',)
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        for dorm_request in queryset.filter(status='Pending'):
            Dormitory.objects.create(
                name=dorm_request.name,
                location=dorm_request.location,
                image=dorm_request.image,
                description=dorm_request.description,
            )
            dorm_request.status = 'Approved'
            dorm_request.save()
        self.message_user(request, "Selected requests have been approved.")
    approve_requests.short_description = "Approve selected requests"

    def reject_requests(self, request, queryset):
        queryset.update(status='Rejected')
        self.message_user(request, "Selected requests have been rejected.")
    reject_requests.short_description = "Reject selected requests"


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
admin.site.register(MenuItem)
admin.site.register(RestaurantReview)