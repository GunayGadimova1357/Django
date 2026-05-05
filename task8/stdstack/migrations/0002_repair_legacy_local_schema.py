from django.db import migrations


def table_names(schema_editor):
    return set(schema_editor.connection.introspection.table_names())


def column_names(schema_editor, table):
    return {
        column.name
        for column in schema_editor.connection.introspection.get_table_description(
            schema_editor.connection.cursor(),
            table,
        )
    }


def repair_legacy_schema(apps, schema_editor):
    tables = table_names(schema_editor)
    User = apps.get_model("auth", "User")
    Category = apps.get_model("stdstack", "Category")
    UserProfile = apps.get_model("stdstack", "UserProfile")
    ArticleRating = apps.get_model("stdstack", "ArticleRating")
    Bookmark = apps.get_model("stdstack", "Bookmark")

    categories = [
        ("Backend", "backend"),
        ("Frontend", "frontend"),
        ("AI", "ai"),
        ("Cyber security", "cyber-security"),
        ("Cyber sport", "cyber-sport"),
        ("Game Development", "game-development"),
    ]
    for name, slug in categories:
        Category.objects.get_or_create(slug=slug, defaults={"name": name})

    if "stdstack_userprofile" not in tables:
        schema_editor.create_model(UserProfile)
        tables.add("stdstack_userprofile")
    if "stdstack_articlerating" not in tables:
        schema_editor.create_model(ArticleRating)
        tables.add("stdstack_articlerating")
    if "stdstack_bookmark" not in tables:
        schema_editor.create_model(Bookmark)
        tables.add("stdstack_bookmark")

    for user in User.objects.all():
        UserProfile.objects.get_or_create(user=user)

    if "stdstack_article" not in tables:
        return

    article_columns = column_names(schema_editor, "stdstack_article")
    if "status" not in article_columns:
        schema_editor.execute(
            "ALTER TABLE stdstack_article "
            "ADD COLUMN status varchar(20) NOT NULL DEFAULT 'approved'"
        )
    if "author_id" not in article_columns:
        schema_editor.execute("ALTER TABLE stdstack_article ADD COLUMN author_id integer NULL")
        cursor = schema_editor.connection.cursor()
        cursor.execute("SELECT id, author FROM stdstack_article")
        for article_id, legacy_author in cursor.fetchall():
            username = legacy_author or "legacy_author"
            user, _ = User.objects.get_or_create(username=username[:150])
            UserProfile.objects.get_or_create(user=user)
            cursor.execute(
                "UPDATE stdstack_article SET author_id = %s WHERE id = %s",
                [user.pk, article_id],
            )
        schema_editor.execute(
            "CREATE INDEX IF NOT EXISTS stdstack_article_author_id_idx "
            "ON stdstack_article(author_id)"
        )


class Migration(migrations.Migration):
    dependencies = [
        ("stdstack", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(repair_legacy_schema, migrations.RunPython.noop),
    ]
