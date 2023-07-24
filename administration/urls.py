from django.urls import path
from administration import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #################
    path('', views.index, name = 'index'),
    path('login_view', views.login_view, name = 'login_view'),
    path('logout_view', views.logout_view, name='logout_view'),
    #################

    ############################ADMIN SIDE###########################
    path('admin_dash', views.admin_dash, name = 'admin_dash'),
    path('admin_dash/subadmin_register', views.subadmin_register, name = 'subadmin_register'),
    path('admin_dash/admin_profile', views.admin_profile, name = 'admin_profile'),
    path('admin_dash/view_subadmin', views.view_subadmin, name = 'view_subadmin'),
    path('admin_dash/edit_subadmin/<int:id>/',views.edit_subadmin, name = 'edit_subadmin'),
    path('admin_dash/delete_subadmin/<int:id>/',views.delete_subadmin, name = 'delete_subadmin'),
    path('admin_dash/address', views.address, name = 'address'),
    path('admin_dash/admin_msg_sent', views.admin_msg_sent, name = 'admin_msg_sent'),
    path('admin_dash/admin_msg_recv', views.admin_msg_recv, name = 'admin_msg_recv'),
    path('admin_dash/admin_msg', views.admin_msg, name = 'admin_msg'),
    path('admin_dash/del_admin_sent/<int:id>/', views.del_admin_sent, name = 'del_admin_sent'),


    #######################################################

    ############################SUB-ADMIN SIDE###########################
    path('subadmin_dash', views.subadmin_dash, name = 'subadmin_dash'),
    path('subadmin_dash/subadmin_profile', views.subadmin_profile, name = 'subadmin_profile'),
    path('subadmin_dash/add_book', views.add_book, name = 'add_book'),
    path('subadmin_dash/view_book', views.view_book, name = 'view_book'),
    path('subadmin_dash/edit_book/<int:id>/',views.edit_book, name = 'edit_book'),
    path('subadmin_dash/delete_book/<int:id>/',views.delete_book, name = 'delete_book'),
    path('subadmin_dash/customer_register', views.customer_register, name = 'customer_register'),
    path('subadmin_dash/view_customer', views.view_customer, name = 'view_customer'),
    path('subadmin_dash/edit_customer/<int:id>/',views.edit_customer, name = 'edit_customer'),
    path('subadmin_dash/delete_customer/<int:id>/',views.delete_customer, name = 'delete_customer'),
    path('subadmin_dash/librarian_register', views.librarian_register, name = 'librarian_register'),
    path('subadmin_dash/view_librarian', views.view_librarian, name = 'view_librarian'),
    path('subadmin_dash/edit_librarian/<int:id>/',views.edit_librarian, name = 'edit_librarian'),
    path('subadmin_dash/delete_librarian/<int:id>/',views.delete_librarian, name = 'delete_librarian'),
    path('subadmin_dash/genre',views.genre, name = 'genre'),
    path('subadmin_dash/delete_genre/<int:id>/',views.delete_genre, name = 'delete_genre'),
    path('subadmin_dash/occupation',views.occupation, name = 'occupation'),
    path('subadmin_dash/delete_occ/<int:id>/',views.delete_occ, name = 'delete_occ'),
    path('subadmin_dash/language',views.language, name = 'language'),
    path('subadmin_dash/delete_lang/<int:id>/',views.delete_lang, name = 'delete_lang'),
    path('subadmin_dash/configure',views.configure, name = 'configure'),
    path('subadmin_dash/subadmin_msg_sent', views.subadmin_msg_sent, name = 'subadmin_msg_sent'),
    path('subadmin_dash/subadmin_msg_recv', views.subadmin_msg_recv, name = 'subadmin_msg_recv'),
    path('subadmin_dash/subadmin_msg', views.subadmin_msg, name = 'subadmin_msg'),
    path('subadmin_dash/del_subadmin_sent/<int:id>/',views.del_subadmin_sent, name = 'del_subadmin_sent'),

    #######################################################

    ############################LIBRARIAN SIDE###########################
    path('librarian_dash', views.librarian_dash, name = 'librarian_dash'),
    path('librarian_dash/customer_view', views.customer_view, name = 'customer_view'),
    path('librarian_dash/view_books', views.view_books, name = 'view_books'),
    path('librarian_dash/libra_profile', views.libra_profile, name = 'libra_profile'),
    path('librarian_dash/issue/<int:id>/', views.issue, name = 'issue'),
    path('librarian_dash/issue_book', views.issue_book, name = 'issue_book'),
    path('librarian_dash/return_book', views.return_book, name = 'return_book'),
    path('librarian_dash/libra_profile', views.libra_profile, name = 'libra_profile'),
    path('librarian_dash/cust_books/<int:id>/', views.cust_books, name = 'cust_books'),
    path('librarian_dash/pay_fine/<int:id>/', views.pay_fine, name = 'pay_fine'),  
    path('librarian_dash/lib_msg_sent', views.lib_msg_sent, name = 'lib_msg_sent'),
    path('librarian_dash/lib_msg_recv', views.lib_msg_recv, name = 'lib_msg_recv'),
    path('librarian_dash/lib_msg', views.lib_msg, name = 'lib_msg'),
    path('librarian_dash/del_lib_sent/<int:id>/',views.del_lib_sent, name = 'del_lib_sent'),  

    #######################################################

    ############################CUSTOMER SIDE###########################
    path('customer_dash', views.customer_dash, name = 'customer_dash'),
    path('customer_dash/books_view', views.books_view, name = 'books_view'),
    path('customer_dash/cust_profile', views.cust_profile, name = 'cust_profile'),
    path('customer_dash/issued_books', views.issued_books, name = 'issued_books'),
    path('customer_dash/reserve_book/<int:id>/', views.reserve_book, name = 'reserve_book'),
    path('customer_dash/genre_search/<int:id>/', views.genre_search, name = 'genre_search'),   
    path('customer_dash/cust_msg_sent', views.cust_msg_sent, name = 'cust_msg_sent'),
    path('customer_dash/cust_msg_recv', views.cust_msg_recv, name = 'cust_msg_recv'),  
    path('customer_dash/cust_msg', views.cust_msg, name = 'cust_msg'),
    path('customer_dash/del_cust_sent/<int:id>/', views.del_cust_sent, name = 'del_cust_sent'),
    #######################################################
    ] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)