# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rating', '0009_auto_20170316_1051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rate',
            old_name='author',
            new_name='user',
        ),
    ]
