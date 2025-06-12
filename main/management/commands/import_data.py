from collections import Counter
import csv
import os
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from main import models


class Command(BaseCommand):
    help = "Import products in BookTime"

    def add_arguments(self, parser):
        parser.add_argument("csvfile", type=argparse.FileType('r'))
        parser.add_argument("image_basedir", type=str)

    def handle(self, *args, **options):
        c = Counter()
        reader = csv.DictReader(options["csvfile"])

        for row in reader:
            product, created = models.Product.objects.get_or_create(
                name=row["name"],
                defaults={
                    "price": row["price"],
                    "description": row["description"],
                    "slug": slugify(row["name"])
                }
            )

            if not created:
                # Update existing product with new data
                product.price = row["price"]
                product.description = row["description"]
                product.slug = slugify(row["name"])
                product.save()

            for import_tag in row["tags"].split("|"):
                tag_name = import_tag.strip()
                tag, tag_created = models.ProductTag.objects.get_or_create(name=tag_name)
                product.tags.add(tag)
                c["tags"] += 1
                if tag_created:
                    c["tags_created"] += 1

            image_path = os.path.join(options["image_basedir"], row["image_filename"])
            if os.path.exists(image_path):
                with open(image_path, "rb") as f:
                    image = models.ProductImage(
                        product=product,
                        image=ImageFile(f, name=row["image_filename"])
                    )
                    image.save()
                    c["images"] += 1

            c["products"] += 1
            if created:
                c["products_created"] += 1

        self.stdout.write(f"Products processed={c['products']} (created={c['products_created']})")
        self.stdout.write(f"Tags processed={c['tags']} (created={c['tags_created']})")
        self.stdout.write(f"Images processed={c['images']}")
