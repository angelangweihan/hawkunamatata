from django import template
from django.shortcuts import get_object_or_404
from hawkuna.models import Category, Subcategory, UserProfile, Review, CurrentProduct, SoldProduct, Product

register = template.Library()

@register.inclusion_tag('hawkuna/categories.html')
def get_category_list():
    catlist = {}
    category_list = Category.objects.order_by('name')
    catlist['categories'] = {}
    
    for cat in category_list:
        catlist['categories'][cat] = Subcategory.objects.filter(category=cat).order_by('name')
    
    return catlist

@register.simple_tag
def get_user_name(user):
    try:
        profile = UserProfile.objects.get(user=user)
        name = profile.slug
    except UserProfile.DoesNotExist:
        name = None
    return name

@register.simple_tag
def get_rating(reviews):
    i = 0
    j = 0
    for review in reviews:
        i = i + int(review.rating)
        j = j + 1
    
    rating = i/j
    return rating

@register.simple_tag
def get_review(product):
    try:
        review = Review.objects.get(product=product)
    except Review.DoesNotExist:
        review = None
        
    return review

@register.simple_tag
def get_first_login(user):
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None
        
    return profile


