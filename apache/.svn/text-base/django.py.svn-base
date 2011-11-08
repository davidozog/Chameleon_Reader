import os
import sys

path1 = '/home/dave/School/CIS522/cis522f11_2g/trunk/GameReader/'
path2 = '/home/dave/School/CIS522/cis522f11_2g/trunk/'
sys.path.append(path1)
sys.path.append(path2)

print sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'GameReader.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
