import requests

def get_open_prices(session, shop_id):
    url = f"https://prices.openfoodfacts.org/api/v1/prices?location_id={shop_id}&size=100&order_by=-date"
    first_page = session.get(url).json()
    yield first_page
    num_pages = first_page['pages']

    for page in range(2, num_pages + 1):
        next_page = session.get(url, params={'page': page}).json()
        yield next_page

def keep_products_intersection_shops(shops, shop_products):
    common_shop_products = {}
    for barcode, product in shop_products.items():
        prices = product['prices']
        if prices.get(shops[0]["id"]) and prices.get(shops[1]["id"]):
            if prices.get(shops[0]["id"]) < prices.get(shops[1]["id"]):
                shop_products[barcode]['cheapest'] = shops[0]["id"]
            else:
                shop_products[barcode]['cheapest'] = shops[1]["id"]
            common_shop_products[barcode] = shop_products[barcode]
    return common_shop_products

def summarize_shop_products(shops, shop_products):
    summary = {}
    summary['len'] = len(shop_products)
    summary['prices'] = {}
    for shop in shops:
        summary['prices'][shop['id']] = {}
        summary['prices'][shop['id']]['sum_prices'] = 0
        for products in shop_products.values():
            summary['prices'][shop['id']]['sum_prices'] += products['prices'][shop['id']]
        
        summary['prices'][shop['id']]['sum_prices'] = "{:.2f}".format(summary['prices'][shop['id']]['sum_prices'])
    return summary