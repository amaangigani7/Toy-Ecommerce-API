from django.test import TestCase
from main.models import *
from django.core import serializers
# Create your tests here.

# purge_old_data.py

# from django.core.management.base import BaseCommand, CommandError
# from cus_leads.models import CustomerLeads
# from datetime import datetime, timedelta
#
# class Command(BaseCommand):
#     help = 'Delete objects older than 10 days'
#
#     def handle(self, *args, **options):
#         CustomerLeads.objects.filter(posting_date__lte=datetime.now()-timedelta(days=10)).delete()
#         self.stdout.write('Deleted objects older than 10 days')

# products = Product.objects.all()
# for i in products:
#     sp = SimilarProduct()
#     sp.product = i
#     sp.slug = "hoppity-rabbit"
#     sp.save()
#     sp = SimilarProduct()
#     sp.product = i
#     sp.slug = "humanzee"
#     sp.save()
#     sp = SimilarProduct()
#     sp.product = i
#     sp.slug = "opero-numero"
#     sp.save()
# lis = ['marble-fun',
#  'tellurian-orrery',
#  'sailboat',
#  'glider',
#  'dot-the-numbers',
#  'opero-numero']
#  # for i in products[:]:
# for i in lis:
#     sp = SpecialProduct()
#     sp.product = Product.objects.filter(slug=i)[0]
#     sp.type = "Classics"
#     sp.save()
# lis = ["Schools", "NGOs", 'Hobby Centers','Clubs']
# for i in lis:
# count = 0
# while (0 <= count <= 5):
# mcr = GlobalReview.objects.all()
# for i in mcr:
#     i.img_link = "https://ik.imagekit.io/928tx6iiq/Glider_3_dRBp1xMrtG.jpg?ik-sdk-version=javascript-1.4.3&updatedAt=1653069341372"
#     i.save()
