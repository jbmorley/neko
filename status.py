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

import argparse
import json
import urllib2
import base64

TYPE_BUILD = 0
TYPE_TEST = 1

TYPE_MAP = {
  "build": TYPE_BUILD,
  "test": TYPE_TEST
}

STATE_RED = 0
STATE_AMBER = 1
STATE_GREEN = 2

STATE_MAP = {
  "disabled": STATE_GREEN,
  "blue": STATE_GREEN,
  "yellow": STATE_AMBER,
  "red": STATE_RED,
  "red_anime": STATE_RED,
}

class Checker:

  def __init__(self, filename):
    self.filename = filename
    self.projects = []

    with open(self.filename, 'r') as file:
      self.configuration = json.load(file)

    if (self.configuration['version'] != 1):
      raise Exception("Unsupported configuration version")

    for name, project in self.configuration['projects'].iteritems():
      p = Project(name, icon = project['icon'])

      for job in project['jobs']:

        username = None
        password = None
        if ('username' in job):
          username = job['username']
        if ('password' in job):
          password = job['password']

        j = Job(
          url = job['url'],
          type = TYPE_MAP[job['type']],
          username = username,
          password = password)

        p.add(j)

      self.projects.append(p)

  def update(self):

    projects = []

    for project in self.projects:
      status = {
        'state': project.state(),
        'icon': project.icon,
        'name': project.name
      }
      projects.append(status)

    return projects


class Project:

  def __init__(self, name, icon):
    self.name = name
    self.icon = icon
    self.jobs = []

  def add(self, job):
    self.jobs.append(job)

  def state(self):

    summary = STATE_GREEN

    for job in self.jobs:

      # Only check the job state if it's not already red.
      if (summary != STATE_RED):

        state = job.state()
        if (job.type == TYPE_BUILD):
          summary = self.combine_states(summary, state)
        elif (job.type == TYPE_TEST):
          if (state == STATE_GREEN):
            summary = self.combine_states(summary, STATE_GREEN)
          elif (state == STATE_AMBER):
            summary = self.combine_states(summary, STATE_AMBER)
          elif (state == STATE_RED):
            summary = self.combine_states(summary, STATE_AMBER)

    return summary

  def combine_states(self, state1, state2):
    return min(state1, state2)


class Job:

  def __init__(self, url, type = TYPE_BUILD, username = None, password = None):
    self.url = url
    self.type = type
    self.username = username
    self.password = password

  def state(self):

    # Construct the request.
    request = urllib2.Request(self.url)

    # Add the log in details.
    if (self.username and self.password):
      base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
      request.add_header("Authorization", "Basic %s" % base64string)

    # Fetch the upate.
    response = urllib2.urlopen(request)
    content = response.read()
    details = json.loads(content)

    state = STATE_MAP[details['color']]

    return state

