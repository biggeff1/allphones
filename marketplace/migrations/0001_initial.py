from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Listing", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=180)), ("category", models.CharField(choices=[("phone","Téléphone"),("computer","Ordinateur")], max_length=20)),
            ("brand", models.CharField(max_length=80)), ("model", models.CharField(max_length=120)),
            ("condition", models.CharField(choices=[("used","Seconde main"),("refurbished","Reconditionné")], default="used", max_length=20)),
            ("description", models.TextField()), ("seller_reference", models.CharField(blank=True, help_text="Référence interne; jamais affichée au public", max_length=120)),
            ("acquisition_price", models.DecimalField(decimal_places=2, help_text="Prix convenu avec le déposant, privé", max_digits=12)),
            ("margin", models.DecimalField(decimal_places=2, default=0, help_text="Marge AllPhones, privée", max_digits=12)),
            ("public_price", models.DecimalField(decimal_places=2, default=0, max_digits=12)), ("currency", models.CharField(default="USD", max_length=3)),
            ("location", models.CharField(default="Lubumbashi", max_length=120)), ("status", models.CharField(choices=[("draft","Brouillon"),("published","Publié"),("reserved","Réservé"),("sold","Vendu")], default="draft", max_length=20)),
            ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
        ]),
        migrations.CreateModel(name="InterestRequest", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("full_name", models.CharField(max_length=160)), ("phone", models.CharField(max_length=40)), ("email", models.EmailField(blank=True, max_length=254)),
            ("message", models.TextField(blank=True)), ("preferred_date", models.DateField(blank=True, null=True)), ("preferred_time", models.TimeField(blank=True, null=True)),
            ("status", models.CharField(choices=[("new","Nouvelle"),("contacted","Traitée par AllPhones"),("meeting","Rencontre planifiée"),("completed","Terminée"),("cancelled","Annulée")], default="new", max_length=20)),
            ("agency_notes", models.TextField(blank=True)), ("created_at", models.DateTimeField(auto_now_add=True)),
            ("listing", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="interest_requests", to="marketplace.listing")),
        ], options={"ordering":["-created_at"]}),
        migrations.CreateModel(name="AgencyMeeting", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")), ("date", models.DateField()), ("time", models.TimeField()),
            ("office", models.CharField(default="Bureau AllPhones", max_length=180)), ("agency_notes", models.TextField(blank=True)), ("confirmed", models.BooleanField(default=False)),
            ("request", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="meeting", to="marketplace.interestrequest")),
        ]),
    ]
