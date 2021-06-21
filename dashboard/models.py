from django.db import models
from users.models import UserProfile


class Event(models.Model):
    event_creator = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(null=False, unique=True)
    dis_image = models.ImageField(upload_to='images/')
    capacity = models.IntegerField(default=100)
    attendance = models.IntegerField(default=0)
    description = models.TextField()
    price = models.FloatField()
    date = models.DateTimeField()

    objects = models.Manager()

    def can_book_seat(self):
        return self.capacity > self.attendance

    def __str__(self):
        return self.name


class Ticket(models.Model):
    attendee = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    book_seat = models.IntegerField(default=1)
    braintree_id = models.CharField(max_length=150, blank=True)

    objects = models.Manager()

    def get_total_cost(self):
        return self.book_seat * self.event.price
