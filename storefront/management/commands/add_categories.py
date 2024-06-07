from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand): 
    help = 'Add predefined categories to the database'

    def handle(self, *args, **kwargs):
        categories = [
            ("Electronics", "Products like smartphones, laptops, cameras, and accessories."),
            ("Clothing", "Various types of apparel including men's, women's, and children's clothing."),
            ("Home Appliances", "Items like refrigerators, washing machines, microwaves, and small kitchen appliances."),
            ("Books", "Different genres of books including fiction, non-fiction, academic, and children's books."),
            ("Beauty and Health", "Products like skincare, haircare, makeup, and wellness items."),
            ("Sports and Outdoors", "Equipment and clothing for sports and outdoor activities."),
            ("Toys and Games", "Products for children including toys, board games, and puzzles."),
            ("Furniture", "Various types of furniture for home and office."),
            ("Automotive", "Car accessories, parts, and tools."),
            ("Groceries", "Food items, beverages, and household essentials."),
        ]

        with connection.cursor() as cursor:
            for name, description in categories:
                cursor.execute(
                    "INSERT INTO storefront_category (name, description) VALUES (%s, %s)",
                    [name, description]
                )

        self.stdout.write(self.style.SUCCESS('Successfully added categories'))
