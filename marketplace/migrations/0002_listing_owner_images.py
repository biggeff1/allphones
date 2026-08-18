from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("marketplace", "0001_initial"),
    ]
    operations = [
        migrations.AddField(model_name="listing", name="owner", field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="listings", to=settings.AUTH_USER_MODEL)),
        migrations.CreateModel(name="ListingImage", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("image", models.ImageField(upload_to="listings/%Y/%m/")),
            ("is_primary", models.BooleanField(default=False)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("listing", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="images", to="marketplace.listing")),
        ]),
    ]
