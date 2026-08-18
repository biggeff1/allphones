from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from .models import AgencyMeeting, DepositRequest, InterestRequest, Listing

@staff_member_required
def dashboard(request):
    stats = {
        "listings": Listing.objects.count(),
        "pending_listings": Listing.objects.filter(status="draft").count(),
        "published": Listing.objects.filter(status="published").count(),
        "deposits": DepositRequest.objects.filter(status__in=["new", "review"]).count(),
        "requests": InterestRequest.objects.filter(status__in=["new", "contacted"]).count(),
        "meetings": AgencyMeeting.objects.filter(confirmed=False).count(),
        "margin": Listing.objects.filter(status__in=["published", "reserved", "sold"]).aggregate(total=Sum("margin"))["total"] or 0,
    }
    recent_deposits = DepositRequest.objects.all().order_by("-created_at")[:8]
    pending_listings = Listing.objects.filter(status="draft").order_by("-created_at")[:10]
    recent_requests = InterestRequest.objects.select_related("listing").all()[:8]
    meetings = AgencyMeeting.objects.select_related("request", "request__listing").order_by("date", "time")[:8]
    return render(request, "marketplace/dashboard.html", {"stats": stats, "pending_listings": pending_listings, "recent_deposits": recent_deposits, "recent_requests": recent_requests, "meetings": meetings})
