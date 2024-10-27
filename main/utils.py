def keep_products_intersection_shops(shops, shop_products):
    common_shop_products = {}
    for barcode, product in shop_products.items():
        if barcode == '3023480110707':
            print('chartreuse')
        prices = product['prices']
        if prices.get(shops[0]["id"]) and prices.get(shops[1]["id"]):
            common_shop_products[barcode] = shop_products[barcode]
    return common_shop_products
