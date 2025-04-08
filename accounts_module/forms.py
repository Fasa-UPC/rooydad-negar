from django import forms
from .models import *


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label='نام',
        widget=forms.TextInput()
    )
    last_name = forms.CharField(
        label='نام خانوادگی',
        widget=forms.TextInput()
    )
    student_code = forms.CharField(
        label='شماره دانشجویی',
        widget=forms.TextInput()
    )
    phone_number = forms.CharField(
        label='شماره تماس',
        widget=forms.TextInput()
    )
    entering_year = forms.CharField(
        label='سال ورود',
        widget=forms.TextInput()
    )
    field_of_study = forms.ModelChoiceField(
        label='رشته تحصیلی',
        queryset=Field.objects.all(),
        empty_label=None
    )
    password = forms.CharField(
        label="پسورد",
        widget=forms.TextInput()
    )
    confirm_password = forms.CharField(
        label="تکرار پسورد",
        widget=forms.TextInput()
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password
        else:
            raise forms.ValidationError("رمز عبور های وارد شده یکسان نیستند")

    def clean_student_code(self):
        code = self.cleaned_data.get('student_code')
        check = User.objects.filter(student_code=code).exists()
        if check:
            raise forms.ValidationError("شماره دانشجویی وارد شده متعلق به فرد دیگری است")
        else:
            return code

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        check = User.objects.filter(phone_number=phone).exists()
        if check:
            raise forms.ValidationError("این شماره قبلا ثبت نام کرده است! لطفا وارد شوید")
        else:
            return phone

    def clean_entering_year(self):
        entering_year = self.cleaned_data.get('entering_year')
        if entering_year and 1403 >= int(entering_year) >= 1395:
            return entering_year
        else:
            raise forms.ValidationError("سال وارد شده معتبر نمی‌باشد")

class LoginForm(forms.Form):
    phone_number = forms.CharField(
        label='شماره تماس',
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label="پسورد",
        widget=forms.TextInput()
    )

    # def clean_phone_number(self):
    #     number = int(self.cleaned_data.get('phone_number'))
    #     if isinstance(number, int):
    #         return number
    #     else:
    #         raise forms.ValidationError("لطفا یک شماره وارد کنید")
