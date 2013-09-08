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
		local_path = file_name[-1]
		return local_path

class File_Movement(Universal_Use):
	def __init__(self):
		self.client_dict = {"Dropbox":dropbox2, "Ubuntu":u1file, "Local": False}
		self.client_names = self.client_dict.keys()
		self.from_client = ""
		self.to_client = ""
		self.to_client_path = ""
		self.from_client_path = ""
		self.from_client = ""

	def split_client_and_path(self,from_client=None,to_client=None):
		
		self.from_client, self.from_client_path = from_client.split(":")

		#checks if a to_client was passed to function.
		if to_client:
			self.to_client, self.to_client_path = to_client.split(":")

		return self.from_client,self.from_client_path,self.to_client,self.to_client_path

	def copy(self,from_client,to_client):

		self.split_client_and_path(from_client,to_client)

		#checks if to_client is Local. If it is, file_name doesn't prepend "/temp/" to to_client_path.
		if not self.client_dict[self.to_client]:
			local_path = self.file_name(self.to_client_path)
		#checks if from_client is Local. If it is, file_name doesn't prepend "/temp/" to from_client_path.
		elif not self.client_dict[self.from_client]:
			local_path = self.file_name(self.from_client_path)
		else:
			if not os.path.isdir("./temp"):
				os.makedir("./temp")
			local_path = self.file_name("/temp/" + self.from_client_path)

		try:
			if self.from_client in self.client_names and self.to_client in self.client_names:
				#Checks if from_client is Local. If it is, it skips the client specific download
				if not self.client_dict[self.from_client]:
					pass
				else:
					self.client_dict[self.from_client].download(self.from_client_path,local_path)
				#Checks if to_client is Local. If it is, it skips the client specific upload
				if not self.client_dict[self.to_client]:
					pass
				else:
					self.client_dict[self.to_client].upload(local_path, self.to_client_path)
			else:
				print "%s or %s client not supported" % (self.from_client, self.to_client)
				return
			if not self.client_dict[self.from_client] or not self.client_dict[self.to_client]:
				pass
			else:
				os.remove(local_path)
			print "success"
			return True
		except Exception, err:
			print traceback.print_exc()
			return False

	def delete(self,path_to_file,format_path):
		#Checks copy function format_path to see if client needs to be separated from the command line argument (whether copy was run before)
		if format_path:
			self.split_client_and_path(path_to_file)
		confirm = raw_input("Are you sure you would like to delete %s? Y/n" % (path_to_file))
		if confirm == "Y" or confirm == "y":

			#If from_client is Local, remove file from local file system
			if not self.client_dict[self.from_client]:
				os.remove(self.from_client_path)

			#If not Local, remove file from designated client
			else:
				self.client_dict[self.from_client].delete(self.from_client_path)

	def mkdir(self,path_to_new_dir,):
		self.split_client_and_path(path_to_new_dir)
		if not self.client_dict[self.from_client]:
			os.mkdir(self.from_client_path)

		else:
			self.client_dict[self.from_client].create_volume(self.from_client_path)

dropbox2.log_in_or_out(True)
u1file.log_in_or_out(True)

main_func = File_Movement()
uni_func = Universal_Use()

if len(sys.argv) > 1:
	if sys.argv[1] == "cp":
		#sys.argv[2] = from_client, sys.argv[3] = to_client
		main_func.copy(sys.argv[2], sys.argv[3])

	elif sys.argv[1] == "mv":
		#sys.argv[2] = from_client, sys.argv[3] = to_client
		copy_success = main_func.copy(sys.argv[2], sys.argv[3])
		if copy_success:
			main_func.delete(sys.argv[2],sys.argv[3],False)

	elif sys.argv[1] == "rm":
		#sys.argv[2] = from_client, sys.argv[3] = to_client
		main.func.delete(sys.argv[2],True)

	elif sys.argv[1] == "mkdir":
		#sys.argv[2] = path to folder
		main_func.mkdir(sys.argv[2],)

	elif sys.argv[1] =="user_info":
		main_func.user_data()

