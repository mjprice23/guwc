from django.contrib import admin
from .models import Student, MagicalBaby


class MagicalBabyAdmin(admin.ModelAdmin):
    pass

class StudentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Student, StudentAdmin)
admin.site.register(MagicalBaby, MagicalBabyAdmin)
