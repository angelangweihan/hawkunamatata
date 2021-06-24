from django import forms
from hawkuna.models import Product, CurrentProduct, UserProfile, Category, Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import  UserChangeForm
import re


EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

#Add product 
class ProductForm(forms.ModelForm):
    name = forms.CharField(max_length = 128, help_text="Please enter the name of the product.")
    description = forms.CharField(help_text="Enter short description of the product.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    price = forms.FloatField(help_text="Please enter the price of the product. ", min_value=0)

    class Meta:
        model = CurrentProduct
        exclude=('subcategory', 'category', 'seller',)
 
class ReviewForm(forms.ModelForm):
    title = forms.CharField(max_length = 128, help_text="Title: ")
    text = forms.CharField(help_text="Review: ")
    CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Average'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent')
    )
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    
    class Meta:
        model = Review
        fields = ('title', 'text', 'rating')
   
class UpdateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'text', 'rating')

class UpdateProductForm(forms.ModelForm):
    description=forms.CharField(help_text ="Describe your product: ")
    price = forms.FloatField(help_text="Price of your product: ", min_value=0)
    class Meta:
        model = CurrentProduct
        fields = ( 'image1', 'image2', 'image3', 'image4', 'image5')
    field_order=['description', 'price', 'image1', 'image2', 'image3','image4', 'image5']

class SellerForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('paypal', 'cash', 'bank_transfer',)

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    password2=forms.CharField(widget=forms.PasswordInput())

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError('Invalid email format')
        return email

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password',)


class UserProfileForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = UserProfile
        fields = ('city', 'postcode', 'picture', 'address')
    field_order=['address', 'postcode', 'city', 'picture']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['city', 'postcode', 'picture','address']
    field_order=['address', 'postcode', 'city', 'picture']

