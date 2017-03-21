# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('rating', '0010_auto_20170316_2323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rate',
            name='comment',
        ),
        migrations.AddField(
            model_name='rate',
            name='content_type',
            field=models.ForeignKey(default=-1, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rate',
            name='object_id',
            field=models.PositiveIntegerField(default=-1),
            preserve_default=False,
        ),
    ]
