from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from .forms import InterestRequestForm
from .models import Listing

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
            obj = form.save(commit=False)
            obj.listing = listing
            obj.save()
            messages.success(request, "Votre demande a été reçue. AllPhones vous contactera pour organiser la suite.")
            return redirect("listing_detail", pk=listing.pk)
    else:
        form = InterestRequestForm()
    return render(request, "marketplace/interest.html", {"listing": listing, "form": form})
