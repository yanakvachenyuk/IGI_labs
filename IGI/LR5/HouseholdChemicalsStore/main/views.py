import os
import calendar
from datetime import date, timedelta,datetime
import logging
import pandas as pd
from django.db.models import Sum, F, Avg
from django.utils import timezone
from statistics import mean, median, mode, StatisticsError
import requests
from django.db.models import Prefetch, Count
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.timezone import get_current_timezone
from django.views.generic import CreateView
from django_pandas.io import read_frame

from HouseholdChemicalsStore import settings
from .forms import CustomUserCreationForm, EmployeeCreationForm, ReviewForm
from .models import news_item, about_company, faq, vacancy, review, promocode, Employee, productType, product, order, \
    orderProduct, pickupPoint, Client

from django.shortcuts import redirect
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt


logger = logging.getLogger(__name__)

def homeView(request):
    try:
        latest_news = news_item.objects.latest('id')
    except news_item.DoesNotExist:
        latest_news = None
    categories = productType.objects.all()
    max_price = request.GET.get('max_price')
    min_price = request.GET.get('min_price')
    category = request.GET.get('category', '')
    search_query = request.GET.get('search', '')
    sort_order = request.GET.get('sort_order', 'asc')

    # Фильтрация
    products = product.objects.all()
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if category:
        products = products.filter(product_type__name=category)
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Сортировка по цене
    if sort_order == 'asc':
        products = products.order_by('price')
    else:
        products = products.order_by('-price')

    pickup_points = pickupPoint.objects.all()

    most_demanded_product = product.objects.annotate(order_count=Count('orderproduct')).order_by('-order_count').first()
    least_demanded_product = product.objects.annotate(order_count=Count('orderproduct')).order_by('order_count').first()

    context = {
        'latest_news': latest_news,
        'categories': categories,
        'products': products,
        'max_price': max_price,
        'min_price': min_price,
        'pickup_points': pickup_points,
        'selected_category': category,
        'search_query': search_query,
        'sort_order': sort_order,
        'most_demanded_product': most_demanded_product,
        'least_demanded_product': least_demanded_product,
    }
    return render(request, 'home.html', context)

def aboutCompanyView(request):
    all_about_company = about_company.objects.all()
    return render(request, 'about_company.html',
    {'all_items':all_about_company})



def contactsView(request):
    employees = Employee.objects.all()
    logger.info('Viewing contacts page')
    return render(request, 'contacts.html', {'employees': employees})


def faqView(request):
    all_dict_of_terms = faq.objects.all()
    return render(request, 'faq.html',
    {'all_items':all_dict_of_terms})

def newsView(request):
    all_news = news_item.objects.all()
    return render(request, 'news.html',
    {'all_items': all_news})

def privacyPolicyView(request):
    return render(request, 'privacy_policy.html')

def promoCouponsView(request):
    all_promocodes = promocode.objects.all()
    return render(request, 'promo_coupons.html',
    {'all_items':all_promocodes})

def reviewsView(request):
    all_reviews = review.objects.all()
    return render(request, 'reviews.html',
    {'all_items':all_reviews})


def vacanciesView(request):
    all_vacancies = vacancy.objects.all()
    return render(request, 'vacancies.html',
    {'all_items':all_vacancies})
# Create your views here.


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class EmployeeSignUp(CreateView):
    form_class = EmployeeCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup_employee.html'

class AddReview(CreateView):
    model = review
    form_class = ReviewForm
    template_name = 'add_review.html'
    success_url = '/reviews/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

def order_create(request):
    promo_code_error = None
    error_message = None
    products = product.objects.all()
    delivery_date = date.today() + timedelta(days=2)
    if request.method == 'POST':
        selected_products = request.POST.getlist('products')
        if not selected_products:
            error_message = 'Вы не выбрали ни одного товара'
            return render(request, 'order_create.html',
                          {'products': products, 'delivery_date': delivery_date, 'error_message': error_message})
        promo_code = request.POST.get('promo_code')

        order_products = []
        for product_id in selected_products:
            quantity = request.POST.get('quantity_' + product_id)
            if quantity:
                product_instance = product.objects.get(pk=product_id)
                # Проверяем, достаточно ли товара на складе
                if product_instance.quantity < int(quantity):
                    error_message = 'Товара ' + product_instance.name + ' недостаточно на складе'
                else:

                    product_instance.quantity -= int(quantity)
                    product_instance.save()  # Сохраняем изменения

                    order_products.append((product_instance, quantity))

        promo = None
        if promo_code:
            try:
                promo = promocode.objects.get(code=promo_code, is_active=True)
            except promocode.DoesNotExist:
                promo_code_error = 'Промокод не найден или не активен'

        if promo_code_error and error_message:
            error_message += ' и ' + promo_code_error
        elif promo_code_error:
            error_message = promo_code_error

        if error_message:
            return render(request, 'order_create.html',
                          {'products': products, 'delivery_date': delivery_date, 'error_message': error_message})

        #custom_sale_date = datetime(2024, 5, 18)

        new_order = order.objects.create(client=request.user.client, sale_date=date.today(), delivery_date=delivery_date)

        for product_instance, quantity in order_products:
            orderProduct.objects.create(order=new_order, product=product_instance, quantity=quantity)

        new_order.update_total_price()

        if promo:
            new_order.total_price -= new_order.total_price * promo.number_of_percents / 100

        new_order.save()

        return redirect('home')
    else:
        return render(request, 'order_create.html',
                      {'products': products, 'delivery_date': delivery_date, 'error_message': error_message})

def orders_history(request):
    logger.debug('Entered orders_history function')
    if request.user.is_authenticated:
        current_client = get_object_or_404(Client, user=request.user)
        orders = order.objects.filter(client=current_client).distinct()
        orders = orders.prefetch_related(Prefetch('orderproduct_set', queryset=orderProduct.objects.select_related('product')))
        logger.info(f'Retrieved order history for client {current_client.id}')
        return render(request, 'orders_history.html', {'orders': orders})

def all_orders_history(request):
    orders = order.objects.prefetch_related('products')

    return render(request, 'all_orders_history.html', {'orders': orders})

def all_clients(request):
    clients = Client.objects.all()
    return render(request, 'all_clients.html', {'clients': clients})

def customers_list(request):
    cities = Client.objects.order_by('city').values_list('city', flat=True).distinct()
    clients_by_city = {city: Client.objects.filter(city=city) for city in cities}
    return render(request, 'customers_list.html', {'clients_by_city': clients_by_city})
def client_profile(request):
    return render(request, 'client_profile.html')


def admin_profile(request):
    return render(request, 'admin_profile.html')

def employee_profile(request):
    return render(request, 'employee_profile.html')

def receipts_for_year(request):
    year = request.GET.get('year', timezone.now().year)
    total_sales_year = product.objects.filter(orderproduct__order__sale_date__year=year).aggregate(
        total_sales=Sum(F('orderproduct__quantity') * F('price')))
    return render(request, 'receipts_for_year.html',{'total_sales_year': total_sales_year, 'year': year})

def monthly_sales_volume(request):
    month = str(request.GET.get('month', timezone.now().month))
    sales_by_product_type = product.objects.filter(orderproduct__order__sale_date__month=month).values(
        'product_type__name').annotate(total_sales=Sum('orderproduct__quantity'))
    return render(request, 'monthly_sales_volume.html', {'sales_by_product_type': sales_by_product_type, 'month': month,})

def weather(request):
    api_key = '23eb69b2555a5daad5add4dac54cc77a'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + api_key
    city = 'Minsk'
    res = requests.get(url.format(city)).json()
    city_info = {
        'city': city,
        'temp': res["main"]["temp"],
        'icon': res["weather"][0]["icon"]
    }

    c = calendar.HTMLCalendar()
    d = datetime.today()
    html_out = c.formatmonth(datetime.today().year, datetime.today().month)

    tz = get_current_timezone()
    stored_date = datetime.now()
    desired_date = stored_date + tz.utcoffset(stored_date)
    timezone_name = desired_date.astimezone().tzinfo

    context = {'info': city_info, 'd': d, 'html_out': html_out,  'timezone': timezone_name,
               'date': desired_date}

    return render(request, 'weather.html', context)

def quotes(request):
    api_key = '7a171d032a6899fd3ad3bad4dc099455'
    url = "https://favqs.com/api/qotd"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        data = {'error': 'Failed to fetch quote of the day'}
    return render(request, 'quotes.html', {'data': data})
def read(request):
    product_types = productType.objects.all()
    return render(request, "crud_product_type.html", {"product_types": product_types})

def create(request):
    if request.method == "POST":
        product_type = productType()
        product_type.name = request.POST.get("name")
        product_type.save()

    return HttpResponseRedirect("/admin_profile")

def update(request, id):
    try:
        product_type = productType.objects.get(id=id)

        if request.method == "POST":
            product_type.name = request.POST.get("name")
            product_type.save()

            return HttpResponseRedirect("/admin_profile")
        else:
            return render(request, "edit_product_type.html", {"product_type": product_type})
    except productType.DoesNotExist:

        return HttpResponseNotFound("<h2>product type not found</h2>")


def delete(request, id):
    try:
        product_type = productType.objects.get(id=id)
        product_type.delete()
        logger.info(f"Product type '{product_type.name}' deleted.")
        return HttpResponseRedirect("/admin_profile")
    except productType.DoesNotExist:
        logger.error(f"Category with id {id} not found.")
        return HttpResponseNotFound("<h2>Category not found</h2>")


def statistics(request):
    # Статистика по товарам
    products = product.objects.annotate(
        total_sales=Sum(F('orderproduct__quantity') * F('price'))
    ).order_by('name')

    total_sales = products.aggregate(total=Sum('total_sales'))['total']

    sales_list = list(filter(None, products.values_list('total_sales', flat=True)))  # filter out None values

    average_sales = mean(sales_list) if sales_list else 0

    median_sales = median(sales_list) if sales_list else 0

    try:
        mode_sales = mode(sales_list)
    except StatisticsError:
        mode_sales = "No mode"

    # Статистика по клиентам
    birth_dates = Client.objects.values_list('date_of_birth', flat=True)
    today = date.today()
    ages = [(today - birth_date).days // 365 for birth_date in birth_dates if
            birth_date is not None]  # check if birth_date is not None

    average_age = mean(ages) if ages else 0
    clients_count = Client.objects.count()

    return render(request, 'statistics.html', {
        'products': products,
        'total_sales': total_sales,
        'average_sales': average_sales,
        'median_sales': median_sales,
        'mode_sales': mode_sales,
        'average_age': average_age,
        'clients_count': clients_count,
    })

def tables_and_charts(request):
    try:
        # Получаем все данные из моделей
        clients = Client.objects.all()
        products = product.objects.all()
        orders = order.objects.all()

        logger.info('Data fetched from database.')

        # Преобразуем QuerySets в DataFrame
        df_clients = read_frame(clients)
        df_products = read_frame(products)
        df_orders = read_frame(orders)

        # Логирование размера датафреймов
        logger.debug(f'df_clients size: {df_clients.shape}')
        logger.debug(f'df_products size: {df_products.shape}')
        logger.debug(f'df_orders size: {df_orders.shape}')

        #диаграмма для клиентов
        client_dict = df_clients['city'].value_counts().to_dict()
        sort_client_dict = {k: v for k, v in sorted(client_dict.items(), key=lambda item: item[1], reverse=True)}
        k = list(sort_client_dict.keys())
        v = list(sort_client_dict.values())
        plt.figure(figsize=(8, 6))
        plt.pie(v, labels=k, autopct=lambda p: f'{p:.1f}%')
        plt.axis('equal')
        save_path1 = os.path.join(settings.MEDIA_ROOT, 'client_diag.png')
        image_path1 = os.path.join(settings.MEDIA_URL, 'client_diag.png')
        plt.savefig(save_path1)
        plt.clf()  # Очищаем текущую фигуру
        logger.info('Client pie chart created.')

        # диаграмма для видов продукции
        product_dict = df_products['product_type'].value_counts().to_dict()
        sort_product_dict = {k: v for k, v in sorted(product_dict.items(), key=lambda item: item[1], reverse=True)}
        k = list(sort_product_dict.keys())
        v = list(sort_product_dict.values())
        plt.figure(figsize=(8, 6))
        plt.pie(v, labels=k, autopct=lambda p: f'{p:.1f}%')
        plt.axis('equal')
        save_path2 = os.path.join(settings.MEDIA_ROOT, 'product_diag.png')
        image_path2 = os.path.join(settings.MEDIA_URL, 'product_diag.png')
        plt.savefig(save_path2)
        plt.clf()
        logger.info('Product pie chart created.')

        #диаграмма для объемов и поступлений от продаж
        sales_dict = df_orders.groupby('client')['total_price'].sum().to_dict()
        sort_sales_dict = {k: v for k, v in sorted(sales_dict.items(), key=lambda item: item[1], reverse=True)}
        k = list(sort_sales_dict.keys())
        v = list(sort_sales_dict.values())
        plt.figure(figsize=(8, 6))
        plt.pie(v, labels=k, autopct=lambda p: f'{p:.1f}%')
        plt.axis('equal')
        save_path3 = os.path.join(settings.MEDIA_ROOT, 'sales_diag.png')
        image_path3 = os.path.join(settings.MEDIA_URL, 'sales_diag.png')
        plt.savefig(save_path3)
        plt.clf()
        logger.info('Sales pie chart created.')

        # Создаем сводные таблицы
        pivot_clients = pd.pivot_table(df_clients, index='city', aggfunc='size').reset_index()
        pivot_clients.columns = ['City', 'Count']

        pivot_products = pd.pivot_table(df_products, index='product_type', aggfunc='size').reset_index()
        pivot_products.columns = ['Product Type', 'Count']

        pivot_sales = pd.pivot_table(df_orders, index='client', values='total_price', aggfunc='sum').reset_index()
        pivot_sales.columns = ['Client', 'Total Price']

        # Преобразуем сводные таблицы в HTML
        clients_html = pivot_clients.to_html()
        products_html = pivot_products.to_html()
        sales_html = pivot_sales.to_html()

        logger.info('Pivot tables created.')

        # Предполагаем, что df_orders содержит данные о продажах
        df_orders['sale_date'] = pd.to_datetime(df_orders['sale_date'])

        # Группировка данных по дате и вычисление суммарных продаж за каждый день
        daily_sales = df_orders.groupby('sale_date')['total_price'].sum().reset_index()

        # Преобразуем даты в числовой формат для модели
        daily_sales['sale_date_ordinal'] = daily_sales['sale_date'].map(datetime.toordinal)

        # Подготовка данных для обучения модели
        X = daily_sales['sale_date_ordinal'].values.reshape(-1, 1)
        y = daily_sales['total_price'].values.reshape(-1, 1)
        y = y.astype('float64')
        logger.debug('Data prepared for model.')

        # Создание и обучение модели
        A = np.vstack([X.T, np.ones(len(X))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]

        # Построение линии тренда
        plt.figure(figsize=(10, 6))
        plt.scatter(daily_sales['sale_date'], y, label='Original data', color='blue')
        plt.plot(daily_sales['sale_date'], m * X + c, 'r', label='Fitted line')

        # Генерируем даты для будущего периода
        future_dates = pd.date_range(start=daily_sales['sale_date'].max(), periods=365).to_pydatetime().tolist()
        future_dates_ordinal = [date.toordinal() for date in future_dates]
        future_dates_ordinal = np.array(future_dates_ordinal).reshape(-1, 1)

        # Предсказываем продажи на эти даты
        future_sales = m * future_dates_ordinal + c

        # Добавляем прогноз продаж на график
        future_dates_dt = [datetime.fromordinal(date) for date in future_dates_ordinal.flatten()]
        plt.plot(future_dates_dt, future_sales, 'g', label='Sales forecast')
        plt.xlabel('Date')
        plt.ylabel('Total Price')
        plt.legend()

        # Сохранение графика в файл
        save_path4 = os.path.join(settings.MEDIA_ROOT, 'sales_forecast.png')
        image_path4 = os.path.join(settings.MEDIA_URL, 'sales_forecast.png')
        plt.savefig(save_path4)
        plt.clf()

        logger.info('Sales forecast chart created.')

        return render(request, 'tables_and_charts.html', {
            'client_chart': image_path1,
            'product_chart': image_path2,
            'sales_chart': image_path3,
            'sales_forecast': image_path4,
            'clients_table': clients_html,
            'products_table': products_html,
            'sales_table': sales_html,
         })
    except Exception as e:
            logger.error(f'Error in tables_and_charts view: {str(e)}')
            return render(request, 'error.html', {'message': 'An error occurred while generating the charts and tables.'})