try :
	import os
	import random
	import pickle
	import threading
	from gi.repository import Gtk
	import modules
except Exception as error:
	print( "Error: Package Import failed. ( package missing )" )
	print( error)
	exit()


class AnySearch_GUI( Gtk.Window ):

	def __init__( self ) :
		
		
		self.app_modules = modules.AnySearch_modules()

		self.init_msg = '''				         AnySearch V1.0
	      ( A faster then ever file search tool for windows os )

	HOW TO USE AnySearch :
	1. Enter a keyword in the entry box and press the search button.
	2.The search result will be displayed in the result area.
		
		Hopefully you will get your desired file in the first attempt.
	But in case if you got some confusing result, don't worry, you
	still can have one more try.
		To get your file from this confusing list, follow this step:
	1.Select the checkbox just below the entry box.
	2.Now type a new keuword and press the search button.

		This time probably you will get your file in the result. But
	If you still couldn't find your file, again dont worry. You can have
	one more try.
		this time without doing anything, directly enter some more
	keyword in entry box and search. By doing this multiple times,
	you will definitely find your file.

	
		To perform a complete new search, uncheck the check 
	button below the entry box and search your keyword.


							Thanks for using AnySearch
				'''

		self.empty_entry_box_msg = '''\n\n\n\n\n\n\n\n\n
		Error : Empty entry box ( keyword missing )
	
		Please enter some keyword in the search box 
		and then press enter to initiate the search.
				'''



		Gtk.Window.__init__( self, type=0, title="AnySearch_v1.0", resizable=False )
		self.set_position( 3 )
		#self.set_size_request( 600, 400)

		#table to hold all the widgets
		self.table = Gtk.Table( 34, 44, True )
		self.add( self.table )

		######################################################################
		#main search area
		self.search_entry = Gtk.Entry()	#user need to enter keyword in this box
		self.search_button = Gtk.Button( label = "Search" ) #click here to get ur search result
		self.search_type_checking = Gtk.CheckButton( label = "Search again on the current search result" )  #if set search on the current search result
		self.search_type_checking.set_sensitive( False )
		
		self.search_button.connect( "clicked", self.generate_search_result )
		self.search_entry.connect( "activate", self.generate_search_result )

		######################################################################
		#bottom team detail
		self.team_detail = Gtk.Label( label = "Designed by Team OPUSWAY. (www.opusway.com)" )

		######################################################################
		#logo part
		self.logo_image = Gtk.Image()
		self.logo_image.set_from_file( r"logo.png" )

		######################################################################
		#search result area
		self.liststore = Gtk.ListStore( int, str ) #store the search result here
		self.treeview = Gtk.TreeView( model=self.liststore ) #display result in this treeview
		renderer_text1 = Gtk.CellRendererText()
		renderer_text2 = Gtk.CellRendererText()
		column1_text = Gtk.TreeViewColumn( "Folder ID", renderer_text1, text=0 )
		column2_text = Gtk.TreeViewColumn( "Filename", renderer_text2, text=1 )
		self.treeview.append_column(column1_text)
		self.treeview.append_column(column2_text)

		self.search_result_scrolled_window = Gtk.ScrolledWindow() 
		self.search_result_scrolled_window.add( self.treeview ) #manage the treeview into a window
		#self.treeview.connect( "cursor-changed", self.show_preview )

		######################################################################
		#preview part
		self.textview_preview = Gtk.TextView( can_focus = False ) #preview for text based files
		self.textview_buffer = Gtk.TextBuffer()
		self.textview_buffer.set_text( self.init_msg )
		self.textview_preview.set_buffer( self.textview_buffer )
		self.textview_preview.set_editable( False )
		self.textview_preview_scrolled_window = Gtk.ScrolledWindow()
		self.textview_preview_scrolled_window.add( self.textview_preview )

		self.image_preview = Gtk.Image() #preview for images
		#self.image_preview.set_from_file( r"c:\users\miku\desktop\11882831_857616444345692_8762951027327451034_o.jpg" )
		self.image_preview_window = Gtk.AspectFrame()
		self.image_preview_window.add( self.image_preview )

		

		#######################################################################
		#table attach
		self.table.attach( self.search_entry, 4, 16, 1, 3 )
		self.table.attach( self.search_button, 16, 20, 1, 3 )
		self.table.attach( self.search_type_checking, 5, 21, 2, 5 )

		self.table.attach( self.logo_image, 24, 40, 0, 4 )

		self.table.attach( self.search_result_scrolled_window, 2, 22, 5, 32 )
		
		#self.table.attach( self.image_preview_window, 21, 35, 4, 18 )
		self.table.attach( self.textview_preview_scrolled_window, 23, 42, 4, 32 )

		self.table.attach( self.team_detail, 28, 44, 33, 34 )


		#######################################################################
		#prepare table display
		self.connect( "delete-event", self.quit_app )
		self.connect( "destroy", self.quit_app )
		self.show_all()


	def run(self):
		Gtk.main()
	

	def quit_app( self, parent=None, event=None ) :
		#Gtk.main_quit()
		os.system( 'taskkill /F /FI "WINDOWTITLE eq AnySearch_v1.0' )


	def show_result( self ) :

		self.liststore.clear()
		for entry in self.app_modules.search_result :
			self.liststore.append( [ self.app_modules.file_database[entry],  entry.lstrip('|') ] )



	def generate_search_result( self, parent=None, event=None ) :

		#self.app_modules.search_keyword = self.search_entry.get_text()
		#if self.app_modules.search_keyword != ""  :
		if self.search_entry.get_text() != '':
			#self.app_modules.search_for_keyword()
			self.show_result()

		else :
			self.textview_buffer.set_text( self.empty_entry_box_msg )

	
	'''

	def show_preview( self, parent ) :
		#print( self.liststore[ path ][0],"  ::  ", self.liststore[ path ][1] )
		liststore, treeiter = self.treeview.get_selection().get_selected()
		path_id = liststore[treeiter][0]
		file_id = liststore[treeiter][1]
		if file_id.endswith( "jpg" ):#, "jpeg", "png") :
			path = self.app_modules.path_database[ path_id] + '\\' + file_id
			#print(path)
			self.image_preview.set_from_file( path )
	'''



	def start_app( self) :
		
		if self.app_modules.database_loading_completed == False :
			
			self.table.set_sensitive( False )
			dialog = AnySearch_dialog_box.database_missing( parent=self )
			response = dialog.run()
			dialog.destroy()

			if response == -4 :
				self.emit( "destroy" )

			else :
				dialog = AnySearch_dialog_box.database_create( parent=self )
				response = dialog.run()
				dialog.destroy()
				print(response)
				if response == Gtk.ResponseType.OK :
					print("databse created")
					self.table.set_sensitive( True )
					self.search_entry.grab_focus()
				else:
					print("aborted")
					self.emit( "destroy" )
			
			



class AnySearch_dialog_box() :

	class database_missing( Gtk.Dialog ) :

		def __init__( self, parent ) :

			Gtk.Dialog.__init__( self, "AnySearch : Error :: Database missing", parent, 0, resizable=False )
			self.set_position( 4 )

			self.table = Gtk.Table( 5, 13, True )
			self.content_area = self.get_content_area()
			self.content_area.add( self.table )

			self.label = Gtk.Label( "APP_ERROR :  Database missing.\n\nAnySearch won't work without the database." )
			self.confirm_button = Gtk.Button( label="Create Now" )

			self.table.attach( self.label, 0, 13, 0,  3 )
			self.table.attach( self.confirm_button, 4, 9, 3, 4 )

			self.confirm_button.connect( "clicked", self.dialog_response, Gtk.ResponseType.OK )
			self.show_all()

		def dialog_response( self , widget, response_code):

			self.response( response_code )



	class database_create( Gtk.Dialog) :

		def __init__(self, parent) :

			Gtk.Dialog.__init__(self, "AnySearch : Info :: Creating database", parent, 0, resizable=False)#, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
			self.set_position(4)

			self.table = Gtk.Table(6, 13, True)
			self.content_area = self.get_content_area()
			self.content_area.add(self.table)

			self.label1 = Gtk.Label("APP_INFO : Creating database.\nIt may take about 5 minutes.\navg time :  500 gb = 3 min (approx.)")
			self.status_spin = Gtk.Spinner()
			self.status_spin.start()
			self.label2 = Gtk.Label("APP_INFO : Database created.")
			self.continue_to_search = Gtk.Button( label="continue_to_search") 

		#	self.table.attach( self.label2, 1, 12, 1,  5)
		#	self.table.attach( self.continue_to_search, 1, 12, 4, 5)
			self.table.attach( self.label1, 1, 9, 1,  5)
			self.table.attach( self.status_spin, 10, 12, 2, 4)
			self.show_all()

			build_db_thread = threading.Thread( target=parent.app_modules.build_database, args=[self, 1] )
			build_db_thread.start()
			#build_db_thread.wait()

