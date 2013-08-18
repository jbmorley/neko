#!/usr/bin/env python

import wsgiref
import wsgiref.simple_server
import cgi
import json
import os.path
import sys

# Ensure the current directory is in the include path under mod_wsgi.
ROOT = os.path.join(os.path.dirname(__file__))
CONFIG = os.path.join(ROOT, "config.json")
if (not ROOT in sys.path):
  sys.path.insert(1, ROOT)

import status


def application(environ, start_response):

  # Fetch the build status and return the appropriate JSON.
  start_response('200 OK', [('Content-type', 'application/json')])
  checker = status.Checker(CONFIG)
  return [json.dumps(checker.update())]


