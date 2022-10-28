from html.parser import HTMLParser

from django.core.management.base import BaseCommand
from accounts.models import Provider


class HTMLFilter(HTMLParser):
    cleaned_text = ""

    def handle_data(self, data):
        self.cleaned_text += data


class Command(BaseCommand):
    help = 'Convert HTML to text'
    notfound = []
    fetched = 0

    def handle(self, *args, **options):
        fields = ["name", "business_name", "description", "short_description", "address"]
        providers = Provider.objects.all()
        for prov in providers:
            print(f"\n{prov.display_name}")

            for field in fields:
                value = getattr(prov, field)
                if value:
                    print(f"  - Removing HTML tags in field [{field}]")
                    html_parser = HTMLFilter()
                    html_parser.feed(value)
                    setattr(prov, field, html_parser.cleaned_text)

            prov.save()
