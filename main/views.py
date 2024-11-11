import requests
from django.shortcuts import render, redirect
from .utils import keep_products_intersection_shops, summarize_shop_products, get_open_prices, search_osm
from django.http import HttpResponse

def shops_compare_summary(request):
    # Get user's selected location or shop type, then call OSM API
    selected_shops = []
    
    shop_id_1 = int(request.session.get('first_supermarket_id'))
    shop_id_2 = int(request.session.get('second_supermarket_id'))
    selected_shops = [{'id': shop_id_1}, 
                       {'id': shop_id_2}]

    # Receive list of selected shops and retrieve product prices from OFF
    shop_products = {}
    products = {}
    for shop in selected_shops:
        session = requests.Session()
        for prices in get_open_prices(session, shop['id']): 
            for price in prices['items']:
                if not shop.get('name'):
                    location = price.get('location')
                    shop['name'] = location['osm_display_name']
                
                product = price.get('product')
                if not product:
                    continue
                
                if product.get('code') not in products.keys():  ## Init the dict if it s the first time
                    products[product.get('code')] = {}
                    products[product.get('code')]['name'] = product.get('product_name')
                    products[product.get('code')]['prices'] = {}

                if not products[product.get('code')]['prices'].get(shop["id"]): # Do not overide prices to get the latest ones
                    products[product.get('code')]['prices'][shop["id"]] = price['price']

    
    shop_products = keep_products_intersection_shops(selected_shops, products)
    shop_products_summary = summarize_shop_products(selected_shops, shop_products)
    return render(request, 'main/shop_summary.html', {'shops': selected_shops, 'products': shop_products, 'shop_products_summary': shop_products_summary})

def landing_page(request):
    if request.method == "POST":
        # Get the query from the form
        query = request.POST.get("query", "supermarket")

        # Redirect to the search page with the first search stage
        context = {'query': query, 'stage': '1'}
    else:
        context = {'stage': '1'}
    return render(request, 'main/select_supermarket.html', context)

def search_supermarkets(request):
    # Determine which search phase (first or second)
    search_stage = request.GET.get('stage', '1')
    query = request.GET.get('query', 'supermarket')
    
     # If no query is provided, prompt the user to enter one
    if not query:
        return render(request, 'main/search_form.html', {'stage': search_stage})
    
    # Perform the search
    supermarkets = search_osm(query)
    context = {'supermarkets': supermarkets, 'stage': search_stage}
    return render(request, 'main/select_supermarket.html', context)

def select_supermarket(request):
    if request.method == "POST":
        selected_id = request.POST.get("supermarket_id")
        search_stage = request.POST.get('stage', '1')

        if search_stage == "1":
            # Store the first selection in the session and redirect for the second selection
            request.session['first_supermarket_id'] = selected_id
            context = {'stage': '2'}
            return render(request, 'main/select_supermarket.html', context)
    
        elif search_stage == "2":
            # Store the second selection and redirect to the summary
            request.session['second_supermarket_id'] = selected_id
            return shops_compare_summary(request)
    return HttpResponse("No supermarket selected.")