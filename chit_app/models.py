from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chit(models.Model):
    name = models.CharField(max_length=30)
    month = models.IntegerField()
    year = models.IntegerField()
    # start_date = models.DateField()
    amount = models.IntegerField()
    number_of_months = models.IntegerField()
    people_present = models.IntegerField()# this is equivalent to number of chits allocated
    user = models.ManyToManyField(User)

    def __str__(self):
        return self.name

class Lifted(models.Model):
    lifted = models.BooleanField(default= False)
    lift_request = models.IntegerField(default = 0)#0 for not requested, 1 for requested, 2 for granted and cannot be modified further
    amount = models.IntegerField(default=0)
    user = models.ForeignKey(User, related_name='user', on_delete= models.CASCADE)
    chit = models.ForeignKey(Chit, related_name='chit', on_delete=models.CASCADE)

    def __str__(self):
        return self.lifted