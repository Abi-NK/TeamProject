from django.db import models


class StockManager(models.Manager):
    def reduce_stock(self, json):
        """Take a JSON description of an order and reduce each item's stock appropriately."""
        print(json)
        for item_id, quantity in json.items():
            item = Menu.objects.get(pk=item_id)
            print("%s current: %s" % (item, item.stock))
            item.stock -= quantity
            item.save()
            print("%s updated: %s" % (item, item.stock))


class Menu(models.Model):

    # Table attributes
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=1000)
    course = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    allergy = models.CharField(max_length=1000, default="")
    calories = models.IntegerField(default=0)
    image = models.CharField(max_length=1000, default='na')
    vegetarian = models.BooleanField(default=False)
    vegan = models.BooleanField(default=False)
    meat = models.BooleanField(default=False)
    stock = models.IntegerField(default=0)
    removed = models.BooleanField(default=False)

    objects = models.Manager()
    stock_manager = StockManager()

    def __str__(self):
        return "%s (%s)" % (self.name, self.course)
