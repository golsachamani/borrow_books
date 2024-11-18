from django.db import models
from books import models as book_models
from django.contrib.auth.models import User
# Create your models hecla
class OrderItem(models.Model):
    book_instance = models.ForeignKey(book_models.BookInstace,on_delete=models.PROTECT)
    borrow_days = models.PositiveIntegerField()

class Order(models.Model):
    CHOICE_FIELD = (('c','canceled'),('p', 'paid'), ('n', 'none'))
    item = models.ForeignKey(OrderItem, on_delete=models.PROTECT)
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    status = models.BooleanField(default='n',choices=CHOICE_FIELD)




