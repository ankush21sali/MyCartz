import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages
from unicodedata import category

from .models import Product, ContactUs, Order, OrderItem

# Create your views here.
def index(request):
    electronics = Product.objects.filter(category='Electronics')
    fashion = Product.objects.filter(category='Fashion')
    home_appliances = Product.objects.filter(category='Home Appliances')
    sports_and_fitness = Product.objects.filter(category='Sports & Fitness')

    products = {
        'electronics' : electronics,
        'fashion' : fashion,
        'home_appliances' : home_appliances,
        'sports_and_fitness' : sports_and_fitness
    }
    return render(request, "shop/home.html", products)




def about(request):
    return render(request, "shop/about.html")




def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")

        if name and email and phone and desc:
            contact = ContactUs(name=name, email=email, phone=phone, desc=desc)
            contact.save()
            url = reverse("ContactUs") + "?submitted=true"
            return redirect(url)

    submitted = request.GET.get("submitted") == "true"
    return render(request, "shop/contact.html", {"submitted": submitted})


def tracker(request):
    context = {}

    if request.method == "POST":
        # Check if it's a cancel request
        if "cancel_order" in request.POST:
            order_id = request.POST.get("order_id")
            order = get_object_or_404(Order, order_id=order_id)
            order.delete()  # Or set status = "Cancelled" if soft-delete
            messages.success(request, f"Order #{order_id} has been cancelled.")
            return redirect("TrackingStatus")

        # Otherwise, it's an email search
        track_email = request.POST.get("track_email")

        if track_email:
            user_orders = Order.objects.filter(email=track_email)

            if user_orders.exists():
                order_details = []
                for order in user_orders:
                    items = OrderItem.objects.filter(order=order)
                    order_details.append({
                        "order": order,
                        "items": items
                    })

                context["orders_found"] = True
                context["order_details"] = order_details
            else:
                context["orders_found"] = False
                context["message"] = "No orders found for this email."

    return render(request, "shop/tracker.html", context)



def search(request):
    return HttpResponse("We are at Search")




def productview(request, myid):
    product = Product.objects.get(product_id=myid)
    print(product)

    return render(request, "shop/productView.html", {"product" : product})



def checkout(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        cart_data = request.POST.get("cart_data")  # JSON from hidden input

        if all([first_name, last_name, email, address, city, state, pincode, cart_data]):
            # Save the order
            order = Order.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                address=address,
                city=city,
                state=state,
                pincode=pincode
            )

            # Parse the cart JSON and save each item
            cart = json.loads(cart_data)
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product_name=item["name"],
                    price=item["price"],
                    quantity=item["quantity"]
                )

            return redirect(reverse("Checkout") + "?submitted=true")

    return render(request, 'shop/checkout.html')

