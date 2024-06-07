from datetime import date

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from django.conf import settings


class news_item(models.Model):
    title = models.CharField(max_length=100, default='')
    content = models.TextField()
    image = models.ImageField(upload_to='images/', default='images/default.png')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title




class about_company(models.Model):
    content = models.TextField()

    class Meta:
        verbose_name = 'О компании'
        verbose_name_plural = 'О компании'



class faq(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Вопрос-ответ'
        verbose_name_plural = 'Вопросы-ответы'



class vacancy(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.title



class review(models.Model):
    name = models.CharField(max_length=100)
    rating = models.IntegerField()
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class promocode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    number_of_percents = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True)
    description = models.TextField()

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды и купоны'

    def __str__(self):
        return self.code


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_description = models.TextField()
    photo = models.ImageField(upload_to='employees', default='employees/employee.jpg')
    phone = models.CharField(max_length=13)
    date_of_birth = models.DateField(null=True, blank=True, default="2000-01-01")
    email = models.EmailField()

    def __str__(self):
        return f'Сотрудник {self.user.username}'

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    email = models.EmailField()
    date_of_birth = models.DateField()
    city = models.CharField(max_length=100, default='Минск')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'Клиент {self.user.username}'


class product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    product_type = models.ForeignKey('productType', on_delete=models.CASCADE)
    manufacturer = models.ForeignKey('manufacturer', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0,validators=[MinValueValidator(1), MaxValueValidator(500)])
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class order(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    products = models.ManyToManyField('product', through='orderProduct')
    sale_date = models.DateField()
    delivery_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return 'Заказ'+str(self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def update_total_price(self):
        total = 0
        for order_product in self.orderproduct_set.all():
            total += order_product.product.price * order_product.quantity
        self.total_price = total
        self.save()

class orderProduct(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE)
    product = models.ForeignKey('product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()



class productType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Вид товаров'
        verbose_name_plural = 'Виды товаров'

    def __str__(self):
        return self.name



class manufacturer(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100,default='Минск')
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Изготовитель'
        verbose_name_plural = 'Изготовители'

    def __str__(self):
        return self.name

class pickupPoint(models.Model):
    address = models.CharField(max_length=200)
    working_hours = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Точка самовывоза'
        verbose_name_plural = 'Точки самовывоза'

    def __str__(self):
        return self.address
