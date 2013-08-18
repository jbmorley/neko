#!/usr/bin/env python

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
      p = Project(name, image = project['image'])

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
        'image': project.image,
        'name': project.name
      }
      projects.append(status)

    return projects


class Project:

  def __init__(self, name, image):
    self.name = name
    self.image = image
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


def main():
  """Run the script."""
  parser = argparse.ArgumentParser(description = 'Summarize the status of a collection of builds.')
  parser.add_argument("configuration", help = 'Configuration file specifying the build jobs to check.')
  options = parser.parse_args()

  checker = Checker(options.configuration)
  print json.dumps(checker.update())

if __name__ == "__main__":
  main()