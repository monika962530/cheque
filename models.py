from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import RegexValidator
# Create your models here.
class Signs(models.Model):
	relation = models.OneToOneField(User, on_delete=models.CASCADE)
	department = models.CharField(null=True, blank=True, max_length=1000, help_text="User Department")
	mobile = models.CharField(null=True, blank=True, max_length=1000, help_text="User Mobile")

	
	def __str__(self):
		return (self.relation.username).title()
	class Meta:
			verbose_name_plural = "Registration Information"
class Mvouchar(models.Model):
	related = models.ForeignKey(Signs, on_delete=models.CASCADE, null=True, blank=True)
	vouchar_no = models.CharField(max_length=1000, null=True, blank=True)
	to_pay = models.CharField(max_length=50, null=True, blank=True)
	amount = models.CharField(max_length=10000, null=True, blank=True)
	amount_in_words = models.CharField(max_length=1000, null=True, blank=True)
	CHEQUE_REGEX = RegexValidator( regex=r'^\d{6}$', message="Cheque Number must be exactly 6 digits" )
	cheque_no = models.CharField(validators=[CHEQUE_REGEX, ], null=True, max_length=6, help_text='integers only')
	account_no = models.CharField(max_length=50, null=True, blank=True)
	dated = models.DateTimeField(auto_now=True)
	cheque_date = models.CharField(max_length=10, null=True, blank=True)
	
	def __str__(self):
		if self.related:
			return self.related.relation.username.title()
		else:
			return 'no related!'
	class Meta:
			verbose_name_plural = "Single Cheque Multiple Vouchar Of Users"
class Bill(models.Model):
	voucher = models.ForeignKey(Mvouchar, on_delete=models.CASCADE, null=True, blank=True)
	bill_no = models.CharField(max_length=8000, null=True, blank=True)
	bill_details = models.CharField(max_length=10000, null=True, blank=True)
	am = models.CharField(max_length=30000, null=True, blank=True)
	
	
	