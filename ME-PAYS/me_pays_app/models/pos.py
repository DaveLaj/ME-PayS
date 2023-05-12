from django.db import models

# Create your models here.
class menu(models.Model):
    menu_name = models.CharField(max_length=50)
    menu_price = models.IntegerField()
    menu_owner = models.ForeignKey("me_pays_app.CustomUser", verbose_name="menu_owner", on_delete=models.CASCADE, null=True)
    menu_is_active = models.BooleanField(default=True, null=True)
    # class Meta:
    #     db_table ="menu"