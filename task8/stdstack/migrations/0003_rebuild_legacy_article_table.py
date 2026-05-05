from django.db import migrations


def columns(schema_editor, table):
    return {
        column.name
        for column in schema_editor.connection.introspection.get_table_description(
            schema_editor.connection.cursor(),
            table,
        )
    }


def rebuild_legacy_article_table(apps, schema_editor):
    if schema_editor.connection.vendor != "sqlite":
        return

    table_names = set(schema_editor.connection.introspection.table_names())
    if "stdstack_article" not in table_names:
        return

    article_columns = columns(schema_editor, "stdstack_article")
    legacy_columns = {"author", "likes", "dislikes"}
    if not legacy_columns.intersection(article_columns):
        return

    User = apps.get_model("auth", "User")
    fallback_user, _ = User.objects.get_or_create(username="legacy_author")
    cursor = schema_editor.connection.cursor()
    cursor.execute(
        "UPDATE stdstack_article SET author_id = %s WHERE author_id IS NULL",
        [fallback_user.pk],
    )

    schema_editor.execute("PRAGMA foreign_keys=OFF")
    schema_editor.execute(
        """
        CREATE TABLE stdstack_article_new (
            id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            title varchar(200) NOT NULL,
            image varchar(100) NOT NULL,
            excerpt text NOT NULL,
            content text NOT NULL,
            status varchar(20) NOT NULL,
            created_at datetime NOT NULL,
            updated_at datetime NOT NULL,
            author_id integer NOT NULL REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED,
            category_id bigint NOT NULL REFERENCES stdstack_category(id) DEFERRABLE INITIALLY DEFERRED
        )
        """
    )
    schema_editor.execute(
        """
        INSERT INTO stdstack_article_new
            (id, title, image, excerpt, content, status, created_at, updated_at, author_id, category_id)
        SELECT
            id, title, image, excerpt, content, status, created_at, updated_at, author_id, category_id
        FROM stdstack_article
        """
    )
    schema_editor.execute("DROP TABLE stdstack_article")
    schema_editor.execute("ALTER TABLE stdstack_article_new RENAME TO stdstack_article")
    schema_editor.execute(
        "CREATE INDEX stdstack_article_category_id_70796c34 ON stdstack_article(category_id)"
    )
    schema_editor.execute(
        "CREATE INDEX stdstack_article_author_id_f1a4260a ON stdstack_article(author_id)"
    )
    schema_editor.execute(
        "CREATE INDEX stdstack_article_status_084573f3 ON stdstack_article(status)"
    )
    schema_editor.execute("PRAGMA foreign_keys=ON")


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("stdstack", "0002_repair_legacy_local_schema"),
    ]

    operations = [
        migrations.RunPython(rebuild_legacy_article_table, migrations.RunPython.noop),
    ]
