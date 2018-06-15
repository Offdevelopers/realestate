# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
import random
import string
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
import pdb
from django.http import JsonResponse, HttpResponseRedirect
from django.template.loader import render_to_string
# Create your views here.


class LoginView(View):

	def get(self, request, *args, **kwargs):

		if request.is_ajax():
			if request.user.is_authenticated():
				return JsonResponse({'status':False})
			name=request.GET.get('name')
			email=request.GET.get('email')
			username=name.replace(' ', '')
			oauth_id=request.GET.get('id')
			oauth_method=request.GET.get('method')
			status=False
			#pdb.set_trace()
			try:
				profile=Profile.objects.get(Q(oauth_id=oauth_id),method__icontains=oauth_method)
				login(request,profile.user)
				
				status=True

			except Profile.DoesNotExist:
				username=create_username(username)
				
				user=User(username=username, email=email)


				user.save()
				profile=Profile(name=name, method=oauth_method, oauth_id=oauth_id, user=user)
				profile.save()
				login(request,user)
				status=True

		data= render_to_string('main/includes/nav.html',{'home':True, 'user':profile.user})		
			
			

			
		return JsonResponse({'status':status, 'data':data})		
				
				






def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


def create_username(username):
	#pdb.set_trace()
	try:
		user=User.objects.get(username=username)
	except User.DoesNotExist:	
		#pdb.set_trace()
		return username	
	username=username+'_'+random_char(5)
	return create_username(username)

	
		
	
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

		


