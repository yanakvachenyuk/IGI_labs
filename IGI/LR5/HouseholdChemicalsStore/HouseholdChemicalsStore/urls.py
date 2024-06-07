"""
URL configuration for HouseholdChemicalsStore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from main.views import homeView, aboutCompanyView, contactsView, faqView, newsView, privacyPolicyView, promoCouponsView, \
    reviewsView, vacanciesView, SignUp, EmployeeSignUp, AddReview, order_create, orders_history, all_orders_history, \
    all_clients, customers_list, client_profile, weather, employee_profile, admin_profile, receipts_for_year, \
    monthly_sales_volume, read, create, update, delete, quotes, statistics, tables_and_charts
from django.conf.urls.static import static
from HouseholdChemicalsStore import settings

urlpatterns = [
    re_path('^admin/', admin.site.urls, name='admin'),
    path('', homeView, name='home'),
    re_path(r'^about_company/', aboutCompanyView, name='about_company'),
    re_path(r'^contacts/', contactsView, name='contacts'),
    re_path(r'^faq/', faqView, name='faq'),
    re_path(r'^news/', newsView, name='news'),
    re_path(r'^privacy_policy/', privacyPolicyView, name='privacy_policy'),
    re_path(r'^promo_coupons/', promoCouponsView, name='promo_coupons'),
    re_path(r'^reviews/', reviewsView, name='reviews'),
    re_path(r'^vacancies/', vacanciesView, name='vacancies'),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r"^signup/", SignUp.as_view(), name="signup"),
    re_path(r'^signup_employee/', EmployeeSignUp.as_view(), name='signup_employee'),
    re_path(r'^add_review/', AddReview.as_view(), name='add_review'),
    re_path(r'^order_create/', order_create, name='order_create'),
    re_path(r'^orders_history/', orders_history, name='orders_history'),
    re_path(r'^all_orders_history/', all_orders_history, name='all_orders_history'),
    re_path(r'^all_clients/', all_clients, name='all_clients'),
    re_path(r'^customers_list/', customers_list, name='customers_list'),
    re_path(r'^client_profile/', client_profile, name='client_profile'),
    re_path(r'^weather/',weather, name='weather'),
    re_path(r'^admin_profile',admin_profile, name='admin_profile'),
    re_path(r'^employee_profile',employee_profile, name='employee_profile'),
    re_path(r'^receipts_for_year',receipts_for_year, name='receipts_for_year'),
    re_path(r'^monthly_sales_volume',monthly_sales_volume, name='monthly_sales_volume'),
    path('crud_product_type/', read, name='crud_product_type'),
    re_path('^quotes',quotes, name='quotes'),
    re_path('^statistics', statistics, name='statistics'),
    re_path('^tables_and_charts', tables_and_charts, name='tables_and_charts'),
    re_path(r"^employee_signup/", EmployeeSignUp.as_view(), name="employee_signup"),

    path('create_product_type/', create, name='create_product_type'),
    path('edit_product_type/<int:id>/', update, name='edit_product_type'),
    path('delete_product_type/<int:id>/', delete, name='delete_product_type'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)