import requests
from django.shortcuts import render
from .utils import keep_products_intersection_shops, summarize_shop_products, get_open_prices

def shop_compare_summary(request):
    # Get user's selected location or shop type, then call OSM API
    selected_shops = []
    
    # shop_id_1 = request.GET.get('osm_id_shop_1') if request.GET.get('osm_id_shop_1') else '27108404' # Get shop ID from query parameter Intermarché
    shop_id_1 = request.GET.get('osm_id_shop_1') if request.GET.get('osm_id_shop_1') else '154' # Get shop ID from query parameter Intermarché
    shop_id_2 = request.GET.get('osm_id_shop_2') if request.GET.get('osm_id_shop_2') else '3' # Get shop ID from query parameter Auchan
        
    # Fetch shops from OpenStreetMap
    for shop_id in [shop_id_1, shop_id_2]:
        shop = {'id': shop_id}
        # response = requests.get(f"https://www.openstreetmap.org/api/0.6/node/{shop_id}")
        # data = xmltodict.parse(response.content)['osm']['node'] if response.status_code == 200 else {}
        # if 'tag' in data.keys():
        #     for node in data['tag']:
        #         if node['@k'] == 'name':
        #             shop['name'] = node['@v']
        #         if node['@k'] == 'addr:city':
        #             shop['city'] = node['@v']
        #         pass
        selected_shops.append(shop)
    
    # Receive list of selected shops and retrieve product prices from OFF

    shop_products = {}
    products = {}
    for shop in selected_shops:
        session = requests.Session()
        for prices in get_open_prices(session, shop['id']): 
            for price in prices['items']:
                if not shop.get('name'):
                    location = price.get('location')
                    shop['name'] = location['osm_name']
                
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


