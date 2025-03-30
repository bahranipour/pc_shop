from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order, OrderItem, Category
from .forms import OrderForm,SignUpForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.core.validators import MaxValueValidator
from django.contrib.auth import login
from django.db import transaction,IntegrityError



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request,'ثبت نام شما با موفقیت انجام شد')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})



def product_list(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    category = None

    
    product_list = Product.objects.filter(stock__gt=0)
    if category_id:
        category = get_object_or_404(Category,id=category_id)
        product_list = product_list.filter(category_id=category_id)

    paginator = Paginator(product_list, 10)
    page_number = request.GET.get('page', 1)
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        products = paginator.page(paginator.num_pages)
    
    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'category':category,
    })

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'store/product_detail.html', {'product': product})

@login_required
@transaction.atomic
def create_order(request, product_id):
    try:
        product = get_object_or_404(Product, pk=product_id)
        
        if request.method == 'POST':
            form = OrderForm(request.POST, max_quantity=product.stock)
            if form.is_valid():
                quantity = form.cleaned_data['quantity']

                if quantity <= 0:
                    messages.error(request, 'تعداد باید بیشتر از صفر باشد')
                    return redirect('product_detail', pk=product_id)
                    
                if quantity > product.stock:
                    messages.error(request, 'موجودی کافی نیست')
                    return redirect('product_detail', pk=product_id)
                
                # کاهش موجودی انبار
                product.stock -= quantity
                product.save()
                
                # ایجاد سفارش
                order = Order.objects.create(
                    user=request.user,
                    total_price=product.price * quantity,
                    status='pending'
                )
                
                # ایجاد آیتم سفارش
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
                
            
                
                messages.success(request, 'سفارش شما با موفقیت ثبت شد!')
                return redirect('order_detail', order_id=order.id)
            else:
                messages.error(request, 'لطفاً اطلاعات را صحیح وارد کنید')
        else:
            form = OrderForm(initial={'quantity': 1}, max_quantity=product.stock)
    except IntegrityError:
        messages.error(request, 'خطا در ثبت سفارش')
        return redirect('product_detail', pk=product_id)
        
    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'store/product_detail.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})