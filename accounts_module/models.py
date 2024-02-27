from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Field(models.Model):
    title = models.CharField(max_length=255, null=True, verbose_name="رشته تحصیلی")
    slug = models.CharField(max_length=255, null=True, verbose_name="لینک")
    is_active = models.BooleanField(default=False, null=True, verbose_name="فعال/غیرفعال")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "رشته"
        verbose_name_plural = "رشته ها"


class User(AbstractUser):
    student_code = models.CharField(max_length=255, unique=True, null=True, verbose_name="شماره دانشجویی")
    phone_number = models.CharField(max_length=11, unique=True, null=True, verbose_name="شماره تلفن")
    entering_year = models.CharField(max_length=4, null=True, verbose_name="سال ورود")
    field_of_study = models.ForeignKey(Field, on_delete=models.CASCADE, null=True, verbose_name="رشته تحصیلی")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"