import os
import sys

path1 = '/home/dave/School/CIS522/'
path2 = '/home/dave/School/CIS522/Chameleon_Reader/'
sys.path.append(path1)
sys.path.append(path2)

print sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'Chameleon_Reader.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
