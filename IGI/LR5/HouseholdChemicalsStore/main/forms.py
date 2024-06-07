
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from datetime import date

from django.core.validators import ValidationError
from django.forms import ModelForm

from main.models import Employee, review, Client


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_regex = r'^\+375(29|33|44|25|17)\d{3}\d{2}\d{2}$'
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, date.today().year)))
    city = forms.CharField(max_length=100)
    phone = forms.CharField(
        validators=[RegexValidator(phone_regex, 'Номер телефона должен быть в формате'
                                                ': +375 (29|33|44|25|17) XXX-XX-XX')])


    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'phone', 'date_of_birth')

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        if (today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))) < 18:
            raise ValidationError('Вам должно быть не менее 18 лет для регистрации.')
        return dob

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()

        #contact.objects.create(
         #   user=user,
          #  phone=self.cleaned_data['phone'],
           # email=self.cleaned_data['email'],
            #date_of_birth=self.cleaned_data['date_of_birth'],
        #)

        Client.objects.create(
            user=user,
            phone=self.cleaned_data['phone'],
            email=self.cleaned_data['email'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            city=self.cleaned_data['city'],
        )

        return user


class EmployeeCreationForm(UserCreationForm):
    job_description = forms.CharField(widget=forms.Textarea)
    photo = forms.ImageField()
    email = forms.EmailField(required=True)
    phone_regex = r'^\+375(29|33|44|25|17)\d{3}\d{2}\d{2}$'
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, date.today().year)))
    phone = forms.CharField(
        validators=[RegexValidator(phone_regex, 'Номер телефона должен быть в формате'
                                                ': +375 (29|33|44|25|17) XXX-XX-XX')])

    class Meta(CustomUserCreationForm.Meta):
        fields = CustomUserCreationForm.Meta.fields + ('job_description', 'photo', 'phone', 'email', 'date_of_birth')

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        if (today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))) < 18:
            raise ValidationError('Вам должно быть не менее 18 лет для регистрации.')
        return dob

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()

        employee = Employee.objects.create(
            user=user,
            job_description=self.cleaned_data['job_description'],
            photo=self.cleaned_data['photo'],
            email=self.cleaned_data['email'],
            phone=self.cleaned_data['phone'],
            date_of_birth=self.cleaned_data['date_of_birth'],
        )
        return employee

class ReviewForm(ModelForm):
    class Meta:
        model = review
        fields = ['name', 'rating', 'text']

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise ValidationError('Оценка должна быть в диапазоне от 1 до 5.')
        return rating

