# Generated by Django 4.1 on 2022-12-21 01:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("group", "0011_jointime_remove_group_members_group_member_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="group", old_name="member", new_name="members",
        ),
    ]
