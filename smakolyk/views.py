import json
import pymongo
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render





class ProductListDB:
    def __init__(self):
        uri = "mongodb+srv://sas:01112002!@cluster0.bhuharj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.client = pymongo.MongoClient(uri)
        self.db = self.client['Product']
        self.collection = self.db['ProductList']

    def close_connection(self):
        self.client.close()

    def get_product_details(self, name):

        return self.collection.find_one({'name': name}, {'price': 1, 'Showcase_name': 1, 'image_url': 1, '_id': 0})




def welcome(request):
    return render(request, 'welcome.html')

def get_products():
    product_list_db = ProductListDB()
    products_cursor = product_list_db.collection.find()
    products = list(products_cursor)
    product_list_db.close_connection()
    return products



def store_view(request):
    products = get_products()
    cart = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart)
    total_items = sum(cart.values())

    return render(request, 'store.html', {'products': products, 'total_items': total_items})



def home(request):
    products = get_products()
    cart = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart)
    total_items = sum(cart.values())
    return render(request, 'home.html', {'products': products, 'total_items': total_items})



def why(request):
    cart = json.loads(request.COOKIES.get('cart', '{}'))
    total_items = sum(cart.values())
    return render(request, 'why.html', {'total_items': total_items})



def contacts(request):
    cart = json.loads(request.COOKIES.get('cart', '{}'))
    total_items = sum(cart.values())
    return render(request, 'contacts.html', {'total_items': total_items})




def product_detail(request, name):
    product_list_db = ProductListDB()
    product = product_list_db.collection.find_one({'name': name})
    product_list_db.close_connection()
    cart = request.COOKIES.get('cart', '{}')
    cart = json.loads(cart)
    total_items = sum(cart.values())
    return render(request, 'product_detail.html', {'product': product, 'total_items': total_items})









def cart(request):
    cart_info = get_cart_info(request)
    products_info = cart_info['products']
    total_cost = cart_info['total_cost']
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'products': products_info,
            'total_cost': total_cost
        })
    else:
        return render(request, 'cart.html', {
            'products': products_info,
            'total_cost': total_cost
        })




@csrf_exempt
@require_http_methods(["POST"])
def add_to_cart(request):
    data = json.loads(request.body)
    product_name = data['productName']
    cart = json.loads(request.COOKIES.get('cart', '{}'))

    if product_name in cart:
        cart[product_name] += 1
    else:
        cart[product_name] = 1

    cart_items = ', '.join([f'{name}: {count}' for name, count in cart.items()])
    print(f'Current cart: {cart_items}')

    response = JsonResponse({'message': f'Product {product_name} added to cart', 'cart': cart, 'total_items': sum(cart.values())})
    response.set_cookie('cart', json.dumps(cart), max_age=3600*24*7)

    return response







def get_cart_info(request):
    cart = json.loads(request.COOKIES.get('cart', '{}'))
    product_list_db = ProductListDB()

    products_info = []
    total_cost = 0

    for product_name, quantity in cart.items():
        product_details = product_list_db.get_product_details(product_name)
        if product_details:

            quantity = int(quantity)
            price = float(product_details.get('price', 0))
            total_cost += price * quantity
            product_info = {
                'name': product_name,
                'quantity': quantity,
                'price': price,
                'Showcase_name': product_details.get('Showcase_name', 'N/A'),
                'image_url': product_details.get('image_url', '')
            }
            products_info.append(product_info)

    product_list_db.close_connection()

    return {'products': products_info, 'total_cost': total_cost}









@csrf_exempt
@require_http_methods(["POST"])
def update_cart(request):
    data = json.loads(request.body)
    product_name = data['productName']
    action = data['action']

    cart = json.loads(request.COOKIES.get('cart', '{}'))

    if action == 'init':
        products_info = get_cart_info(request)
        response_data = {
            'message': 'Cart initialized successfully',
            'cart': products_info['products'],
            'total_cost': products_info['total_cost']
        }
    else:
        if product_name in cart:
            if action == 'add':
                cart[product_name] += 1
            elif action == 'remove':
                cart[product_name] -= 1
                if cart[product_name] <= 0:
                    del cart[product_name]

        cart_items = ', '.join([f'{name}: {count}' for name, count in cart.items()])
        print(f'Updated cart: {cart_items}')
        updated_products_info = get_cart_info(request)
        response_data = {
            'message': 'Cart updated successfully',
            'cart': updated_products_info['products'],
            'total_cost': updated_products_info['total_cost']
        }

    response = JsonResponse(response_data)
    response.set_cookie('cart', json.dumps(cart), max_age=3600*24*7)

    return response