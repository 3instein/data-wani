#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/data-wani/deploy-app")

from yourapp import app as application
application.secret_key = 'mbokmutakgeprek'