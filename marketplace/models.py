from django.db import models

class Listing(models.Model):
    CATEGORY_CHOICES = [("phone", "Téléphone"), ("computer", "Ordinateur")]
    CONDITION_CHOICES = [("used", "Seconde main"), ("refurbished", "Reconditionné")]
    STATUS_CHOICES = [("draft", "Brouillon"), ("published", "Publié"), ("reserved", "Réservé"), ("sold", "Vendu")]

    title = models.CharField(max_length=180)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=80)
    model = models.CharField(max_length=120)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default="used")
    description = models.TextField()
    seller_reference = models.CharField(max_length=120, blank=True, help_text="Référence interne; jamais affichée au public")
    acquisition_price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Prix convenu avec le déposant, privé")
    margin = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Marge AllPhones, privée")
    public_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default="USD")
    location = models.CharField(max_length=120, default="Lubumbashi")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.public_price = self.acquisition_price + self.margin
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model} — {self.public_price} {self.currency}"

class InterestRequest(models.Model):
    STATUS_CHOICES = [("new", "Nouvelle"), ("contacted", "Traitée par AllPhones"), ("meeting", "Rencontre planifiée"), ("completed", "Terminée"), ("cancelled", "Annulée")]
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

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Demande #{self.pk} — {self.listing}"

class AgencyMeeting(models.Model):
    request = models.OneToOneField(InterestRequest, on_delete=models.CASCADE, related_name="meeting")
    date = models.DateField()
    time = models.TimeField()
    office = models.CharField(max_length=180, default="Bureau AllPhones")
    agency_notes = models.TextField(blank=True)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Rendez-vous #{self.request_id} — {self.date} {self.time}"
