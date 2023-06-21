from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from . import forms, models


@login_required
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        photo = form.save(commit=False)
        photo.uploader = request.user
        photo.save()
        return redirect('login')
    return render(request, 'appreview/photo_upload.html', context={'form': form})


@login_required
def home(request):
    photos = models.Photo.objects.all()
    products = models.Appreview.objects.all()
    return render(request, 'appreview/home.html', context={'photos': photos, 'products': products})


@login_required
def product_and_photo_upload(request):
    product_form = forms.ProductForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        product_form = forms.ProductForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([product_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            product = product_form.save(commit=False)
            product.author = request.user
            product.photo = photo
            product.save()
            return redirect('home')
    context = {
        'product_form': product_form,
        'photo_form': photo_form,
    }
    return render(request, 'appreview/newproduct.html', context=context)


@login_required
def view_product(request, product_id):
    product = get_object_or_404(models.Appreview, id=product_id)
    return render(request, 'appreview/view_product.html', {'product': product})
