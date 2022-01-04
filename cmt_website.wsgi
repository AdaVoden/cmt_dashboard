from pyramid.paster import get_add, setup_logging

ini_path = '/var/www/documents/cmt/cmt.ini'
setup_logging(ini_path)
application = get_app(ini_path, 'main')