# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0005_auto_20141129_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='owningList',
            field=models.ForeignKey(default=None, to='lists.List'),
            preserve_default=True,
        ),
    ]
