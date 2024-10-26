import requests
from django.shortcuts import render
import xmltodict

def shop_compare_summary(request):
    # Get user's selected location or shop type, then call OSM API
    selected_shops = []
    
    shop_id_1 = request.GET.get('osm_id_shop_1') if request.GET.get('osm_id_shop_1') else '27108404' # Get shop ID from query parameter
    shop_id_2 = request.GET.get('osm_id_shop_2') if request.GET.get('osm_id_shop_2') else '872934393' # Get shop ID from query parameter
    product_barcode = request.GET.get('product_barcode') if request.GET.get('product_barcode') else '3178530410105' # Get shop ID from query parameter
        
    # Fetch shops from OpenStreetMap
    for shop_id in [shop_id_1, shop_id_2]:
        shop = {'id': shop_id}
        response = requests.get(f"https://www.openstreetmap.org/api/0.6/node/{shop_id}")
        data = xmltodict.parse(response.content)['osm']['node'] if response.status_code == 200 else {}
        if 'tag' in data.keys():
            for node in data['tag']:
                if node['@k'] == 'name':
                    shop['name'] = node['@v']
                if node['@k'] == 'addr:city':
                    shop['city'] = node['@v']
                pass
        selected_shops.append(shop)
    
    # Receive list of selected shops and retrieve product prices from OFF
    comparison_data = []

    for shop in selected_shops:
        product = {}
        prices = requests.get(f"https://prices.openfoodfacts.org/api/v1/prices?location_osm_id={shop['id']}&product_code={product_barcode}").json()
        if prices['items']:
            product['price'] = prices['items'][0]['price']
            product_name = prices['items'][0]['product']['product_name']
        product['shop_id'] = shop.get('id')
        product['shop_name'] = shop.get('name', "Shop name not retrieved")
        comparison_data.append(product)
        
    return render(request, 'main/shop_summary.html', {'price_summaries': comparison_data, 'product_name': product_name})


