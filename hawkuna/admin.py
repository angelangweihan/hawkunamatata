from django.contrib import admin
from django import forms
from hawkuna.models import Category, Subcategory, UserProfile, CurrentProduct, SoldProduct, Review

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
class SubcategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
  
class CurrentProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class SoldProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
class ChatAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here.

admin.site.register(UserProfile)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(CurrentProduct, CurrentProductAdmin)
admin.site.register(SoldProduct, SoldProductAdmin)
admin.site.register(Review)



