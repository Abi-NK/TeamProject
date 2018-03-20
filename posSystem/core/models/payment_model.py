from django.db import models


class Payment(models.Model):
    """This model is for payment. Payment stores the payment info and is connected to a order"""
    card_holder = models.CharField(max_length=50, default='na')     # name of card holder
    card_number = models.CharField(max_length=16, default='na')     # Card number
    cvc = models.CharField(max_length=3, default='na')              # CVC
    expiry = models.CharField(max_length=5, default='na')           # Card expiry date
    terms_conditions = models.BooleanField(default=False)           # Customer has accepted t and c
    payment_requested = models.BooleanField(default=False)          # Waiter has asked for payment
    payment_received = models.BooleanField(default=False)           # Payment information has been received
    payment_accepted = models.BooleanField(default=False)           # Waiter has accepted the payment

    def __str__(self):
        return "Order: %s, Accepted: %s" % (self.id, self.payment_accepted)

    def get_payments(self):
        """Returns all the payments"""
        print("Payments sent")
        return Payment.objects.all()

    def get_card_holder(self):
        """Return card holder"""
        return self.card_holder()

    def get_card_number(self):
        """Return card number"""
        return self.card_number()

    def get_cvc(self):
        """Return card cvc"""
        return self.cvc()

    def get_card_expiry(self):
        """Return card expiry"""
        return self.expiry()

    def get_t_and_c(self):
        """Return card T and C"""
        return self.terms_conditions()

    def get_payment_requested(self):
        """Return payment requested"""
        return self.payment_requested()

    def get_payment_received(self):
        """Return payment received"""
        return self.payment_received()

    def get_payment_accepted(self):
        """Return payment accepted"""
        return self.payment_accepted()

    def set_t_and_c(self):
        """Sets the terms and conditions to be accepted"""
        self.terms_conditions = True
        self.save()
        print("Customer %s has accepted the Terms and conditions" % self.id)

    def set_payment_requested(self):
        """Sets the payment to be requested"""
        self.payment_requested = True
        self.save()
        print("Customer %s payment has been requested" % self.id)

    def set_payment_received(self):
        """Sets the payment to be received"""
        self.payment_received = True
        self.save()
        print("Customer %s payment has been received" % self.id)

    def set_payment_accepted(self):
        """Sets the payment to be accepted"""
        self.payment_accepted = True
        self.save()
        print("Customer %s payment has been accepted" % self.id)
