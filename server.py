#!/usr/bin/env python

import wsgiref
import wsgiref.simple_server
import cgi
import json
from summary import Checker, Project, Job


def application(environ, start_response):

  component = wsgiref.util.shift_path_info(environ)
  if (component == None or component == ""):

    # Default page - serve index.html
    start_response('200 OK', [('Content-type', 'text/html')])
    f = open('index.html', 'r')
    return [f.read()]

  elif (component == "api"):

    # Fetch the build status and return the appropriate JSON.
    start_response('200 OK', [('Content-type', 'application/json')])
    checker = Checker("/Users/jbmorley/Desktop/configuration.json")
    return [json.dumps(checker.update())]

  else:

    # 404.
    start_response("404 Not Found", [('Content-type', 'text/plain')])
    return ['Page not found']


def main():

  httpd = wsgiref.simple_server.make_server('', 8000, application)
  print "Serving HTTP on port 8000..."
  httpd.serve_forever()


if __name__ == '__main__':
  main()