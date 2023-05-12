from django.db import models
from me_pays_app.models.users import *

class Balance_Logs(models.Model):

    enduser_id = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    cashier_id = models.ForeignKey(Cashier, on_delete=models.CASCADE)
    amount = models.FloatField()

class Credit_Share_Logs(models.Model):

    sender_id = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    recipient_id = models.ForeignKey(EndUser, on_delete=models.CASCADE)
    amount = models.FloatField()







    