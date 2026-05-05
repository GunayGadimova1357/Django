from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Registers the `excerpt` field in Django's migration state.
    The column already exists in the SQLite DB (created by 0003 raw SQL),
    so we only update the state — no database operation needed.
    """

    dependencies = [
        ("stdstack", "0004_add_avatar_to_userprofile"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(
                    "UPDATE stdstack_article SET excerpt = '' WHERE excerpt IS NULL",
                    migrations.RunSQL.noop,
                ),
            ],
            state_operations=[
                migrations.AddField(
                    model_name="article",
                    name="excerpt",
                    field=models.TextField(
                        blank=True,
                        default="",
                        verbose_name="Excerpt",
                        help_text="If left empty, the preview will be generated from the article text.",
                    ),
                ),
            ],
        ),
    ]
