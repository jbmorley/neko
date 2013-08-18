#!/usr/bin/env python

import wsgiref
import wsgiref.simple_server
import cgi
import json
import os.path
import sys

# Ensure the current directory is in the include path under mod_wsgi.
ROOT = os.path.join(os.path.dirname(__file__))
if (not ROOT in sys.path):
  sys.path.insert(1, ROOT)

from summary import Checker, Project, Job


def application(environ, start_response):

  # Fetch the build status and return the appropriate JSON.
  start_response('200 OK', [('Content-type', 'application/json')])
  checker = Checker("/home/jbmorley/configuration.json")
  return [json.dumps(checker.update())]


