# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0005_auto_20170316_1001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='article',
        ),
    ]
