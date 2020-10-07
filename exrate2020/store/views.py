from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
import logging
import json
from django.conf import settings
from .forms import CheckoutForm
from .serializers import OrderSerializer, ItemSerializer
from authentication.models import User
from .models import (
    Item,
    Order,
    OrderItem,
    ShippingAddress,
    Margin
)

CATEGORY = (
    ('S', 'Shirt'),
    ('SP', 'Sport Wear'),
    ('OW', 'Out Wear')
)

logger = logging.getLogger("error")


class SearchProductView(ListView):
    model = Item
    template_name = "shop/home.html"
    context_object_name = "products"
    searchKey = ""

    def get_queryset(self):
        keyval = self.request.GET.get("q", "")
        self.searchKey = keyval
        products = Item.objects.filter(item_name__icontains=keyval) | \
                   Item.objects.filter(description__icontains=keyval)
        logger.error("get_queryset: search product with keyval {}".format(keyval))
        return products

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        context["keyval"] = self.searchKey

        logger.error("get_context_data: search product with keyval {}".format(self.searchKey))
        return context


# Create your views here.
class HomeView(ListView):
    model = Item
    template_name = "shop/home.html"
    context_object_name = "products"

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["categories"] = CATEGORY
        return context


@method_decorator(login_required(login_url='/webauth/login/'), name="dispatch")
class OrderListView(ListView):
    model = Order
    template_name = "shop/accounts/orders.html"
    context_object_name = "orders"
    paginate_by = 2

    def get_queryset(self):
        orders = Order.objects.filter(user=self.request.user)
        return orders


class ProductView(DetailView):
    model = Item
    template_name = "shop/product.html"


class OrderSummaryView(LoginRequiredMixin, View):
    login_url = "/webauth/login/"

    def get(self, *args, **kwargs):

        logger.error("OrderSummaryView")
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order
            }
            logger.error(context)
            return render(self.request, 'shop/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("/")


class CheckoutView(LoginRequiredMixin, View):
    login_url = "/webauth/login/"

    def get(self, *args, **kwargs):
        try:
            form = CheckoutForm()

            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                "order": order,
                "form": form
            }
            return render(self.request, "shop/checkout.html", context)

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("/")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            logger.error("order wrong??")
            logger.error(order)
            if form.is_valid():
                logger.error(" form is_valid")
                logger.error(str(form.cleaned_data))
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                phone = form.cleaned_data.get('phone')
                postcode = form.cleaned_data.get('postcode')
                state = form.cleaned_data.get('state')
                town = form.cleaned_data.get('town')
                street = form.cleaned_data.get('street')
                address_1 = form.cleaned_data.get('address_1')
                address_2 = form.cleaned_data.get('address_2')

                checkout_address = ShippingAddress(
                    name=name,
                    email=email,
                    phone=phone,
                    postcode=postcode,
                    state=state,
                    town=town,
                    street=street,
                    address_1=address_1,
                    address_2=address_2,
                )
                checkout_address.save()
                order.checkout_address = checkout_address
                order.ordered = True
                order.save()

                order.items.update(ordered=True)

                self.caculate_margins(order)

                messages.success(self.request, "Place Order successfully!")
                return redirect('store:checkout')

            messages.warning(self.request, "Failed Chekout")
            return redirect('store:checkout')

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("store:order-summary")

    def caculate_margins(self, order):
        if order:
            last_index = len(settings.MARGIN_RATES)
            user_profile = order.user.profile
            ancestors = user_profile.get_ancestors(ascending=True, include_self=False)
            ancestors_list = list(ancestors)

            # logger.error("before pop root: len {} ".format(len(ancestors_list)))

            if len(ancestors_list) >= 1:
                ancestors_list.pop()  # remove last root element

            # logger.error("after pop root: len {} ".format(len(ancestors_list)))

            margin_left = order.get_total_distributor_margin()

            if ancestors_list:
                margin_left_loop = margin_left
                logger.error("margin_left {} ".format(margin_left))

                for level in range(len(ancestors_list[:last_index])):
                    level_rate = settings.MARGIN_RATES[str(level + 1)]
                    level_margin = int(margin_left_loop * level_rate)
                    user = ancestors_list[level].user

                    logger.error("order_{}, distibute to {} with margin {} at level:{}, level_rate {}".format(order.id,
                                                                                                              user.username,
                                                                                                              level_margin,
                                                                                                              level,
                                                                                                              level_rate))

                    if user.orders.count() >= settings.MARGIN_CRITERIA_ORDERS:
                        Margin.objects.create(
                            order=order,
                            user=user,
                            level=level,
                            amount=level_margin,
                        )
                        margin_left -= level_margin

            if margin_left:
                # mount left margin to root

                logger.error("order_{}, distibute to ADMIN with margin {} ".format(order.id, margin_left))
                adminuser = User.objects.get(username=settings.ADMIN_NAME)
                Margin.objects.create(
                    order=order,
                    user=adminuser,
                    level=100,
                    amount=margin_left,
                )


@login_required(login_url="/webauth/login/")
def add_to_cart(request, pk, location):
    item = get_object_or_404(Item, pk=pk)
    logger.error("add to cart")
    logger.error(location)
    logger.error(item)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        logger.error("add to cart: order_qs")
        logger.error(order_qs)
        order = order_qs[0]

        if order.items.filter(item__pk=item.pk).exists():
            logger.error("add to cart: order.items.filter(item__pk=item.pk) before")
            logger.error(order_item)
            order_item.quantity += 1
            order_item.save()
            logger.error("add to cart: order.items.filter(item__pk=item.pk) after")
            logger.error(order_item)
            messages.info(request, "Added quantity Item")
            return redirect(location)
        else:
            logger.error("add to cart: else")
            logger.error(order_item)
            order.items.add(order_item)
            return redirect(location)
    else:
        logger.error("add to cart: create new order")
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        return redirect(location)


@login_required(login_url="/webauth/login/")
def remove_from_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.delete()
            messages.info(request, "Item \"" + order_item.item.item_name + "\" remove from your cart")
            return redirect("store:order-summary")
        else:
            messages.info(request, "This Item not in your cart")
            return redirect("store:product", pk=pk)
    else:
        # add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("store:product", pk=pk)


@login_required(login_url="/webauth/login/")
def reduce_quantity_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__pk=item.pk).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            # messages.info(request, "Item quantity was updated")
            return redirect("store:order-summary")
        else:
            # messages.info(request, "This Item not in your cart")
            return redirect("store:order-summary")
    else:
        # add message doesnt have order
        messages.info(request, "You do not have an Order")
        return redirect("store:order-summary")


@login_required(login_url="/webauth/login/")
def show_dashboard(request):
    context = {
        "lionhu": "kinghu"
    }
    return render(request, "shop/accounts/dashboard.html", context)


class ProductAPIView(View):
    def post(self, request):
        data = json.loads(request.body)
        pk = data["product_id"]

        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(instance=item, many=False)

        return JsonResponse({
            "result": "OK",
            "product": serializer.data,
        })


class AddToChartAPIView(View):
    def post(self, request):
        data = json.loads(request.body)
        pk = data["product_id"]
        user = request.user

        logger.error(request.path)
        item = get_object_or_404(Item, pk=pk)
        order_item, created = OrderItem.objects.get_or_create(
            item=item,
            user=request.user,
            ordered=False
        )
        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if order_qs.exists():
            order = order_qs[0]

            if order.items.filter(item__pk=item.pk).exists():
                order_item.quantity += 1
                order_item.save()
            else:
                order.items.add(order_item)

        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)

        serializer = OrderSerializer(instance=order, many=False)

        return JsonResponse({
            "result": "OK",
            "product_id": data["product_id"],
            "order_count": order.get_total_quantity(),
            "order": serializer.data
        })
