from django.conf import settings
from django.db import models

class Listing(models.Model):
    CATEGORY_CHOICES = [("phone", "Téléphone"), ("computer", "Ordinateur")]
    CONDITION_CHOICES = [("used", "Seconde main"), ("refurbished", "Reconditionné")]
    STATUS_CHOICES = [("draft", "En attente"), ("published", "Publié"), ("reserved", "Réservé"), ("sold", "Vendu")]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="listings")
    title = models.CharField(max_length=180)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=80)
    model = models.CharField(max_length=120)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default="used")
    description = models.TextField()
    color = models.CharField(max_length=60, blank=True)
    usage_years = models.PositiveSmallIntegerField(default=0)
    usage_months = models.PositiveSmallIntegerField(default=0)
    purchase_date = models.DateField(null=True, blank=True)
    storage = models.CharField(max_length=60, blank=True)
    ram = models.CharField(max_length=60, blank=True)
    operating_system = models.CharField(max_length=100, blank=True)
    screen_size = models.CharField(max_length=40, blank=True)
    processor = models.CharField(max_length=120, blank=True)
    battery_health = models.CharField(max_length=40, blank=True)
    network = models.CharField(max_length=80, blank=True)
    serial_number = models.CharField(max_length=120, blank=True, help_text="Privé, jamais affiché publiquement")
    imei = models.CharField(max_length=120, blank=True, help_text="Privé, jamais affiché publiquement")
    accessories = models.TextField(blank=True)
    defects = models.TextField(blank=True)
    seller_reference = models.CharField(max_length=120, blank=True, help_text="Référence interne; jamais affichée")
    acquisition_price = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Prix convenu avec le déposant")
    margin = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Marge AllPhones")
    public_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="USD")
    location = models.CharField(max_length=120, default="Lubumbashi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.public_price = self.acquisition_price + self.margin
        super().save(*args, **kwargs)

    @property
    def usage_duration(self):
        parts = []
        if self.usage_years: parts.append(f"{self.usage_years} an(s)")
        if self.usage_months: parts.append(f"{self.usage_months} mois")
        return " et ".join(parts) if parts else "Moins d'un mois / non précisé"

    def __str__(self):
        return f"{self.brand} {self.model} — {self.public_price} {self.currency}"

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="listings/%Y/%m/")
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"Photo #{self.pk} — annonce #{self.listing_id}"

class DepositRequest(models.Model):
    STATUS_CHOICES = [("new", "Nouvelle"), ("review", "En vérification"), ("accepted", "Acceptée"), ("rejected", "Refusée"), ("listed", "Annonce créée")]
    full_name = models.CharField(max_length=160)
    phone = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    category = models.CharField(max_length=20, choices=Listing.CATEGORY_CHOICES)
    brand = models.CharField(max_length=80)
    model = models.CharField(max_length=120)
    condition = models.CharField(max_length=20, choices=Listing.CONDITION_CHOICES, default="used")
    description = models.TextField()
    expected_price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    agency_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Dépôt #{self.pk} — {self.brand} {self.model}"

class InterestRequest(models.Model):
    STATUS_CHOICES = [("new", "Nouvelle"), ("contacted", "Traitée"), ("meeting", "Rencontre planifiée"), ("completed", "Terminée"), ("cancelled", "Annulée")]
    listing = models.ForeignKey(Listing, on_delete=models.PROTECT, related_name="interest_requests")
    full_name = models.CharField(max_length=160)
    phone = models.CharField(max_length=40)
    email = models.EmailField(blank=True)
    message = models.TextField(blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    preferred_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    agency_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created_at"]
    def __str__(self): return f"Demande #{self.pk} — {self.listing}"

class AgencyMeeting(models.Model):
    request = models.OneToOneField(InterestRequest, on_delete=models.CASCADE, related_name="meeting")
    date = models.DateField()
    time = models.TimeField()
    office = models.CharField(max_length=180, default="Bureau AllPhones")
    agency_notes = models.TextField(blank=True)
    confirmed = models.BooleanField(default=False)
    def __str__(self): return f"Rendez-vous #{self.request_id} — {self.date} {self.time}"
