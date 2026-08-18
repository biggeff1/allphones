from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import DepositRequestForm, InterestRequestForm
from .models import Listing
from .public_forms import PublicListingForm

def home(request):
    listings = Listing.objects.filter(status="published").order_by("-created_at")
    return render(request, "marketplace/home.html", {"listings": listings})

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
            form.save()
            messages.success(request, "Votre proposition a été envoyée à AllPhones. L'agence vous contactera après vérification.")
            return redirect("home")
    else: form = DepositRequestForm()
    return render(request, "marketplace/deposit.html", {"form": form})

def create_listing(request):
    if request.method == "POST":
        form = PublicListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.status = "draft"
            listing.acquisition_price = 0
            listing.margin = 0
            listing.save()
            messages.success(request, "Votre annonce a été envoyée. Elle sera visible uniquement après validation par AllPhones.")
            return redirect("home")
    else:
        form = PublicListingForm()
    return render(request, "marketplace/create_listing.html", {"form": form})
