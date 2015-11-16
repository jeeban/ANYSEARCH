import subprocess
import os
import pickle
from gi.repository import Gtk

class AnySearch_modules() :

	def __init__( self) :

		self.path_database = {}
		self.file_database = {}
		self.filename_list = set()

		self.search_keyword = ""
		self.search_result = set()
		self.database_loading_completed = False

		try:
			print("anysearch_log : Database is empty. Loading from the saved file.")
			self.path_database = pickle.load( open( "path.database", "rb" ) )
			self.file_database = pickle.load( open( "file.database", "rb" ) )
			self.filename_list = pickle.load( open( "file_id.database", "rb" ) )
			print("anysearch_log : Database initialized.")
			self.database_loading_completed = True

		except Exception:
			print( 'no database found' )
			self.database_loading_completed = False




	def list_drive_letters( self ):
		""" list all the fixed drives (local hard disks) present on the computer """
		drivelist = subprocess.Popen('fsutil fsinfo drives', stdout=subprocess.PIPE).communicate()
		drivelist = str(drivelist)[15:-15].split('\\\\')
		for letter in drivelist:
			if "Fixed Drive" in str(subprocess.Popen('fsutil fsinfo driveType '+letter, stdout=subprocess.PIPE).communicate()):
				yield letter.lstrip()+"\\"



	def build_database( self, parent, mode) :
	
		print("creating the databse now")
		print( parent, 'printing parent' )
		temp_path_database = {}	#store the path details. { path_id : path }
		temp_file_database = {}	#store the file details. { file_id : path_id }
		temp_file_id_list = set()	#store all file_id list

		try :
			path_id = 1
			#start searching from the individual entries in basepath_list
			#for basepath in basepath_list :
			for basepath in self.list_drive_letters():
				print(basepath)
				for path, dirs, files in os.walk(os.path.abspath( basepath )):
					
					#print(path)
					#testcode
					path_used = False
					for entry in files:
						if entry in temp_file_id_list:
							temp_file_database[ entry].append( path_id)
							path_used = True
						else:
							if all(ord(c) < 255 for c in entry) == True:	#its a valid file. can be used without any issue
								temp_file_id_list.add( entry)
								temp_file_database[ entry] = [ path_id ]
								path_used = True
							else:
								pass

					#associate the selected path_id with all the files in the current path
					if path_used == True :
						#add path detail to database
						temp_path_database[ path_id ] = path
						path_id += 1

			
			try:
				#store the db to the file
				pickle.dump( temp_file_database, open( "file.database", "wb" ), -1)
				pickle.dump( temp_path_database, open( "path.database", "wb" ), -1)
				pickle.dump( temp_file_id_list, open( "file_id.database", "wb" ), -1)
				print("anysearch_log : new database created. path database initialized.")

			except Exception :
				print("anysearch_log :(database creation failed.")
				raise
				
			self.path_database = temp_path_database
			self.file_database = temp_file_database
			self.filename_list = temp_file_id_list
			#everything went correct 
			
			print(parent, 'parent')
			parent.response( Gtk.ResponseType.OK )

		except Exception as error:
			print( error )
			parent.response( Gtk.ResponseType.CANCEL )





	
	def search_for_keyword( self ) :

		temp_search_result_indexing = set()
		self.search_result = set()

		for keys in self.file_database :
			if keys.lower().endswith( self.search_extension_type ) :
				temp_search_result_indexing.add( keys )

		print( len(temp_search_result_indexing))

		#print("keyword = " + self.search_keyword )

		for entry in temp_search_result_indexing :
			if self.search_keyword in entry :
				self.search_result.add( entry )
			#	print( entry )

		#print( "total file found : ", len(self.search_result))
