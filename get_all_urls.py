# get_all_urls.py
import os
import django
from django.urls import get_resolver


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")  # <- путь к settings.py
django.setup()

def get_all_urls():
    urlconf = get_resolver()
    urls = []

    def extract(patterns, prefix=""):
        for entry in patterns:
            if hasattr(entry, 'url_patterns'):
                extract(entry.url_patterns, prefix + str(entry.pattern))
            else:
                urls.append(prefix + str(entry.pattern))

    extract(urlconf.url_patterns)

    for url in urls:
        print(url)

if __name__ == "__main__":
    get_all_urls()