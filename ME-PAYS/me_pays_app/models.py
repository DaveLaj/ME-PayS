from django.db import models

# Create your models here.
class menu(models.Model):
    menu_name = models.CharField(max_length=50)
    menu_price = models.IntegerField()

    class Meta:
        db_table ="menu"