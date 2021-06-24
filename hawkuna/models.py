from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User



# Create your models here.
# YEYYY Let's build some models


class UserProfile(models.Model):
    # Take from here username, password, email, first:_name, last_name
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    address = models.CharField(max_length = 128)
    city = models.CharField(max_length = 20)
    postcode = models.CharField(max_length = 10)
    description = models.TextField(help_text = "Tell us something about you")
    picture = models.ImageField(upload_to='profile_images', default='profile_images/default-user.png')
    dob = models.DateField(null=True)
    isSeller = models.BooleanField(default = False)
    slug = models.SlugField(unique = True)
    paypal = models.BooleanField(default = False)
    cash = models.BooleanField(default = False)
    bank_transfer = models.BooleanField(default = False)
    date_reg = models.DateField(auto_now_add=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    name = models.CharField(max_length = 128, unique = True)
    slug = models.SlugField(unique = True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "categories"
        
    def __str__(self):
        return self.name
        

class Subcategory(models.Model):
    name = models.CharField(max_length = 128, unique = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    slug = models.SlugField(unique = True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Subcategory, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "subcategories"
        
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length = 128, help_text = "Eg. Notebook")
    subcategory = models.ForeignKey(Subcategory, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete = models.CASCADE)
    description = models.TextField(help_text = "Tell the buyers something about your product")
    price = models.FloatField(default = 0, help_text = "3.50")
    date = models.DateField(auto_now_add=True, blank=True, null=True)
    slug = models.SlugField(unique = True)
    
    image1 = models.ImageField(upload_to='product_images', default='product_images/default.png')
    
    def save(self, *args, **kwargs):
           self.slug = slugify(self.name)
           super(Product, self).save(*args, **kwargs)
        
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.name


class CurrentProduct(Product):
    image2 = models.ImageField(upload_to='product_images', blank = True)
    image3 = models.ImageField(upload_to='product_images', blank = True)
    image4 = models.ImageField(upload_to='product_images', blank = True)
    image5 = models.ImageField(upload_to='product_images', blank = True)
    seller = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name="seller")


class SoldProduct(Product):
    buyer = models.ForeignKey(UserProfile, on_delete=models.SET("This user no longer exists"), blank = False, related_name="buyer" )
    seller = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name="sold_by")


class Review(models.Model):
    title = models.CharField(max_length = 128, help_text = "Insert title here")
    text = models.TextField(help_text = "Tell us how the seller was")
    product = models.OneToOneField(SoldProduct, on_delete=models.SET("This product no longer exists"))
    seller = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="reviewed")
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="reviewer")
    on_date = models.DateField(auto_now_add=True, blank=True, null=True)
    rating = models.IntegerField(blank = False)
    def __str__(self):
        return self.title
        

class Wishlist(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    products = models.ManyToManyField(CurrentProduct)

class Chat(models.Model):
    user1 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="user2")
    name = models.CharField(max_length = 128, unique = True)
    slug = models.SlugField(unique = True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Chat, self).save(*args, **kwargs)

class Message(models.Model):
    text = models.TextField(help_text = "Type your message here")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


