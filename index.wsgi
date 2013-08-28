import sys
import sae
from baidumusic import wsgi

sys.path.insert(0, 'lib')
application = sae.create_wsgi_app(wsgi.application)
