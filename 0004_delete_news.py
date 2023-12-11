

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_news_add_time'),
    ]

    operations = [
        migrations.DeleteModel(
            name='News',
        ),
    ]
