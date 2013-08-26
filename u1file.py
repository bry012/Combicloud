#!/bin/bash

#### Basics

import sys,traceback

_login_success = False

def import_globals():
   from gobject import MainLoop
   from dbus.mainloop.glib import DBusGMainLoop
   from ubuntuone.platform.credentials import CredentialsManagementTool
   return MainLoop,DBusGMainLoop,CredentialsManagementTool

def log_in_or_out(login):
   
   MainLoop,DBusGMainLoop,CredentialsManagementTool = import_globals()

   global _login_success
   _login_success = False

   DBusGMainLoop(set_as_default=True)
   loop = MainLoop()
   
   def quit(result):
      global _login_success
      loop.quit()
      if result:
         _login_success = True

   cd = CredentialsManagementTool()
   if login:
      d = cd.login()
   else:
      d = cd.clear_credentials()
   d.addCallbacks(quit)
   loop.run()
   if not _login_success and login:
      sys.exit(1)
   

def create_volume(path):
   import ubuntuone.couch.auth as auth
   import urllib
   base = "https://one.ubuntu.com/api/file_storage/v1/volumes/~/"
   auth.request(base + urllib.quote(path), http_method="PUT")

def upload(local, remote):
  import json
  import ubuntuone.couch.auth as auth
  import mimetypes
  import urllib
 
  # Create remote path (which contains volume path)
  base = "https://one.ubuntu.com/api/file_storage/v1/~/"
  answer = auth.request(base + urllib.quote(remote),
                        http_method="PUT",
                        request_body='{"kind":"file"}')
  node = json.loads(answer[1])
 
  # Read info about local file
  try:
    data = bytearray(open(local, 'rb').read())
    size = len(data)
    content_type = mimetypes.guess_type(local)[0]
    content_type = content_type or 'application/octet-stream'
    headers = {"Content-Length": str(size),
             "Content-Type": content_type}

    # Upload content of local file to content_path from original response
    try: 
      base = "https://files.one.ubuntu.com"
      url = base + urllib.quote(node.get('content_path'), safe="/~")
      auth.request(url, http_method="PUT",
                   headers=headers, request_body=data)
    except TypeError:
      dirs = remote.split('/')
      print dirs[0] + ' is not a volume'

  except IOError as e:
    print local + ":\n\tI/O error({0}): {1}".format(e.errno, e.strerror)



def download(remote, local):
    import json
    import ubuntuone.couch.auth as auth
    import urllib
    
    # Request metadata
    base = 'https://one.ubuntu.com/api/file_storage/v1/~/'
    answer = auth.request(base + urllib.quote(remote))
    node = json.loads(answer[1])
    if node.get('content_path'):
      try:
        # Request content
        base = "https://files.one.ubuntu.com"
        url = base + urllib.quote(node.get('content_path'), safe = "/~")
        answer = auth.request(url)
        f = open(local, 'wb')
        f.write(answer[1])
      except:
        print traceback.print_exc()
    else:
      print '%s does not exist' % remote

def get_metadata(path,base):
  import json
  import ubuntuone.couch.auth as auth
  import urllib
 
  # Request user metadata
  url = base + urllib.quote(path) + "?include_children=true"
  answer = auth.request(url)
  return answer

def user_data():
  import json, urllib
  output = []
  base = "https://one.ubuntu.com/api/file_storage/v1"
  answer = get_metadata("",base)
  node = json.loads(answer[1])
  for key in node:
    if not node.get(key):
      pass
    elif type(node.get(key)) == type([]):
      output.append("%s: " % key)
      for key_value in node.get(key):
        key_value = key_value[3::]
        output.append("\t %s" % key_value)
    else:
      output.append("%s: %s" % (key, node.get(key)))
  return '\n'.join(output)

def get_children(path):
  import json, urllib
  base = "https://one.ubuntu.com/api/file_storage/v1/~/"
  answer = get_metadata(path,base)
  # Create file list out of json data
  filelist = []
  node = json.loads(answer[1])
  if answer[0]['status'] != '200':
    print answer[0]['error']
  if node.get('has_children') == True:
    for child in node.get('children'):
      child_path = urllib.unquote(child.get('path')).lstrip('/')
      filelist += [child_path]
  print filelist

def query(path):
  import json
  import ubuntuone.couch.auth as auth
  import urllib
 
  # Request metadata
  base = "https://one.ubuntu.com/api/file_storage/v1/~/"
  url = base + urllib.quote(path)
  answer = auth.request(url)
  node = json.loads(answer[1])
 
  # Print interesting info
  print 'Size:', node.get('size')

def delete(path):
  import ubuntuone.couch.auth as auth
  import urllib
  base = "https://one.ubuntu.com/api/file_storage/v1/~/"
  auth.request(base + urllib.quote(path), http_method="DELETE")
 

