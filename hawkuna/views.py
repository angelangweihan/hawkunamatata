from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from hawkuna.models import Category, Subcategory, Product, CurrentProduct, UserProfile, User, SoldProduct, Review, Wishlist
from hawkuna.forms import ProductForm, UserForm,  UserUpdateForm, SellerForm, UpdateProductForm, ReviewForm, UpdateReviewForm, UserProfileForm, ProfileUpdateForm
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import JsonResponse
# from pyrebase import pyrebase
from django.shortcuts import render
from operator import attrgetter

"""
General views
"""

def homepage(request):
    context_dict = {}
    context_dict['title'] = 'Welcome'
    #context_dict['recently'] = CurrentProduct.objects.order_by('date')[5]
    
    response = render(request, 'hawkuna/homepage.html', context = context_dict)
    return response


def about(request):
    return render(request,'hawkuna/about.html')


def faq(request):
    return render(request, 'hawkuna/faq.html')


def contact_us(request):
    return render(request, 'hawkuna/contact_us.html')


"""
Search bar view and function
"""
def query_result(request):
    context_dict = {}
    query = ""
    if request.GET:
        query = request.GET['q']
        if 'search_type' in request.GET:
            search_type = request.GET['search_type']
        else:
            search_type = "both"
        context_dict['query'] = str(query)
        context_dict['search_type'] = str(search_type)
    
    product_post = None
    user_post = None
    if (str(query) != ""):
        if str(search_type) == "products":
            product_post = sorted(get_product_queryset(query), key=attrgetter('date'), reverse=True)
        elif str(search_type) == "users":
            user_post = sorted(get_user_queryset(query), key=attrgetter('slug'))
        else:
            product_post = sorted(get_product_queryset(query), key=attrgetter('date'), reverse=True)
            user_post = sorted(get_user_queryset(query), key=attrgetter('slug'))
    else:
        return redirect(reverse('hawkuna:homepage'))

    context_dict['product_post'] = product_post
    context_dict['user_post'] = user_post
    return render(request, 'hawkuna/search.html', context=context_dict)


def get_product_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = CurrentProduct.objects.filter(Q(name__icontains=q))
        otherposts = CurrentProduct.objects.filter(Q(description__icontains=q))
    
    for post in posts:
        queryset.append(post)
                  
    for otherpost in otherposts:
        queryset.append(otherpost)
       
    queryset = list(dict.fromkeys(queryset))
    return queryset
       
def get_user_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        users = UserProfile.objects.filter(Q(slug__icontains=q))
        otherusers = UserProfile.objects.filter(Q(user__first_name__icontains=q))
    
    for user in users:
        queryset.append(user)
                      
    for otheruser in otherusers:
        queryset.append(otheruser)
    
    queryset = list(dict.fromkeys(queryset))
    return queryset
 
 
"""
Showing products, categories, and subcategories
"""

def show_category(request, category_name_slug):
     context_dict = {}
     try:
        category_list = Category.objects.order_by('name')
        context_dict['categories'] = {}
        for cat in category_list:
            context_dict['categories'][cat] = Subcategory.objects.filter(category=cat).order_by('name')
        category_selected = Category.objects.get(slug=category_name_slug)
        context_dict['selected_category']=category_selected
        
        if 'price-min' in request.GET:
            min_price = request.GET['price-min']
        else:
            min_price = 0
        if 'price-max' in request.GET:
            max_price = request.GET['price-max']
        else:
            max_price = 1000
        products = CurrentProduct.objects.filter(category=category_selected).filter(price__gte=min_price).filter(price__lte=max_price).order_by('date')
        context_dict['products']=products
        context_dict['subcategories'] = subCat
        context_dict['category'] = category
     except Category.DoesNotExist:
         context_dict['subcategories'] = None
         context_dict['category'] = None
    
     return render(request, 'hawkuna/category.html', context=context_dict)


def show_sub(request, category_name_slug, subcategory_name_slug):
    context_dict = {}
        
    try:
        subcategory = Subcategory.objects.get(slug=subcategory_name_slug)
        if 'price-min' in request.GET:
            min_price = request.GET['price-min']
        else:
            min_price = 0
        if 'price-max' in request.GET:
            max_price = request.GET['price-max']
        else:
            max_price = 1000
        products = CurrentProduct.objects.filter(subcategory=subcategory).filter(price__gte=min_price).filter(price__lte=max_price).order_by('date')
        context_dict['category'] = subcategory.category
        context_dict['subcategory'] = subcategory
        context_dict['products'] = products
        if request.user.is_anonymous:
            context_dict['user'] = None
        else:
            context_dict['user'] = request.user
            context_dict['profile'] = UserProfile.objects.get(user=context_dict['user'])
            
    except Subcategory.DoesNotExist:
        context_dict['subcategory'] = None
        context_dict['products'] = None
        context_dict['category'] = None
    return render(request,'hawkuna/subcategory.html',context=context_dict)
  
  
def show_product(request, category_name_slug, subcategory_name_slug, product_name_slug):
    context_dict = {}
    if request.user.is_anonymous:
        context_dict['user'] = None
    else:
        context_dict['user'] = request.user
        context_dict['profile'] = UserProfile.objects.get(user=context_dict['user'])
    
    try:
        product = CurrentProduct.objects.get(slug=product_name_slug)
        context_dict['subcategory'] = product.subcategory
        context_dict['category'] = product.category
        context_dict['seller'] = product.seller
        context_dict['product'] = product
        print(context_dict)
    except CurrentProduct.DoesNotExist:
        context_dict['subcategory'] = None
        context_dict['category'] = None
        context_dict['product'] = None
    return render(request,'hawkuna/product.html',context=context_dict)

 
"""
Register
"""
def register(request):
    context_dict = {}
    context_dict['title'] = 'Join hawkuna-matata*'
    
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True

            wishlist = Wishlist(user=profile)
            wishlist.save()

        else:
            print(user_form.errors, profile_form.errors)
            
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    context_dict['user_form'] = user_form
    context_dict['profile_form'] = profile_form
    context_dict['registered'] = registered
    return render(request, 'hawkuna/register.html', context_dict)
    

"""
User Profile view
"""
@login_required  
def view_profile(request, user_name_slug):
    owned = False
    context_dict = {}

    profile = UserProfile.objects.get(slug=user_name_slug)
    if request.user == profile.user:
        owned = True
    else:
        context_dict['otheruser'] = profile.user
    context_dict['address'] = profile.address
    context_dict['city'] = profile.city
    context_dict['postcode'] = profile.postcode
    context_dict['picture'] = profile.picture
    context_dict['isSeller'] = profile.isSeller
    context_dict['date_reg'] = profile.date_reg
    context_dict['owned'] = owned
    context_dict['slug'] = profile.slug
    if profile.isSeller:
        try:
            products = CurrentProduct.objects.filter(seller=profile).order_by('date')
        except CurrentProduct.DoesNotExist:
            products = None
        context_dict['products'] = products
        
        try:
            reviews = Review.objects.filter(seller=profile)
        except Review.DoesNotExist:
            reviews = None
        context_dict['reviews'] = reviews

    return render(request, 'hawkuna/profile.html', context_dict)
   
   
"""
Edit profile view
"""

@login_required
def edit_profile(request, user_name_slug):
    context_dict = {}
    changed = False
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            user_form =form.save()
            custom_form = profile_form.save(commit=False)
            custom_form.user = user_form
            if 'picture' in request.FILES:
                custom_form.picture = request.FILES['picture']
            custom_form.save()
            messages.success(request, f'Your account has been updated!')
            changed = True

    else:
        form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
    
    context_dict['changed'] = changed
    context_dict ['form'] = form
    context_dict['profile_form'] = profile_form
    return render(request, 'hawkuna/edit_profile.html', context_dict)
 

"""
Login view 
"""
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('hawkuna:homepage'))
            else:
                return HttpResponse("Your account is disabled")
            
        else:
            print(f"Invalid login details:{username}, {password}")
            return render(request, 'hawkuna/login.html', {'notlogged': True, })
    else:
        return render(request, 'hawkuna/login.html')
 
 
"""
Successful login with Google Account
"""

def manage(request):
    context_dict = {}
    user = request.user
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            wishlist = Wishlist(user=profile)
            wishlist.save()
            
        
        else:
            print(profile_form.errors)
            
    else:
        profile_form = UserProfileForm()
    
    context_dict['profile_form'] = profile_form
    return render(request, 'hawkuna/manage.html', context_dict)


"""
Logout and change password
"""
        
@login_required
def user_logout(request):
     logout(request)
     return redirect(reverse('hawkuna:homepage'))


@login_required
def change_password(request, user_name_slug):
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return redirect(reverse('hawkuna:homepage'))
        
    context_dict = {}
    changed = False
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password has been updated successfully!')
            user.save()
            changed = True

        else:
            print(form.errors)
    else:
        form = PasswordChangeForm(request.user)
        
    context_dict['changed'] = changed
    context_dict['profile'] = profile
    context_dict['form'] = form
    return render(request, 'hawkuna/change_password.html', context_dict)


"""
Become a seller views
"""

@login_required
def become_a_seller(request, user_name_slug):
    
    context_dict = {'title': 'Join the team'}
    
    user = request.user
    context_dict['username'] = user.username
    profile = UserProfile.objects.get(user=user)
    context_dict['profile'] = profile
    
    if request.method == 'POST':
        form = SellerForm(request.POST)
        listPay = request.POST.keys()
        if 'paypal' in listPay:
            profile.paypal = True
        if 'cash' in listPay:
            profile.cash = True
        if 'bank_transfer' in listPay:
            profile.bank_transfer = True
        
        profile.isSeller = True
        profile.save()
    
    form = SellerForm()
    context_dict['form'] = form
    return render(request, 'hawkuna/become_a_seller.html', context_dict)


def seller_manual(request):
    context_dict = {}
    context_dict['title'] = 'The Seller Manual'
    return render(request, 'hawkuna/seller_manual.html', context_dict)


"""
Profile insights - first for buyers, other for sellers
"""
def past_orders(request, user_name_slug):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    try:
        soldProducts = SoldProduct.objects.filter(buyer=profile)
    except SoldProduct.DoesNotExist:
        soldProducts = None
    context_dict = {}
    context_dict['user'] = user
    context_dict['profile'] = profile
    context_dict['products'] = soldProducts
    return render(request, 'hawkuna/past_orders.html', context_dict)


def current_products(request, user_name_slug):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    try:
        currentProducts = CurrentProduct.objects.filter(seller=profile)
    except CurrentProduct.DoesNotExist:
        currentProducts = None
    
    context_dict = {}
    context_dict['user'] = user
    context_dict['profile'] = profile
    context_dict['products'] = currentProducts
    return render(request, 'hawkuna/current_products.html', context_dict)


def sold_products(request, user_name_slug):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    try:
        soldProducts = SoldProduct.objects.filter(seller=profile)
    except SoldProduct.DoesNotExist:
        soldProducts = None
    
    context_dict = {}
    context_dict['user'] = user
    context_dict['profile'] = profile
    context_dict['products'] = soldProducts
    print(context_dict)
    return render(request, 'hawkuna/sold_products.html', context_dict)

"""
Add a product view
"""

@login_required
def add_product(request, category_name_slug, subcategory_name_slug):
    added = False
    try:
        subcategory = Subcategory.objects.get(slug=subcategory_name_slug)
    except Subcategory.DoesNotExist:
        subcategory = None
        
    if subcategory is None:
        return redirect('/hawkuna/')
        
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    if category is None:
        return redirect('/hawkuna/')
     
    form = ProductForm()
    
    user = request.user.id
    try:
        seller = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return redirect('/hawkuna/')
    
    product = None
    
    if request.method =='POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            if subcategory:
                product = form.save(commit=False)
                product.subcategory = subcategory
                product.category = category
                product.seller = seller
                
                product.save()
                added = True
    
        else:
            print(form.errors)
    else:
        form = ProductForm()
    
    return render(request, 'hawkuna/add_product.html', {'form':form, 'subcategory':subcategory, 'category':category, 'product':product, 'added':added})


"""
Manage and sell products
"""

@login_required
def manage_product(request, category_name_slug, subcategory_name_slug, product_name_slug):
    
    context_dict = {'title': 'Manage your products'}
    
    try:
        product = CurrentProduct.objects.get(slug = product_name_slug)
    except CurrentProduct.DoesNotExist:
        redirect('/hawkuna/')
           
    seller = product.seller
    modif = False
    
    if request.method == 'POST':
        form = UpdateProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            modif = True
        else:
            print(form.errors)
        
    else:
        form = UpdateProductForm(instance = product)
        
    context_dict['form'] = form
    return render(request, 'hawkuna/manage_product.html', {'form':form, 'product':product, 'modif':modif})

def delete_product(request, category_name_slug, subcategory_name_slug, product_name_slug):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    product = get_object_or_404(CurrentProduct, slug=product_name_slug)

    product.delete()
    return redirect(reverse('hawkuna:profile', kwargs={'user_name_slug':profile.slug}))

def sell_product(request, category_name_slug, subcategory_name_slug, product_name_slug):
    context_dict = {'title':'Sell your product'}
    try:
        product = CurrentProduct.objects.get(slug = product_name_slug)
    except CurrentProduct.DoesNotExist:
        product = None
   
    if product is None:
       return redirect('/hawkuna/')

    seller = product.seller
    context_dict['product'] = product
    sold = False
    if request.method == 'POST':
        buyer_name = request.POST.getlist('uname')[0]
        try:
            userb = User.objects.get(username=buyer_name)
            buyer = UserProfile.objects.get(user=userb)
        except User.DoesNotExist:
            context_dict['message'] = 'No user with such name'
            return render(request, 'hawkuna/sell_product.html', context_dict)
        
        newProduct = SoldProduct(name=product.name, subcategory=product.subcategory, category=product.category, description=product.description, price=product.price, image1=product.image1)
        newProduct.seller = seller
        newProduct.buyer = buyer
        newProduct.save()
        sold = True
        product.delete()
    
    context_dict['sold'] = sold
    return render(request, 'hawkuna/sell_product.html', context_dict)

"""
Wishlist, add to wishlist, delete items from wishlist
"""
@login_required
def wishlist(request, user_name_slug):
    user = request.user.id
    try:
        userProfile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        print("you don't have a userprofile")
        return redirect('/reuse/')
    
    try:
        wishlist = Wishlist.objects.get(user=userProfile)
        products = wishlist.products.filter(wishlist=wishlist)
    except Wishlist.DoesNotExist:
        return redirect('/reuse/')
    
    return render(request,'reuse/wishlist.html', {'products': products})

@login_required
def add_to_wishlist(request, category_name_slug, subcategory_name_slug, product_name_slug):
    
    category = get_object_or_404(Category, slug=category_name_slug)
    subcategory = get_object_or_404(Subcategory, slug=subcategory_name_slug)
    product = get_object_or_404(CurrentProduct, slug=product_name_slug)
    
    user = request.user.id
    buyer = get_object_or_404(UserProfile, user=user)

    wishlist = get_object_or_404(Wishlist, user=buyer)
    
    if request.method == 'POST':
        if product:
            wishlist.products.add(product)
            wishlist.save()
            # Change to pop up
            return redirect(reverse('reuse:product', kwargs={'category_name_slug':category_name_slug, 'subcategory_name_slug':subcategory_name_slug, 'product_name_slug':product_name_slug}))
    
    return render(request, 'reuse/product.html', {'category': category, 'subcategory': subcategory, 'product': product})

def remove_from_wishlist(request, user_name_slug, product_name_slug):
    user = request.user.id
    buyer = get_object_or_404(UserProfile, user=user)
    wishlist = get_object_or_404(Wishlist, user=buyer)
    product = get_object_or_404(CurrentProduct, slug=product_name_slug)
    
    if product:
        wishlist.products.remove(product)
    return redirect(reverse('reuse:wishlist', kwargs={'user_name_slug':user_name_slug}))
    

""" 
Reviews 
"""
def leave_a_review(request, product_name_slug):

    context_dict = {'title': 'Leave A Review'}
    completed = False
    try:
        product = SoldProduct.objects.get(slug = product_name_slug)
    except SoldProduct.DoesNotExist:
        redirect('/hawkuna/')
        
    review = None
    
    context_dict['product'] = product
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.seller = product.seller
            review.buyer = product.buyer
            review.product = product
            review.save()
            completed = True
        else:
            print(form.errors)
    
    else:
        form = ReviewForm()
    
    context_dict['review'] = review
    context_dict['completed'] = completed
    context_dict['form'] = form
    return render(request, 'hawkuna/leave_a_review.html', context_dict)

def update_review(request, product_name_slug):
    
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    product = get_object_or_404(SoldProduct, slug=product_name_slug)
    review = get_object_or_404(Review, product=product)
    
    if request.method == 'POST':
       form = UpdateReviewForm(request.POST, request.FILES, instance=review)
       if form.is_valid():
           form.save()
           return redirect(reverse('hawkuna:past_orders', kwargs={'user_name_slug': profile.slug}))
       else:
           print(form.errors)
       
    else:
       form = UpdateReviewForm(instance = review)
       
    return render(request, 'hawkuna/update_review.html', {'form':form, 'review':review, 'product':product})


def delete_review(request, product_name_slug):
    user = request.user
    profile = get_object_or_404(UserProfile, user=user)
    product = get_object_or_404(SoldProduct, slug=product_name_slug)
    review = get_object_or_404(Review, product=product)
    
    review.delete()
    return redirect(reverse('hawkuna:past_orders', kwargs={'user_name_slug': profile.slug}))






            
