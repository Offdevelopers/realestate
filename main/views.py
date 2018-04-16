from django.shortcuts import render

# Create your views here.
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,
                                  FormView)
from django.views import View

from algoliasearch_django import raw_search
from django.http import HttpResponse, JsonResponse
import pdb
from .models import Property
from django.db.models import Avg,Count
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template.loader import render_to_string
from django.views.generic import DetailView




class HomeView(TemplateView):
	template_name='main/index.html'


class PropertyDetail(DetailView):
	model=Property
	template_name='main/detail.html'

	def get_context_data(self, **kwargs):
		context=super(PropertyDetail, self).get_context_data(**kwargs)
		context['property_images']=Property




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
		values=[int(property.price) for property in property_list]
		context['median']=median(values)
		pageNo=a.get('nbPages')
		context['state_average']=Property.objects.values('city').annotate(Avg('price')).filter(state__icontains=property_list[0].state)
		context['country']=property_list[0].country
		context['country_average']=Property.objects.values('state').annotate(Avg('price')).filter(country__icontains=property_list[0].country)
		two_bedroom=property_list.filter(bedroom=2)
		context['two_bedroom_count']=two_bedroom.count()  
		context['two_bedroom_avergae_price']=two_bedroom.aggregate(Avg('price'))

		one_bedroom=property_list.filter(bedroom=1)
		context['one_bedroom_count']=one_bedroom.count()  
		context['one_bedroom_avergae_price']=one_bedroom.aggregate(Avg('price'))

		three_bedroom=property_list.filter(bedroom__gte=3)
		context['three_bedroom_count']=one_bedroom.count()  
		context['three_bedroom_avergae_price']=three_bedroom.aggregate(Avg('price'))

		
		context['last_page']=pageNo
		context['pageNo']=range(0, pageNo)
		context['no_of_properties_for_sales']=a.get('nbHits')

		context['property_list']=Property.objects.filter(id__in=[int(w.get('objectID')) for w in a.get('hits')  ])
		return render(request, 'main/search.html', context)


 			

 	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(SearchView, self).dispatch(request, *args, **kwargs)

 	def post(self, request, *args, **kwargs):
 		filter_string=''
		if request.is_ajax():
			context=dict()
			if request.POST.get('page'):
	 			
	 			if request.POST.get('filter_string'):
	 				search_params=build_search_string(filter_string=request.POST.get('filter_string'))
				else:
					search_params=build_search_string()
			else:			
				params_dict=build_params_dict(request)
				filter_string=get_filter_string(request,params_dict)
				search_params=build_search_string(filter_string )
			query=request.session['query']
			a=raw_search(Property, query, search_params)
			pageNo=a.get('nbPages')
			context['property_list']=Property.objects.filter(id__in=[int(w.get('objectID')) for w in a.get('hits')  ])
			pageNo=range(0, pageNo)
			query=request.session['query']
			pagination=render_to_string('main/includes/navigation.html', {'pageNo':pageNo})
			result=render_to_string('main/includes/result.html', context)
			return JsonResponse({'status':'success','result':result, 'pagination':pagination, 'filter_string':filter_string})








		

def build_search_string(filter_string=''):
	params={'hitsPerPage':settings.NO_OF_ITEM , 'filters':filter_string}
	return params



def seperate_field(field):
	value_operator_list=field.split('-')
	return value_operator_list


 	
def build_params_dict(request):
		params_dict=dict()
		fields=['min-bedroom','max-bedroom','min-lot_size', 
			'max-lot_size', 'type-property_type','min-year_built',
			'max-year_built','max-parking_space', 'min-parking_space']
		for a in fields :
			value_operator_list=seperate_field(a)
			operator_string=value_operator_list[0]
			field=value_operator_list[1]
			
			if request.POST.get(a) != '':
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



