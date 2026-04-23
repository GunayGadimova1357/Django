from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Review
from .forms import ReviewForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')

    next_url = request.GET.get('next') or request.POST.get('next') or '/'
    context = {'next': next_url}

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        context['username'] = username

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url)

        context['error'] = 'Invalid username or password.'

    return render(request, 'registration/login.html', context)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return render(request, 'registration/logged_out.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'review/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.select_related('user')
    form = ReviewForm()

    return render(request, 'review/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form
    })


@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', pk=pk)

        reviews = product.reviews.select_related('user')
        return render(request, 'review/product_detail.html', {
            'product': product,
            'reviews': reviews,
            'form': form,
        })

    return redirect('product_detail', pk=pk)


@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=review.product.pk)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'review/review_form.html', {'form': form})


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        product_pk = review.product.pk
        review.delete()
        return redirect('product_detail', pk=product_pk)

    return render(request, 'review/confirm_delete.html', {'review': review})
