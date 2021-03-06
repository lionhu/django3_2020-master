from decimal import Decimal

from django.conf import settings

from . import module_loading
from . import settings as carton_settings
import logging

logger = logging.getLogger("error-logger")


class CartItem(object):
    """
    A cart item, with the associated product, its quantity and its price.
    """

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = int(quantity)
        self.price = Decimal(str(price))

    def __repr__(self):
        return u'CartItem Object (%s)' % self.product

    def to_dict(self):
        return {
            'product': {
                "id": self.product.id,
                "name": self.product.item_name,
                "discount_price": self.product.discount_price,
                "price": self.product.price,
                "thumbimage": self.product.thumbimage.url,
            },
            'product_id': self.product.id,
            'quantity': self.quantity,
            'price': str(self.price),
        }

    @property
    def subtotal(self):
        """
        Subtotal for the cart item.
        """
        if self.product.discount_price:
            return self.product.discount_price * self.quantity

        return self.price * self.quantity


class Cart(object):
    def __init__(self, session, user_id, session_key=None):
        self._items_dict = {}
        self.session = session
        self.user_id = user_id
        self.session_key = session_key or carton_settings.CART_SESSION_KEY
        # self.session["modified"] = False
        # If a cart representation was previously stored in session, then we
        if self.session_key in self.session:
            # rebuild the cart object from that serialized representation.
            cart_representation = self.session[self.session_key]
            # logger.error("cart_representation")
            # logger.error(cart_representation)
            ids_in_cart = cart_representation["orderitems"].keys()
            # logger.error("ids_in_cart")
            # logger.error(ids_in_cart)
            products_queryset = self.get_queryset().filter(pk__in=ids_in_cart)
            for product in products_queryset:
                # logger.error("product ids_in_cart")
                # logger.error(product)
                # logger.error("cart_representation ids_in_cart")
                # logger.error(cart_representation)
                item = cart_representation["orderitems"][str(product.id)]
                self._items_dict[product.id] = CartItem(
                    product, item['quantity'], Decimal(item['price'])
                )

    def __contains__(self, product):
        """
        Checks if the given product is in the cart.
        """
        return product in self.products

    def get_product_model(self):
        return module_loading.get_product_model()

    def filter_products(self, queryset):
        """
        Applies lookup parameters defined in settings.
        """
        lookup_parameters = getattr(settings, 'CART_PRODUCT_LOOKUP', None)
        if lookup_parameters:
            queryset = queryset.filter(**lookup_parameters)
        return queryset

    def get_queryset(self):
        product_model = self.get_product_model()
        queryset = product_model._default_manager.all()
        queryset = self.filter_products(queryset)
        return queryset

    def update_session(self):
        """
        Serializes the cart data, saves it to session and marks session as modified.
        """
        self.session[self.session_key] = self.cart_serializable
        # self.session["modified"] = True

    def add(self, product, price=None, quantity=1):
        """
        Adds or creates products in cart. For an existing product,
        the quantity is increased and the price is ignored.
        """
        quantity = int(quantity)
        if quantity < 1:
            raise ValueError('Quantity must be at least 1 when adding to cart')
        if product in self.products:
            self._items_dict[product.id].quantity += quantity
        else:
            if price == None:
                raise ValueError('Missing price when adding to cart')
            self._items_dict[product.id] = CartItem(product, quantity, price)
        self.update_session()

    def remove(self, product):
        """
        Removes the product.
        """
        logger.error("before remove session:")
        logger.error(self.session)
        if product in self.products:
            del self._items_dict[product.id]
            self.update_session()

        logger.error("after remove session:")
        logger.error(self.session)

    def remove_single(self, product):
        """
        Removes a single product by decreasing the quantity.
        """
        if product in self.products:
            if self._items_dict[product.id].quantity <= 1:
                # There's only 1 product left so we drop it
                del self._items_dict[product.id]
            else:
                self._items_dict[product.id].quantity -= 1
            self.update_session()

    def clear(self):
        """
        Removes all items.
        """
        logger.error("clear sesstion cart after ordered!")
        self._items_dict = {}
        self.update_session()

    def set_quantity(self, product, quantity):
        """
        Sets the product's quantity.
        """
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError('Quantity must be positive when updating cart')
        if product in self.products:
            self._items_dict[product.id].quantity = quantity
            if self._items_dict[product.id].quantity < 1:
                del self._items_dict[product.id]
            self.update_session()

    @property
    def items(self):
        """
        The list of cart items.
        """
        return self._items_dict.values()

    @property
    def cart_serializable(self):
        """
        The serializable representation of the cart.
        For instance:
        {
            '1': {'product_id': 1, 'quantity': 2, price: '9.99'},
            '2': {'product_id': 2, 'quantity': 3, price: '29.99'},
        }
        Note how the product pk servers as the dictionary key.
        """
        orderitems = {}
        cart_representation = {}
        for item in self.items:
            # JSON serialization: object attribute should be a string
            product_id = str(item.product.id)
            orderitems[product_id] = item.to_dict()

        cart_representation["orderitems"] = orderitems
        cart_representation["Qty"] = self.count
        cart_representation["Total"] = self.total
        cart_representation["user_id"] = self.user_id
        return cart_representation

    @property
    def items_serializable(self):
        """
        The list of items formatted for serialization.
        """
        return self.cart_serializable["orderitems"].items()

    @property
    def count(self):
        """
        The number of items in cart, that's the sum of quantities.
        """
        return sum([item.quantity for item in self.items])

    @property
    def unique_count(self):
        """
        The number of unique items in cart, regardless of the quantity.
        """
        return len(self._items_dict)

    def product_count(self, product):
        """
        The number of unique items in cart, regardless of the quantity.
        """
        try:
            return self._items_dict[product.id].quantity
        except KeyError:
            return 0

    def product_subtotal(self, product):
        """
        The number of unique items in cart, regardless of the quantity.
        """
        try:
            return self._items_dict[product.id].subtotal
        except KeyError:
            return 0

    @property
    def is_empty(self):
        return self.unique_count == 0

    @property
    def products(self):
        """
        The list of associated products.
        """
        return [item.product for item in self.items]

    @property
    def total(self):
        """
        The total value of all items in the cart.
        """
        return sum([item.subtotal for item in self.items])
