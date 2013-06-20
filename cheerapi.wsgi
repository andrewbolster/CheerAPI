import logging, sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/opt/CheerAPI/')
from __init__ import app as application
