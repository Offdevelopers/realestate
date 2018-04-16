from __future__ import unicode_literals

from django.db import models


# Create your models here.

class Developer(models.Model):
	name=models.CharField(max_length=200)
	address=models.TextField()
	phone=models.CharField(max_length=200)
	email=models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Agent(models.Model):
	name=models.CharField(max_length=200)
	email=models.CharField(max_length=200)
	phone=models.CharField(max_length=100)
	developer=models.ForeignKey(Developer)
	rating=models.DecimalField(max_digits=2, decimal_places=1)

	def __str__(self):
		return self.name

class Property(models.Model):
	name=models.CharField(max_length=200)
	thumbnail=models.ImageField(upload_to='media')
	bedroom=models.IntegerField()
	bathroom=models.IntegerField()
	developer=models.ForeignKey(Developer)
	full_address=models.TextField()
	price=models.IntegerField()
	area=models.CharField(max_length=200)
	date_added=models.DateTimeField(auto_now_add=True)
	year_built=models.DateField(null=True)
	agent_name=models.ForeignKey(Agent)
	city=models.CharField(max_length=200)
	state=models.CharField(max_length=200)
	country=models.CharField(max_length=200)
	zipcode=models.CharField(max_length=200)
	developer_price=models.IntegerField()
	longitude=models.CharField(max_length=200, null=True)
	latitude=models.CharField(max_length=200, null=True)
	last_updated=models.DateTimeField(auto_now=True)
	property_type=models.CharField(max_length=200, choices=(('House', 'House'), ('Land', 'Land')), null=True)
	description=models.TextField( null=True)
	lot_size=models.IntegerField( default=2000)
	parking_space=models.IntegerField(default=0)
	status=models.CharField(default='Sold', max_length=200)

	def __str__(self):
		return self.name


class Picture(models.Model):
	picture_for=models.ForeignKey(Property)
	picture=models.ImageField(upload_to='media')
	description=models.TextField()






















