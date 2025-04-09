from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("limits", "0003_auto_20160413_1046"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="limit",
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name="limit",
            name="pool",
        ),
        migrations.RemoveField(
            model_name="limitspool",
            name="user",
        ),
        migrations.DeleteModel(
            name="Limit",
        ),
        migrations.DeleteModel(
            name="LimitsPool",
        ),
    ]
