from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "store/product_detail.html", {"product": product})


def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    items = []
    total = 0
    for p in products:
        qty = cart[str(p.id)]
        line_total = qty * p.price
        total += line_total
        items.append({'product': p, 'quantity': qty, 'line_total': line_total})
    return render(request, 'store/cart.html', {'items': items, 'total': total})


def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    pid = str(pk)
    if pid in cart:
        if cart[pid] > 1:
            cart[pid] -= 1
        else:
            del cart[pid]
        request.session['cart'] = cart
    return redirect('cart')


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})


@login_required(login_url='login')
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    items = OrderItem.objects.filter(order=order)
    return render(request, 'store/order_detail.html', {'order': order, 'items': items})


@login_required(login_url='login')
def place_order(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    total = sum(
        Product.objects.get(id=int(pid)).price * int(qty)
        for pid, qty in cart.items()
    )

    if request.method == 'POST':
        full_name = request.POST['full_name']
        phone = request.POST['phone']
        address = request.POST['address']
        payment_method = request.POST['payment_method']

        # store temporarily for online payment
        request.session['tmp_name'] = full_name
        request.session['tmp_phone'] = phone
        request.session['tmp_address'] = address

        if payment_method == 'cash':
            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                address=address,
                total=total,
                payment_method='cash',
            )
            for pid, qty in cart.items():
                product = Product.objects.get(id=int(pid))
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=int(qty),
                    price=product.price,
                )
            request.session['cart'] = {}
            return render(request, 'store/order_success.html', {'order': order})
        else:
            return redirect('fake_payment')

    return render(request, 'store/checkout.html', {'total': total})


@login_required(login_url='login')
def fake_payment(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')

    total = sum(
        Product.objects.get(id=int(pid)).price * int(qty)
        for pid, qty in cart.items()
    )

    if request.method == 'POST':
        full_name = request.session.get('tmp_name', '')
        phone = request.session.get('tmp_phone', '')
        address = request.session.get('tmp_address', '')

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            total=total,
            payment_method='online',
        )
        for pid, qty in cart.items():
            product = Product.objects.get(id=int(pid))
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=int(qty),
                price=product.price,
            )
        request.session['cart'] = {}
        return render(request, 'store/order_success.html', {'order': order})

    return render(request, 'store/payment_page.html', {'total': total})
