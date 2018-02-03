from django.core.management.base import BaseCommand
from customer.models import Menu


class Command(BaseCommand):
    help = 'Clears and repopulates the Menu table with a sample menu.'

    sample_menu = [
        # this sample menu is taken from Wahaca's menu, found at https://www.wahaca.co.uk/menu/food/
        # [name, price, description, course, category, vegetarian]
        # Nibbles
        ["Guacamole with tortilla chips", 4.75, "Freshly made every day with Hass avocados, lime and coriander", "Nibbles", "", True],
        ["Roast tomato salsa & tortilla chips", 3.85, " Charred & mashed with fresh lime & a touch of chilli", "Nibbles", "", True],
        ["Frijoles & tortilla chips", 3.85, "Creamy twice-cooked black beans", "Nibbles", "", True],
        # Street Food - Classic Tacos
        ["Pork pibil", 4.60, "The original, and still the best! Slow braised shoulder of pork cooked in Yucatecan spices & orange, with fiery pink pickled onions", "Street Food", "Classic Tacos", False],
        ["Grilled chicken and avocado", 4.95, "Chicken thigh with sweet ancho chilli, fresh guacamole & tomatillo salsa", "Street Food", "Classic Tacos", False],
        ["Grilled British steak", 4.95, "Flash-grilled skirt steak with chipotle salsa", "Street Food", "Classic Tacos", False],
        ["Fire-roasted poblano pepper & corn", 4.10, "With crushed new potatoes, herbs & ancho mayo", "Street Food", "Classic Tacos", True],
        ["Plantain", 4.40, "With sweet & spicy chipotle adobo & a crumble of feta", "Street Food", "Classic Tacos", True],
        # Street Food - Tostadas & Taquitos
        ["Corn & black bean tostadas", 3.95, "With creamy guacamole, ancho chilli oil & feta on crisp tortillas ", "Street Food", "Tostadas & Taquitos", True],
        ["Smoked salmon tostadas", 5.75, "With cucumber, chipotle mayo, white slaw and avocado on crisp tortillas", "Street Food", "Tostadas & Taquitos", False],
        ["Sweet potato & feta taquito", 4.50, "Roast sweet potato, feta & caramelised onion wrapped in a crispy blue corn tortilla with salsas & chipotle mayo", "Street Food", "Tostadas & Taquitos", True],
        # Street Food - Quesadillas
        ["Black bean & cheese", 4.50, "Slow cooked smoky black beans with bay & avocado leaf", "Street Food", "Quesadillas", True],
        ["Roast chilli", 4.95, "Roasted serrano chillies & sweet sautéed onions with a crumble of feta.", "Street Food", "Quesadillas", True],
        ["Mexican style chorizo & potato", 5.45, "Trealy Farm sobrasada, with crushed new potatoes & thyme", "Street Food", "Quesadillas", False],
        ["The chicken club", 5.95, "Grilled chicken, avocado, Cos lettuce & chipotle mayo. Our chefs’ favourite", "Street Food", "Quesadillas", False],
        # Main - Classics
        ["Yucatecan grilled chicken", 12.45, "Chargrilled chicken breast marinated in achiote, citrus & oregano. Served with green rice, pink pickled onions & our fresh house slaw", "Main", "Classics", False],
        ["British steak, the Mexican way", 13.45, "Marinated bavette steak, served medium rare with green rice, grilled spring onion salsa & our fresh house slaw", "Main", "Classics", False],
        ["Grilled MSC cod with green olive & herb", 12.75, "Sustainably sourced cod, flash-grilled, served with our fresh house slaw, green rice & lime", "Main", "Classics", False],
        ["Winter vegetable enchiladas", 9.50, "Fire roasted poblano peppers & crushed new potato folded into 2 corn tortillas, with a rich tomato salsa & grilled cheese. Served with a green leaf salad", "Main", "Classics", True],
        ["Chicken and tomato enchiladas", 10.85, "Two corn tortillas stuffed with grilled chicken in a spiced tomato sauce, topped with melted cheese. Served with a green leaf salad", "Main", "Classics", False],
        # Main - Burritos
        ["Pork pibil", 7.80, "Slow cooked, with pink pickled onions", "Main", "Burritos", False],
        ["Chicken tinga", 8.00, " In a smoky tomato chipotle sauce", "Main", "Burritos", False],
        ["Flash-grilled skirt steak", 8.30, " With chipotle salsa & grilled spring onions", "Main", "Burritos", False],
        ["Fire-roasted poblano pepper", 7.45, " With herb-dressed, crushed new potato", "Main", "Burritos", True],
    ]

    def handle(self, *args, **options):
        print("Deleting all entries in Menu table...")
        Menu.objects.all().delete()
        print("Deleted.")
        for item in self.sample_menu:
            print("Adding %s (%s)..." % (item[0], item[3]))
            Menu(
                name=item[0],
                price=item[1],
                description=item[2],
                course=item[3],
                category=item[4],
            ).save()
        print("Sample menu added.")
