from django.db import models
import json
import random

class Order(models.Model):
    items = models.TextField()
    reference_number = models.CharField(max_length=20, unique=True, null=True)
    school_id = models.IntegerField(null=True)
    paid = models.BooleanField(default=False)
    def set_items(self, items):
        self.items = json.dumps(items)

    def get_items(self):
        return json.loads(self.items)

    def generate_reference_number(self):
        self.reference_number = str(random.randint(100000, 999999))

    def save(self, *args, **kwargs):
        if not self.reference_number:
            self.generate_reference_number()
        super().save(*args, **kwargs)

