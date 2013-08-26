#!/bin/python

import dropbox2, u1file
import os, sys, traceback

class Universal_Use():
	def __init__(self):
		pass

	def user_data(self):
		output = []
		dropbox2.log_in_or_out(True)
		output.append('\nDropbox:')
		output.append(dropbox2.user_data())
		output.append(str(dropbox2.file_data('')))
		output.append('\nUbuntu One:')
		output.append(u1file.user_data())
		return '\n'.join(output)

	def file_name(self,file_path):
		file_name = file_path.split('/')
		local_path = './temp/' + file_name[-1]
		return local_path

class File_Movement(Universal_Use):
	def __init__(self):
		self.client_dict = {"Dropbox":dropbox2, "Ubuntu":u1file}
		self.client_names = self.client_dict.keys()
		self.from_client = ""
		self.to_client = ""
		self.to_client_path = ""
		self.from_client_path = ""
		self.from_client = ""

	def copy(self,from_client,to_client):
		self.from_client, self.from_client_path = from_client.split(":")
		self.to_client, self.to_client_path = to_client.split(":")
		local_path = self.file_name(self.from_client_path)

		try:
			if self.from_client in self.client_names and self.to_client in self.client_names:
				self.client_dict[self.from_client].download(self.from_client_path,local_path)
				self.client_dict[self.to_client].upload(local_path, self.to_client_path)
			else:
				print "%s or %s client not supported" % (self.from_client, self.to_client)
				return
			os.remove(local_path)
			print "success"
			return True
		except Exception, err:
			print traceback.print_exc()
			return False


	def move(self,from_client,to_client):
		copy_success = self.copy(from_client,to_client)
		if copy_success:
			self.client_dict[self.from_client].delete(self.from_client_path)

dropbox2.log_in_or_out(True)
u1file.log_in_or_out(True)

main_func = File_Movement()
uni_func = Universal_Use()

if len(sys.argv) > 1:
	if sys.argv[1] == "cp":
		#sys.argv[2] = from_client, sys.argv[3] = to_client
		main_func.copy(sys.argv[2], sys.argv[3])

	if sys.argv[1] == "mv":
		#sys.argv[2] = from_client, sys.argv[3] = to_client
		main_func.move(sys.argv[2], sys.argv[3])

if __name__ == "__main__":
	print uni_func.user_data()

