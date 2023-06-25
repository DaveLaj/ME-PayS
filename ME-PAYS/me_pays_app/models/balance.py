from django.db import models
from me_pays_app.models.users import *

class Balance_Logs(models.Model):
    account_Owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='account_balance_logs')
    enduser_sender = models.ForeignKey(EndUser, null=True, blank=True, on_delete=models.CASCADE, related_name='sender_balance_logs')
    cashier_sender = models.ForeignKey(Cashier, null=True, blank=True, on_delete=models.CASCADE, related_name='cashier_balance_logs')
    pos_sender = models.ForeignKey(POS, null=True, blank=True, on_delete=models.CASCADE, related_name='pos_balance_logs')
    amount = models.FloatField()
    desc = models.CharField(max_length=255, blank=False)
    datetime = models.DateTimeField(auto_now_add=True, null=True) 
    def __str__(self):
        return f"Balance Log #{self.pk}"



# class Credit_Share_Logs(models.Model):

#     sender_id = models.ForeignKey(EndUser, on_delete=models.CASCADE)
#     recipient_id = models.ForeignKey(EndUser, on_delete=models.CASCADE)
#     amount = models.FloatField()







    