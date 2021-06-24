from django.urls import path
from hawkuna import views
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin


app_name = 'hawkuna'

urlpatterns = [
    
path('', views.homepage, name='homepage'),
path('about/', views.about, name='about'),
path('faq/', views.faq, name='faq'),
path('contact_us/', views.contact_us, name='contact_us'),
path('login/', views.user_login, name='login'),
path('register/', views.register, name='register'),
path('logout/', views.user_logout, name='logout'),
path('query_result/', views.query_result, name='query_result'),
path('seller_manual/', views.seller_manual, name='seller_manual'),
path('manage/', views.manage, name='manage'),
path('profile/<slug:user_name_slug>/', views.view_profile, name='profile'),
path('profile/<slug:user_name_slug>/become_a_seller/', views.become_a_seller, name='become_a_seller'),
# path('profile/<slug:user_name_slug>/edit_profile/', views.edit_profile, name='edit_profile'),
path('profile/<slug:user_name_slug>/wishlist/', views.wishlist, name='wishlist'),
path('profile/<slug:user_name_slug>/wishlist/<slug:product_name_slug>/remove_from_wishlist/', views.remove_from_wishlist, name='remove_from_wishlist'),
path('profile/<slug:user_name_slug>/change_password/', views.change_password, name='change_password'),
path('profile/<slug:user_name_slug>/past_orders/', views.past_orders, name='past_orders'),
path('profile/<slug:user_name_slug>/sold_products/', views.sold_products, name='sold_products'),
path('profile/<slug:user_name_slug>/current_products/', views.current_products, name='current_products'),
path('cat/<slug:category_name_slug>/', views.show_category, name='show_category'),
path('cat/<slug:category_name_slug>/<slug:subcategory_name_slug>/',views.show_sub, name='show_sub'),
path('cat/<slug:category_name_slug>/<slug:subcategory_name_slug>/add_product/', views.add_product, name='add_product'),
path('cat/<slug:category_name_slug>/<slug:subcategory_name_slug>/<slug:product_name_slug>/', views.show_product, name='product'),
path('cat/<slug:category_name_slug>/<slug:subcategory_name_slug>/<slug:product_name_slug>/manage_product/', views.manage_product, name='manage_product'),
path('cat/<slug:category_name_slug>/<slug:subcategory_name_slug>/<slug:product_name_slug>/sell_product/', views.sell_product, name='sell_product'),
path('cat/<slug:category_name_slug>/<slug:subcategory_name_slug>/<slug:product_name_slug>/delete_product/', views.delete_product, name='delete_product'),
path('sold/<slug:product_name_slug>/leave_a_review/', views.leave_a_review, name='leave_a_review'),
path('sold/<slug:product_name_slug>/update_review/', views.update_review, name='update_review'),
path('sold/<slug:product_name_slug>/delete_review/', views.delete_review, name='delete_review'),
url(r'^admin/', admin.site.urls),


#url(r'^ajax_calls/search/', views.autocompleteModel, name='search'),



    
]
