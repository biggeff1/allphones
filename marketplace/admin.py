from django.contrib import admin
from .models import AgencyMeeting, InterestRequest, Listing

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "brand", "model", "public_price", "margin", "status", "created_at")
    list_filter = ("category", "condition", "status")
    search_fields = ("title", "brand", "model", "seller_reference")
    readonly_fields = ("public_price", "created_at", "updated_at")

@admin.register(InterestRequest)
class InterestRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "full_name", "phone", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("full_name", "phone", "email")
    readonly_fields = ("created_at",)

@admin.register(AgencyMeeting)
class AgencyMeetingAdmin(admin.ModelAdmin):
    list_display = ("request", "date", "time", "office", "confirmed")
    list_filter = ("confirmed", "date")
