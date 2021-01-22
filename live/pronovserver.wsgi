#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/pronovserver/")

from __init__ import app as application
application.secret_key = 'txbU+2653#'