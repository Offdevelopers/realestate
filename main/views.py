from django.shortcuts import render

# Create your views here.
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,
                                  FormView)
from django.views import View

from algoliasearch_django import raw_search
from django.http import HttpResponse, JsonResponse, Http404
import pdb
from .models import Property, Picture, Agent
from django.db.models import Avg,Count, Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template.loader import render_to_string
from django.views.generic import DetailView




class HomeView(TemplateView):
	template_name='main/index.html'


class IncreaseStat(View):


	def get(self, request):
		house=self.get_object(request.GET.get('id'))
		if request.GET.get('stat')=='views':
			house.views+=1
			
		if request.GET.get('stat')=='favorites':
			house.favorites+=1

		house.save()
		return JsonResponse({'status':True})


	def get_object(self, id):
		return Property.objects.get(pk=id)






class PropertyDetail(DetailView):
	model=Property
	template_name='main/detail.html'

	def get_context_data(self, **kwargs):
		context=super(PropertyDetail, self).get_context_data(**kwargs)
		house=self.get_object()

		context['max_range']=int(house.price)*1.2
		context['min_range']=int(house.price)*0.8
		context['initialdownpayt']=int(house.price)*0.4

		context['principal']=(int(house.price)-context['initialdownpayt'])/60
		context['property_images']=Picture.objects.filter(picture_for=house)
		context['nearby_similar_homes']=Property.objects.filter(city__icontains=house.city).filter(property_type__icontains=house.property_type)
		
		property_list=Property.objects.filter(city__icontains=house.city)
		values=[int(property.price) for property in property_list]
		context['median']=median(values)
		context['savings']=house.developer_price - house.price
		return context


class SearchView(View):
 	template_name='main/search.html'
 	no_of_item=settings.NO_OF_ITEM
 	def get(self, request, *args, **kwargs):
 		context=dict()	
 		if request.GET.get('page'):
 			query=request.session['query']
 			params={"hitsPerPage": self.no_of_item, "page":request.GET.get('page')}
 		else:
			query=request.GET.get('address')
			params = { "hitsPerPage": self.no_of_item}
		request.session['query']=query
		
		a=raw_search(Property, query, params)
		b=raw_search(Property, query, {"hitsPerPage":2000})

		property_list=Property.objects.filter(id__in=[int(w.get('objectID')) for w in a.get('hits')  ])

		if property_list.exists():

			context=self.get_context(property_list)
			pageNo=a.get('nbPages')
			context['last_page']=pageNo
			context['pageNo']=range(0, pageNo)
			context['no_of_properties_for_sales']=a.get('nbHits')
			
			context['result']=True
			context['query']=query
		else:
			context=self.get_context(get_feature())
			context['result']=True



		return render(request, 'main/search.html', context)


 	def get_context(self,property_list):
 		context=dict()
 		values=[int(property.price) for property in property_list]
		context['median']=median(values)
		context['state_average']=Property.objects.values('city').annotate(Avg('price')).filter(state__icontains=property_list[0].state)
		context['country']=property_list[0].country
		context['city']=property_list[0].city
		context['state']=property_list[0].state
		context['country_average']=Property.objects.values('state').annotate(Avg('price')).filter(country__icontains=property_list[0].country)
		two_bedroom=property_list.filter(bedroom=2)
		context['two_bedroom_count']=two_bedroom.count()  
		context['two_bedroom_avergae_price']=two_bedroom.aggregate(Avg('price'))
		
		one_bedroom=property_list.filter(bedroom=1)
		context['one_bedroom_count']=one_bedroom.count()  
		context['one_bedroom_avergae_price']=one_bedroom.aggregate(Avg('price'))
		three_bedroom=property_list.filter(bedroom__gte=3)
		context['three_bedroom_count']=three_bedroom.count()  
		context['three_bedroom_avergae_price']=three_bedroom.aggregate(Avg('price'))
		context['property_list']=property_list
		context['customer_satisfaction']=Agent.objects.filter(city__icontains=property_list[0].city).aggregate(Avg('rating'))
		context['no_of_agent']=Agent.objects.filter(city__icontains=property_list[0].city).count()

		return context


 	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(SearchView, self).dispatch(request, *args, **kwargs)

 	def post(self, request, *args, **kwargs):
 		filter_string=''
		if request.is_ajax():
			context=dict()
			if request.POST.get('page'):
	 			
	 			if request.POST.get('filter_string'):
	 				search_params=build_search_string(filter_string=request.POST.get('filter_string'), page=request.POST.get('page'))
				else:
					search_params=build_search_string(page=request.POST.get('page'))
			else:			
				params_dict=build_params_dict(request)
				filter_string=get_filter_string(request,params_dict)
				search_params=build_search_string(filter_string )
			query=request.session['query']

			a=raw_search(Property, query, search_params)
			pageNo=a.get('nbPages')
			context['property_list']=Property.objects.filter(id__in=[int(w.get('objectID')) for w in a.get('hits')  ])
			if not context['property_list'].exists():
				context['result']=True
			pageNo=range(0, pageNo)
			#pdb.set_trace()
			query=request.session['query']
			pagination=render_to_string('main/includes/navigation.html', {'pageNo':pageNo})
			result=render_to_string('main/includes/result.html', context)
			return JsonResponse({'status':'success','result':result, 'pagination':pagination, 'filter_string':filter_string})


class AgentView(View):

	 def get(self, request,*args, **kwargs):
	 	if request.GET.get('city') and request.GET.get('state'):
	 		state=request.GET.get('state')
	 		city=request.GET.get('city')
	 		country=request.GET.get('country')
	 		premium_agent=Agent.objects.filter(premium=True)
	 		premium_agent_state=Agent.objects.filter(premium=True).filter(state__icontains=state)[:3]
	 		partners=Agent.objects.filter(city__icontains=city)
	 		partner_nearby=Agent.objects.filter(state__icontains=state).exclude(city__icontains=city)[:3]
	 		context={
	 		'premium_agent':premium_agent,
	 		'premium_agent_state':premium_agent_state,
	 		'partners':partners,
	 		'partner_nearby':partner_nearby,
	 		'city':city,
	 		'state':state,
	 		'country':country,
	 		}
	 		return render(request, 'main/agent.html', context)
	 	else:
	 		raise Http404('Invalid request')




class StartNow(TemplateView):
	template_name='main/offer.html'



def getFeature(request):
	data=dict()
	location=request.GET.get('location')
	properties=get_feature(location)

	latest=Property.objects.filter(state__icontains=location).order_by('date_added')[:8]
	#pdb.set_trace()
	if latest.count() < 4:
		latest=Property.objects.filter(Q(state__icontains=location)|Q(state__icontains='lagos')).order_by('date_added','-state')[:8]
	context={'location':location, 'properties':properties, 'latest':latest, 'state':location}
	data['featurelatest']=render_to_string('main/includes/partial-feature.html', context)
	return JsonResponse(data)


def get_feature(location=None):
	if location == None:
		location='Lagos'
	properties=Property.objects.filter(Q(state__icontains=location), feature=True)
	if properties.count() < 3:
		properties=Property.objects.filter(Q(state__icontains=location)|Q(state__icontains='lagos'), feature=True)[:6]
	return properties


def recent(request):
	location=request.GET.get('location')
	if location == None:
		location='abuja'
	latest=Property.objects.filter(Q(state__icontains=location)|Q(state__icontains='FCT')).order_by('uploadDate','-state')
	context={'latest':latest,'topform':topForm()}
	return render(request,'home/recent-listing.html', context)



		

def build_search_string(filter_string='', page=0):
	params={'hitsPerPage':settings.NO_OF_ITEM ,'page':page, 'filters':filter_string }
	return params



def seperate_field(field):
	value_operator_list=field.split('-')
	return value_operator_list


 	
def build_params_dict(request):
		params_dict=dict()
		fields=['min-bedroom','max-bedroom','min-bathroom', 'max-bathroom','min-lot_size', 
			'max-lot_size', 'type-property_type','min-year_built',
			'max-year_built','max-parking_space', 'min-parking_space', 'min-price', 'max-price']
		for a in fields :
			value_operator_list=seperate_field(a)
			operator_string=value_operator_list[0]
			field=value_operator_list[1]
			
			if request.POST.get(a) != '' and request.POST.get(a) != None :
				params_dict[operator_string]=field
			else:
				pass
		
		return params_dict



def get_filter_string(request, params_dict):
	filter_string=''
	for k, v in params_dict.items():
		operator_symbol=get_operator_symbol(k)
		
		newfilter=v+' '+operator_symbol+' '+request.POST.get(k+'-'+v)

		if filter_string== '':
			filter_string=newfilter
		else:
			filter_string+=' AND' + ' ' + newfilter

	return filter_string


def get_operator_symbol(operator):
	operator_symbol_dict={'min':'>', 'max':'<' , 'type':':'}
	return operator_symbol_dict[operator]



def median(lst):
	    lst = sorted(lst)
	    n = len(lst)
	    if n < 1:
	            return None
	    if n % 2 == 1:
	            return lst[n//2]
	    else:
	            return sum(lst[n//2-1:n//2+1])/2.0	




class MortageView(TemplateView):
	template_name='main/lenders.html'
	
