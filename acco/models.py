# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
	oauth_id=models.CharField(max_length=200)
	method=models.CharField(max_length=200)
	name=models.CharField(max_length=200)
	user=models.ForeignKey(User, null=True)

	