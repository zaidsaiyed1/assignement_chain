from django.db import models
from accounts.models import CustomUser

# Create your models here.


class Event(models.Model):
              title = models.CharField(max_length=200)
              description = models.TextField()
              organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
              location = models.CharField(max_length=200)
              start_date = models.DateField()
              end_date = models.DateField()
              is_public = models.BooleanField(default=True)
              created_at = models.DateTimeField(auto_now_add=True)
              updated_at = models.DateTimeField(auto_now=True)
              def __str__(self):
                  return self.title

class RSVP(models.Model):
              event = models.ForeignKey(Event, on_delete=models.CASCADE)
              user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
              status = models.CharField(max_length=20, choices=[('Going', 'Going'),('Not Going', 'Not Going'),('Maybe', 'Maybe'),])
              def __str__(self):
                  return f"{self.user.email} - {self.event.title} - {self.status}"

class Review(models.Model):
              event = models.ForeignKey(Event, on_delete=models.CASCADE)
              user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
              rating = models.IntegerField()
              comment = models.TextField(blank=True)
              def __str__(self):
                  return f"{self.user.email} - {self.event.title} - {self.rating}"