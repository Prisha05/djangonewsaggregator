

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='add_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
