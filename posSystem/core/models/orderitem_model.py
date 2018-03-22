from django.db import models
from .menu_model import Menu


class OrderItem(models.Model):
    menu_item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return "%s %s" % (self.quantity, self.menu_item)

    def get_price(self):
        """Return the total price of this item."""
        return self.menu_item.price * self.quantity

    def get_price_display(self):
        """Get the price in a displayable format."""
        return "£%.2f" % self.get_price()

    def reduce_item_stock(self):
        """Reduce the stock count of the menu item by quantity."""
        self.menu_item.stock -= self.quantity
        self.menu_item.save()

    def refund_item_stock(self):
        """Increase the stock count of the menu item by quantity."""
        self.menu_item.stock += self.quantity
        self.menu_item.save()
