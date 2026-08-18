from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("marketplace", "0001_initial")]
    operations = [migrations.CreateModel(name="DepositRequest", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("full_name", models.CharField(max_length=160)), ("phone", models.CharField(max_length=40)), ("email", models.EmailField(blank=True, max_length=254)),
        ("category", models.CharField(choices=[("phone","Téléphone"),("computer","Ordinateur")], max_length=20)),
        ("brand", models.CharField(max_length=80)), ("model", models.CharField(max_length=120)),
        ("condition", models.CharField(choices=[("used","Seconde main"),("refurbished","Reconditionné")], default="used", max_length=20)),
        ("description", models.TextField()), ("expected_price", models.DecimalField(decimal_places=2, max_digits=12)),
        ("currency", models.CharField(default="USD", max_length=3)),
        ("status", models.CharField(choices=[("new","Nouvelle"),("review","En vérification"),("accepted","Acceptée"),("rejected","Refusée"),("listed","Annonce créée")], default="new", max_length=20)),
        ("agency_notes", models.TextField(blank=True)), ("created_at", models.DateTimeField(auto_now_add=True)),
    ])]
