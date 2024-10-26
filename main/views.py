import requests
from django.shortcuts import render
import xmltodict

def shop_compare_summary(request):
    # Get user's selected location or shop type, then call OSM API
    selected_shops = []
    
    shop_id_1 = request.GET.get('osm_id_shop_1') if request.GET.get('osm_id_shop_1') else '1392117416' # Get shop ID from query parameter
    shop_id_2 = request.GET.get('osm_id_shop_2') if request.GET.get('osm_id_shop_2') else '1392117416' # Get shop ID from query parameter
        
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
    summary_prices = {}

    for shop in selected_shops:
        summary_prices = requests.get(f"https://prices.openfoodfacts.org/api/v1/prices/stats?location_osm_id={shop['id']}").json()
        summary_prices['shop_id'] = shop['id']
        comparison_data.append(summary_prices)
        
    return render(request, 'main/shop_summary.html', {'price_summaries': comparison_data})


