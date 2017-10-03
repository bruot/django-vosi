import os
import sys
sys.path.append('..')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
	'tests',
	'vosi',
]
SECRET_KEY = 'This is a secret key for testing'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  os.path.join(BASE_DIR, 'provdb.sqlite3'),
    }
}
ROOT_URLCONF = 'tests.urls'
