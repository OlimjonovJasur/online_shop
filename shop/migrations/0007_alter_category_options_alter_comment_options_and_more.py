# Generated by Django 5.1.5 on 2025-02-04 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_comment_is_negative'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['my_order'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['my_order']},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['my_order']},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['my_order'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AddField(
            model_name='category',
            name='my_order',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='my_order',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='my_order',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='my_order',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
