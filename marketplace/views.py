from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .account_forms import MultipleImageForm, RegisterForm
from .forms import DepositRequestForm, InterestRequestForm
from .models import Listing, ListingImage
from .public_forms import PublicListingForm

def home(request):
    listings = Listing.objects.filter(status="published").prefetch_related("images").order_by("-created_at")
    return render(request, "marketplace/home.html", {"listings": listings})

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(); login(request, user)
            messages.success(request, "Votre compte AllPhones a été créé.")
            return redirect("create_listing")
    else: form = RegisterForm()
    return render(request, "marketplace/register.html", {"form": form})

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk, status="published")
    return render(request, "marketplace/detail.html", {"listing": listing})

def interest(request, pk):
    listing = get_object_or_404(Listing, pk=pk, status="published")
    if request.method == "POST":
        form = InterestRequestForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False); obj.listing = listing; obj.save()
            messages.success(request, "Votre demande a été reçue. AllPhones vous contactera pour organiser la suite.")
            return redirect("listing_detail", pk=listing.pk)
    else: form = InterestRequestForm()
    return render(request, "marketplace/interest.html", {"listing": listing, "form": form})

def deposit(request):
    if request.method == "POST":
        form = DepositRequestForm(request.POST)
        if form.is_valid():
            form.save(); messages.success(request, "Votre proposition a été envoyée à AllPhones."); return redirect("home")
    else: form = DepositRequestForm()
    return render(request, "marketplace/deposit.html", {"form": form})

@login_required
def create_listing(request):
    if request.method == "POST":
        form = PublicListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.status = "draft"
            listing.acquisition_price = 0
            listing.margin = 0
            listing.save()
            messages.success(request, "Annonce enregistrée. Ajoutez maintenant vos photos; AllPhones la validera avant publication.")
            return redirect("add_listing_images", pk=listing.pk)
    else: form = PublicListingForm()
    return render(request, "marketplace/create_listing.html", {"form": form})

@login_required
def add_listing_images(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user, status="draft")
    if request.method == "POST":
        form = MultipleImageForm(request.POST, request.FILES)
        if form.is_valid():
            files = form.cleaned_data["images"]
            for index, image in enumerate(files):
                ListingImage.objects.create(listing=listing, image=image, is_primary=(index == 0 and not listing.images.exists()))
            messages.success(request, "Photos reçues. Votre annonce est maintenant en attente de validation.")
            return redirect("home")
    else: form = MultipleImageForm()
    return render(request, "marketplace/listing_images.html", {"listing": listing, "form": form})
