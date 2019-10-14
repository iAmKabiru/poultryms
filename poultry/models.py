from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.db.models import F, Sum

class BirdType(models.Model):
	bird_type = models.CharField(max_length=255)

	def __str__(self):
		return self.bird_type

	def quantity(self):
		return self.birds_set.count()


class Birds(models.Model):
	bird_type = models.ForeignKey(BirdType, on_delete=models.CASCADE)
	description = models.CharField(max_length = 255)
	quantity = models.IntegerField()
	date = models.DateTimeField(auto_now_add=True)
	cost_per_bird = models.IntegerField(default=0, verbose_name = 'cost per bird (N)')

	class Meta:
		verbose_name_plural = 'Birds'

	def __str__(self):
		return self.description


class Feed(models.Model):
	bird = models.ForeignKey(Birds, on_delete=models.CASCADE)
	description = models.CharField(max_length=255)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.description



class Medication(models.Model):
	bird  = models.ForeignKey(Birds, on_delete=models.CASCADE)
	description = models.CharField(max_length=255)
	date = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.description



class Sales(models.Model):
	birds = models.ForeignKey(Birds, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	selling_price = models.IntegerField(verbose_name = 'selling price (N)')

	class Meta:
		verbose_name_plural = 'Sales'

	def __str__(self):
		return self.birds.description


class Employers(models.Model):
	name = models.CharField(max_length=255)
	phone = models.CharField(max_length=255)
	salary = models.CharField(max_length=255, verbose_name = 'salary (N)')

	class Meta:
		verbose_name_plural = 'Employers'

	def __str__(self):
		return self.name


class DoctorVisit(models.Model):
	doctor_name = models.CharField(max_length=255)
	purpose = models.CharField(max_length=255)
	date = models.DateTimeField(auto_now_add=True)
	description = models.TextField()

	def __str__(self):
		return self.doctor_name


class MedicalReport(models.Model):
	case = models.CharField(max_length=255)
	description = models.TextField()
	date = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.case

class Purchase(models.Model):
	purchase_type_choices = (
		('feed', 'feed'),
		('birds', 'birds'),
		('medicine', 'medicine'),
		('equipement', 'equipement')
		)
	purchase_type = models.CharField(max_length=255, choices=purchase_type_choices)
	amount = models.IntegerField(default=0, verbose_name='Amount (N)')
	description = models.CharField(max_length=255, blank=True, null=True)
	quantity = models.IntegerField(default=0)
	date = models.DateTimeField(auto_now_add=True)


class Casualty(models.Model):
	casualty_type_choices = (
		('death','death'),
		('injury', 'injury'),
		)
	birds = models.ForeignKey(Birds, on_delete=models.CASCADE)
	casualty_type = models.CharField(max_length=255, choices = casualty_type_choices)
	quantity = models.IntegerField(default=0)
	date = models.DateTimeField(auto_now_add=True)


	class Meta:
		verbose_name_plural = 'Casualties'


# signal for updating birds on casualties 
@receiver(post_save, sender=Casualty, dispatch_uid="update_when_add_casualty")
def update_when_add_casualty(sender, **kwargs):
    casualty = kwargs['instance']
    if casualty.pk:
        Birds.objects.filter(pk=casualty.birds_id).update(quantity=F('quantity') - casualty.quantity)




# signal for updating birds on sale
@receiver(post_save, sender=Sales, dispatch_uid="update_when_add")
def update_when_add(sender, **kwargs):
    sales = kwargs['instance']
    if sales.pk:
        Birds.objects.filter(pk=sales.birds_id).update(quantity=F('quantity') - sales.quantity)
