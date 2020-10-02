#!/usr/bin/env python3

#**********************
#*
#* Progam Name: MP1. Membership Protocol.
#*
#* Current file: submit.py
#* About this file: Submission python script.
#*
#***********************

# UPDATE LOG:
# Originally designed for Python 2.
# Updated 20191024 with Python2/3 compatibility, further diagnostics
# Updated Fall 2020 for MP revision, h/cpp source upload as zip

# MAINTAINER NOTES:
# Make sure the assignment key (akey) and Part IDs (partIds) in this script
# are up to date for the current installation of the assignment. Look in the
# definition of the submit function.

# This message was primarily meant for MOOC students
print('\nREQUIREMENTS: To work on this assignment, we assume you already know how to')
print('program in C++, you have a working Bash shell environment set up (such as')
print('Linux, or Windows 10 with WSL installed for Ubuntu Linux and a Bash shell,')
print('or macOS with developer tools installed and possibly additional Homebrew')
print('tools. If you are not clear yet what these things are, then you need to')
print('take another introductory course before working on this assignment. The')
print('University of Illinois offers some intro courses on Coursera that will help')
print('you understand these things and set up your work environment.\n')

import hashlib
import random
import email
import email.message
import email.encoders
# import StringIO # unused
import sys
import subprocess
import json
import os
import os.path
import base64
from io import BytesIO
from zipfile import ZipFile

# Python2/3 compatibility hacks: ----------------------------

# The script looks for this file to make sure it's the right working directory
anchoring_file = 'Application.cpp'

# Message displayed if compatibility hacks fail
compat_fail_msg = '\n\nERROR: Python 3 compatibility fix failed.\nPlease try running the script with the "python2" command instead of "python" or "python3".\n\n'
wrong_dir_msg = '\n\nERROR: Please run this script from the same directory where ' + anchoring_file + ' is.\n\n'

if not os.path.isfile(anchoring_file):
  print(wrong_dir_msg)
  raise Exception(wrong_dir_msg)
else:
  #print('Found file: ' + anchoring_file)
  pass

try:
  raw_input
except:
  # NameError
  try:
    raw_input = input
  except:
    raise Exception(compat_fail_msg)

# urllib2 hacks based on suggestions by Ed Schofield.
# Link: https://python-future.org/compatible_idioms.html?highlight=urllib2
try:
  # Python 2 versions
  from urlparse import urlparse
  from urllib import urlencode
  from urllib2 import urlopen, Request, HTTPError
except ImportError:
  # Python 3 versions
  try:
    from urllib.parse import urlparse, urlencode
    from urllib.request import urlopen, Request
    from urllib.error import HTTPError
  except:
    raise Exception(compat_fail_msg)

# End of compatibility hacks ---------------------------

def submit():
  print('==\n== Submitting Solutions \n==')

  (login_email, token) = loginPrompt()
  if not login_email:
    print('!! Submission Cancelled')
    return

  # debug log runner:
  # script_process = subprocess.Popen(['bash', 'run.sh', str(0)])
  # output = script_process.communicate()[0]
  # return_code = script_process.returncode
  # if return_code is not 0:
  #   raise Exception('ERROR: Build script failed during compilation. See error messages above.')
  # submissions = [read_dbglog(i) for i in range(3)]

  # src = read_codefile("MP1Node.cpp")
  # submissions = [src, src, src]
  # submitSolution(login_email, token, submissions)

  # Assignment Key from the programming assignment setup:
  akey = 'mg8YcRJOQvG_GF2VDVWwFQ'
  # The Part ID shown on Coursera when this grading part was created:
  partIds = ['epZ7n', 'L2OvG', 'VGHIC']
  # Descriptive names for each part to use in messages in this script:
  # (These don't have to match anything in the Coursera setup exactly)
  partFriendlyNames = ['Single Failure', 'Multiple Failure', 'Message Drop Single Failure']

  # Currently submitting the same bundle for each part
  b64zip = b64zip_from_files(["MP1Node.h", "MP1Node.cpp"])
  submissions = [b64zip, b64zip, b64zip]

  submitSolution(login_email, token, akey, submissions, partFriendlyNames, partIds)

# =========================== LOGIN HELPERS - NO NEED TO CONFIGURE THIS =======================================

class NullDevice:
  def write(self, s):
    pass

def loginPrompt():
  """Prompt the user for login credentials. Returns a tuple (login, token)."""
  (login_email, token) = basicPrompt()
  return login_email, token

def basicPrompt():
  """Prompt the user for login credentials. Returns a tuple (login, token)."""
  print('Please enter the email address that you use to log in to Coursera.')
  login_email = raw_input('Login (Email address): ')
  print('To validate your submission, we need your submission token.\nThis is the single-use key you can generate on the Coursera instructions page for this assignment.\nThis is NOT your own Coursera account password!')
  token = raw_input('Submission token: ')
  return login_email, token

def partPrompt(partFriendlyNames, partIds):
  print('Hello! These are the assignment parts that you can submit:')
  counter = 0
  for part in partFriendlyNames:
    counter += 1
    print(str(counter) + ') ' + partFriendlyNames[counter - 1])
  partIdx = int(raw_input('Please enter which part you want to submit (1-' + str(counter) + '): ')) - 1
  return (partIdx, partIds[partIdx])

def submit_url():
  """Returns the submission url."""
  return "https://www.coursera.org/api/onDemandProgrammingScriptSubmissions.v1"

def submitSolution(email_address, token, akey, submissions, partFriendlyNames, partIds):
  """Submits a solution to the server. Returns (result, string)."""

  num_submissions = len(submissions)
  if len(partFriendlyNames) != num_submissions:
    raise Exception('Config error: need one friendly name per submission item')
  if len(partIds) != num_submissions:
    raise Exception('Config error: need one part ID per submission item')

  parts_dict = dict()
  i = 0
  for p_ in partIds:
    parts_dict[partIds[i]] = {"output": submissions[i]}
    i += 1

  values = {
    "assignmentKey": akey,
    "submitterEmail": email_address,
    "secret": token,
    "parts": parts_dict
  }
  url = submit_url()
  # (Compatibility update) Need to encode as utf-8 to get bytes for Python3:
  data = json.dumps(values).encode('utf-8')
  req = Request(url)
  req.add_header('Content-Type', 'application/json')
  req.add_header('Cache-Control', 'no-cache')
  response = urlopen(req, data)
  return

## Read a debug log
def read_dbglog(partIdx):
  # open the file, get all lines
  f = open("dbg.%d.log" % partIdx)
  src = f.read()
  f.close()
  #print src
  return src

## Read a source code file
def read_codefile(filename):
  # open the file, get all lines
  f = open(filename)
  src = f.read()
  f.close()
  #print src
  return src

# Given a list of filenames, construct a zipfile in memory,
# and return it encoded as a b64 string
def b64zip_from_files(filenames):
  if len(filenames) < 1:
    raise Exception("filenames list is empty")
  buf = BytesIO()
  zipbuf = ZipFile(buf, mode='w')
  for filename in filenames:
    zipbuf.write(filename)
  zipbuf.close()
  buf.seek(0)
  b64str = base64.b64encode(buf.read()).decode('ascii')
  buf.close()
  return b64str

def cleanup():
    for i in range(3):
        try:
            os.remove("dbg.%s.log" % i)
        except:
            pass

try:
  submit()
  print('\n\nSUBMISSION FINISHED!\nYou can check your grade on Coursera.\n\n');
except HTTPError:
  print('ERROR:\nSubmission authorization failed. Please check that your submission token is valid.')
  print('You can generate a new submission token on the Coursera instructions page\nfor this assignment.')

# For dbg.*.log only:
# cleanup()
