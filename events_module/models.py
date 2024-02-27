from django.db import models
from django_jalali.db import models as jmodels
from accounts_module.models import User


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=255, null=True, verbose_name="عنوان رویداد")
    description = models.TextField(null=True, verbose_name="توضیحات رویداد")
    start_date = models.CharField(max_length=255, verbose_name="تاریخ شروع")
    place = models.CharField(max_length=255, null=True, blank=True, verbose_name="محل برگزاری")
    days_of_week = models.TextField(null=True, blank=True, verbose_name="روزهای برگزاری")
    teacher = models.CharField(max_length=250, null=True, verbose_name="نام مدرس")
    price = models.IntegerField(null=True, verbose_name="هزینه رویداد")
    capacity = models.IntegerField(default=0, null=True, verbose_name="ظرفیت دوره")
    image = models.ImageField(upload_to='events', verbose_name="تصویر")
    slug = models.CharField(max_length=255, null=True, verbose_name="لینک")
    status = models.BooleanField(default=False, verbose_name="فعال/غیرفعال")

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "رویداد"
        verbose_name_plural = "رویدادها"


class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="شرکت کننده")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="سمینار")
    date = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت نام")
    status = models.BooleanField(default=False, verbose_name="وضعیت")
    total = models.IntegerField(default=0, verbose_name="هزینه کل")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "شرکت کننده"
        verbose_name_plural = "شرکت کنندگان"


class Discount(models.Model):
    code = models.CharField(max_length=250, null=True, unique=True, verbose_name="کد تخفیف")
    percent = models.IntegerField(null=True, verbose_name="درصد تخفیف")
    count = models.IntegerField(null=True, verbose_name="تعداد استفاده")
    status = models.BooleanField(default=True, verbose_name="وضعیت")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "کد تخفیف"
        verbose_name_plural = "کدهای تخفیف"


class UserDescount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    code = models.CharField(max_length=250, verbose_name="کد")
    status = models.BooleanField(default=False, verbose_name="وضعیت")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'کد استفاده شده'
        verbose_name_plural = "کدهای استفاده شده"
