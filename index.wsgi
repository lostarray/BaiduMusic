import sae
from baidumusic import wsgi

application = sae.create_wsgi_app(wsgi.application)
