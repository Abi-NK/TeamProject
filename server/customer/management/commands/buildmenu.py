from django.core.management.base import BaseCommand
from customer.models import Menu


class Command(BaseCommand):
    help = 'Clears and repopulates the Menu table with a sample menu.'

    sample_menu = [
        # [name, price, description, course, category, vegetarian]
        # Main - Classics
        ["Yucatecan grilled chicken", 12.45, "Chargrilled chicken breast marinated in achiote, citrus & oregano. Served with green rice, pink pickled onions & our fresh house slaw", "Main", "Classics", False],
        ["British steak, the Mexican way", 13.45, "Marinated bavette steak, served medium rare with green rice, grilled spring onion salsa & our fresh house slaw", "Main", "Classics", False],
        ["Grilled MSC cod with green olive & herb", 12.75, "Sustainably sourced cod, flash-grilled, served with our fresh house slaw, green rice & lime", "Main", "Classics", False],
        ["Winter vegetable enchiladas", 9.50, "Fire roasted poblano peppers & crushed new potato folded into 2 corn tortillas, with a rich tomato salsa & grilled cheese. Served with a green leaf salad", "Main", "Classics", True],
        ["Chicken and tomato enchiladas", 10.85, "Two corn tortillas stuffed with grilled chicken in a spiced tomato sauce, topped with melted cheese. Served with a green leaf salad", "Main", "Classics", False]
    ]

    def handle(self, *args, **options):
        print("Deleting all entries in Menu table...")
        Menu.objects.all().delete()
        print("Deleted.")
        print("Adding sample menu item...")
        Menu(
            name="Pork pibil",
            price=7.80,
            description="Slow cooked, with pink pickled onions",
            course="Main",
            category="Burritos"
        ).save()
        print("Added.")
