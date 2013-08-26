#!/bin/python

# Include the Dropbox SDK libraries
from dropbox import client, rest, session
import os, sys
# Get your app key and secret from the Dropbox developer website
APP_KEY = ''
APP_SECRET = ''
TOKEN = './access.txt'
# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'dropbox'
sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
drop_client = None

def log_in_or_out(login):
	global drop_client
	if not drop_client:
		if not os.path.isfile(TOKEN):
			request_token = sess.obtain_request_token()

			url = sess.build_authorize_url(request_token, oauth_callback=None)
			print "url:", url
			print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
			raw_input()

			# This will fail if the user didn't visit the above URL and hit 'Allow'
			access_token = sess.obtain_access_token(request_token)
			f = open(TOKEN, 'w')
			f.write('%s|%s' % (access_token.key, access_token.secret))
			f.close()
		elif not login:
			os.remove(TOKEN)
		else:
			f = open(TOKEN, 'r')
			token_key, token_secret = f.read().split('|')
			sess.set_token(token_key,token_secret)

		drop_client = client.DropboxClient(sess)
	else:
		pass

def download(DB_path, local_path):
	f = drop_client.get_file(DB_path).read()
	out = open(local_path, 'w')
	out.write(f)
	out.close()

def upload(local_path,DB_path):
	f = open(local_path, 'rb')
	response = drop_client.put_file(DB_path, f)
	print "uploaded:", response
	f.close()	

def create_volume(DB_path):
	new_folder = drop_client.file_create_folder(DB_path)
	print new_folder

def delete(DB_path):
	deleted_file = drop_client.file_delete(DB_path)
	print deleted_file

def file_data(DB_path):
	folder_metadata = drop_client.metadata(DB_path)
	if len(folder_metadata['contents']) < 1:
		return 'none'
	else:
		dir_items = []
		for folders in folder_metadata['contents']:
			if folders["is_dir"] == False:
				folders["path"] = folders["path"].replace("/","")
			dir_items.append("\t%s\n" % folders["path"])
		return "Dropbox Home:\n" + "".join(dir_items)

def user_data():
	output = []
	user_d = drop_client.account_info()
	for keys in user_d.keys():
		if type(user_d[keys]) == type({}):
			output.append("%s:" % keys)
			for sub_key in user_d[keys].keys():
				output.append('\t%s: %s' % (sub_key, user_d[keys][sub_key]))
		else:
			output.append('%s: %s' % (keys, user_d[keys]))
	return '\n'.join(output)

def search(path, search_string):
	file_list = drop_client.search(path, search_string)
	return file_list

def copy(from_path, to_path):

	"""copies file/folder into new directory. returns metadata on copied file/folder."""

	copied_file = drop_client.file_copy(from_path,to_path)
	return copied_file

