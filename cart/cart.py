from decimal import Decimal
from django.conf import settings
from shop.models import Product, ProductSize


# сделать возможность добавлять одинаковый товар, но с разными размерами. ключ будет product_id + размер. Добавить методы проверки ко-ва размеров в jsonresponse


class Cart(object):

    def __init__(self, request, new_session=None):
        if new_session:
            self.session = new_session
        else:
            self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, qty=1, size=None, update_qty=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'qty': 0,
                'price': str(product.price),
                'size': size
            }
        if update_qty:
            self.cart[product_id]['qty'] = qty
        else:
            if self.cart[product_id]['qty'] < ProductSize.objects.get(product=product, name=size).qty:
                self.cart[product_id]['qty'] += qty
            else:
                pass
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        print(product_ids)
        products = Product.objects.filter(id__in=product_ids)
        print(products)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        print(self.cart)
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item
        print(self.cart)

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
