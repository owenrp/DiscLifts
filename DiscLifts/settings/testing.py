from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db_testing'
     }
}


FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
    )
