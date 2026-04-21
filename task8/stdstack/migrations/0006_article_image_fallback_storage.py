from django.db import migrations, models

import stdstack.storage


class Migration(migrations.Migration):
    dependencies = [
        ("stdstack", "0005_remove_article_image_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="article",
            name="image",
            field=models.FileField(
                blank=True,
                help_text="Uploads try Cloudinary first. If it rejects the file, the image is stored locally.",
                storage=stdstack.storage.CloudinaryFallbackStorage(),
                upload_to="articles/",
                verbose_name="Image",
            ),
        ),
    ]
