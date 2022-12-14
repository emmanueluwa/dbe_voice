# Generated by Django 4.1.1 on 2022-09-17 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "anthology",
            "0002_rename_blog_post_publish_493ec4_idx_anthology_p_publish_ca1060_idx",
        ),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="post",
            options={"ordering": ["-publish"]},
        ),
        migrations.RemoveIndex(
            model_name="post",
            name="anthology_p_publish_ca1060_idx",
        ),
        migrations.RenameField(
            model_name="post",
            old_name="published",
            new_name="publish",
        ),
        migrations.AddIndex(
            model_name="post",
            index=models.Index(
                fields=["-publish"], name="anthology_p_publish_f73996_idx"
            ),
        ),
    ]
