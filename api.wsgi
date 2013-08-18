#!/usr/bin/env python
# 
# Copyright (c) 2013 Jason Barrie Morley.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE. 

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


