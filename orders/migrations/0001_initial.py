# Generated by Django 4.2.16 on 2024-11-18 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("books", "0003_alter_author_img_alter_book_img"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("borrow_days", models.PositiveIntegerField()),
                (
                    "book_instance",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="books.bookinstace",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.BooleanField(
                        choices=[("c", "canceled"), ("p", "paid"), ("n", "none")],
                        default="n",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="orders.orderitem",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
