import pygtk
import gtk
import patterns
import os.path

#todo
#textbuffer.place_cursor(where)
#textview.set_wrap_mode(gtk.WRAP_WORD)
class Base:
  def __init__(self):
		self.cur_filename=''
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("destroy", self.destroy)
		self.window.set_title("python Mozhi")
		self.window.set_border_width(2)
		self.window.set_size_request(600, 400)
		
		#-----------------------------------#
		#					file Selection window			#
		#-----------------------------------#
		self.filew = gtk.FileSelection("File selection")
		self.filew.ok_button.connect("clicked", self.file_ok_sel)
		self.filew.cancel_button.connect("clicked",lambda w: self.filew.destroy())
		self.filew.set_filename("mozhi.txt")
		#-----------------------------------#
		
		box=gtk.VBox(False,0)
		
		#--------------------------#
		#					menu bar				 #
		#--------------------------#	
		menubar = self.get_main_menu()
		box.pack_start(menubar, False, True, 0)
		menubar.show()
		#--------------------------#
		
		
		#--------------------------#
		#					Toolbar					 #
		#--------------------------#
		handlebox = gtk.HandleBox()
		box.pack_start(handlebox, False, False, 5)
		toolbar = gtk.Toolbar()
		toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
		toolbar.set_style(gtk.TOOLBAR_BOTH)
		toolbar.set_border_width(5)
		handlebox.add(toolbar)
		
		iconw = gtk.Image() # icon widget
		iconw.set_from_file("img/exit.png")
		close_button = toolbar.append_item(
			"Close",           # button label
			"Closes this app", # this button's tooltip
			"Private",         # tooltip private info
			iconw,             # icon widget
			self.destroy) # a signal
		toolbar.append_space() # space after item
		
		iconw = gtk.Image() # icon widget
		iconw.set_from_file("img/save.png")
		tooltips_button = toolbar.append_item(
			"Save","Save the Translation",
			"Private",iconw,self.save_trans)
		
		toolbar.show()
		handlebox.show()
		#-----------------------------------#
		
				
		#--------------------------#
		#					TextView				 #
		# to show the translated 	 #
		# malayalam text					 #
		#--------------------------#
		sw_mal = gtk.ScrolledWindow()
		sw_mal.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		self.textmal = gtk.TextView()
		self.textmalbuffer = self.textmal.get_buffer()
		self.textmal.set_editable(False)
		self.textmal.set_wrap_mode(gtk.WRAP_WORD)
		self.textmal.set_border_width(2)
		self.textmal.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(200,192,93))
		
		sw_mal.add(self.textmal)
		self.textmal.show()
		box.pack_start(sw_mal)
		sw_mal.show()
		self.sw_mal=sw_mal
		#--------------------------#
		
		
		seperator=gtk.HSeparator()
		box.pack_start(seperator,False,True,5)
		seperator.show()
		
		
		#--------------------------#
		#					TextView				 #
		# for the input of				 # 
		# manglish text 	 				 #
		#--------------------------#
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
		self.texteng = gtk.TextView()
		self.textengbuffer = self.texteng.get_buffer()
		self.texteng.connect("key_release_event",self.txt_keypress)
		self.texteng.set_wrap_mode(gtk.WRAP_WORD)
		sw.add(self.texteng)
		self.texteng.show()
		box.pack_start(sw)
		sw.show()
		self.texteng.grab_focus()
		#--------------------------#
		
		
		# This packs the box into the window (a GTK container).
		self.window.add(box)
		box.show()
		# The final step is to display this newly created widget.
		self.window.show()
	
	#--------------------------------#
	#						menubar	Object			 #
	#--------------------------------#	
	def get_main_menu(self):
		menu_items = (
					( "/_File",         None,         None, 0, "<Branch>" ),
   				( "/File/_New",     "<control>N", self.menuitem_response, 0, None ),
          ( "/File/_Open",    "<control>O", self.menuitem_response, 0, None ),
          ( "/File/_Save",    "<control>S", self.menuitem_response, 0, None ),
          ( "/File/Save _As", None,         None, 0, None ),
          ( "/File/sep1",     None,         None, 0, "<Separator>" ),
          ( "/File/Quit",     "<control>Q", self.destroy, 0, None ),
          ( "/_Options",      None,         None, 0, "<Branch>" ),
          ( "/Options/Test",  None,         None, 0, None ),
          ( "/_Help",         None,         None, 0, "<LastBranch>" ),
          ( "/_Help/About",   None,         None, 0, None ),
    )
		accel_group = gtk.AccelGroup()
		self.item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
		# This method generates the menu items. Pass to the item factory
		self.item_factory.create_items(menu_items)
		# Attach the new accelerator group to the window.
		self.window.add_accel_group(accel_group)		
		return self.item_factory.get_widget("<main>")
	
	def menuitem_response(self, widget, string):
		name=string.get_label()
		if name=='_Save': self.save_trans()
	
	def save_trans(self,*args):
		self.filew.show()
  #-------------------------------#

	def file_ok_sel(self,w):
		fname=self.filew.get_filename()
		if os.path.lexists(self.filew.get_filename()):
			print 'file already exists'
		else:
			fp=open(fname,'w')
  		st, end = self.textmalbuffer.get_bounds()
  		fp.write(self.textmalbuffer.get_text(st,end))
  		fp.close()
  		self.filew.destroy()
  		
	def destroy(self, widget, data=None):
		print "going to desctory"
		gtk.main_quit()
	
	def move_maltxt_scrollbar(self):
		adj=self.sw_mal.get_vadjustment()#print dir(gtk)
		val=adj.upper-adj.page_size
		adj.set_value(val)
		#print d.type
		
		
	def txt_keypress(self, widget, data=None):
		st, end = self.textengbuffer.get_bounds()
		mang= self.textengbuffer.get_text(st,end)		
		str_res=''
		for w in mang.split(' '):
			str_res+= patterns.transword(w+' ')# + ' '			
		self.textmalbuffer.set_text(str_res.replace('|',''))
		self.move_maltxt_scrollbar()
		#self.sw_mal.set_vadjustment(adj)
		#adj.set_value(val)
		#print adj.upper-(adj.value+adj.page_size)
		#print adj.upper,adj.page_size
		#print help(self.mal_scroll_window.set_vadjustment)
		#self.textmal.scroll_to_iter(self.textmalbuffer.get_end_iter())
		
		
	def main(self):
		gtk.main()


if __name__ == "__main__":
	base = Base()
	base.main()
