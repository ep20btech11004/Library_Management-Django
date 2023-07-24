from django.contrib import admin
from administration import models

# Register your models here.
admin.site.register(models.Login)
admin.site.register(models.SubAdmin)
admin.site.register(models.Book)
admin.site.register(models.Customer)
admin.site.register(models.Librarian)
admin.site.register(models.Reserve)
admin.site.register(models.Configure)
admin.site.register(models.Organization)
admin.site.register(models.Message)
admin.site.register(models.Genre)
admin.site.register(models.Language)
admin.site.register(models.Occupation)

