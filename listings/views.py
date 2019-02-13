from django.shortcuts import get_object_or_404, render
from .models import Listing
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, listingtype_choices, state_choices


# Create your views here.
def index(request):
	listings = Listing.objects.order_by('-list_date').filter(is_published=True)

	paginator = Paginator(listings, 6)
	page = request.GET.get('page')
	paged_listings = paginator.get_page(page)

	#Generate list to the view.
	context = {
		'listings' : paged_listings
	}

	return render(request, 'listings/listings.html', context)


#Listing all publications.
def listing(request, listing_id):
	listing = get_object_or_404(Listing, pk=listing_id)	

	context = {
		'listing': listing,
	}

	return render(request, 'listings/listing.html', context)


#Search inside listings by filters.
def search(request):	
	queryset_list = Listing.objects.order_by('-list_date')

	#Keywords
	if 'keywords' in request.GET:
		keywords = request.GET['keywords']
		if keywords:
			queryset_list = queryset_list.filter(description__icontains=keywords)

	#City
	if 'city' in request.GET:
		city = request.GET['city']
		if city:
			queryset_list = queryset_list.filter(city__iexact=city)

	#State (Will be changed to colonias instead states)
	# if 'state' in request.GET:
	# 	state = request.GET['state']
	# 	if state:
	# 		queryset_list = queryset_list.filter(state__iexact=state)

	#Listing Type
	if 'listingtype' in request.GET:
		listingtype = request.GET['listingtype']
		if listingtype:
			queryset_list = queryset_list.filter(listingtype__iexact=listingtype)

	#Price
	if 'price' in request.GET:
		price = request.GET['price']
		if price:
			queryset_list = queryset_list.filter(price__lte=price)


	context = {
		'state_choices': state_choices,
		'listingtype_choices': listingtype_choices,
		'price_choices': price_choices,
		'listings': queryset_list,
		'values': request.GET
	}	

	return render(request, 'listings/search.html', context)