import sys , os.path

import pygtk
pygtk.require('2.0')
import gtk

import operator as op

from OpenGL.GL import *

import numpy as np

from glwidget import GLDrawingArea

from eulers import EulersScene
from quaternions import QuaternionsScene

import transformations as tr


ui_file = "queuler.ui"

class App(object):
	"""Application main class"""

	def __init__(self):

		self.button = {}
		self.move = [0,0,0]

		self.dirskeys = ( ( ['w'] , ['s'] ) , ( ['a'] , ['d'] ) , ( ['e'] , ['q'] ) )

		for d in self.dirskeys :
			for e in d :
				for i in range(len(e)) : e[i] = ( gtk.gdk.unicode_to_keyval(ord(e[i])) , False )

		self.near = 1
		self.far = 1000
		self.fov  = 60

		builder = gtk.Builder()
		builder.add_from_file(ui_file)

		glconfig = self.init_glext()

		self.drawing_area = GLDrawingArea(glconfig)
		self.drawing_area.set_events( gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.BUTTON1_MOTION_MASK | gtk.gdk.BUTTON2_MOTION_MASK |gtk.gdk.BUTTON3_MOTION_MASK )
		self.drawing_area.set_size_request(320,240)

		builder.get_object("vbox1").pack_start(self.drawing_area)

		win_main = builder.get_object("win_main")
		self.save_diag = builder.get_object("save_dialog")
		self.open_diag = builder.get_object("open_dialog")
		self.leuler      = builder.get_object("leuler")
		self.lquaternion = builder.get_object("lquaternion")

		win_main.set_events( gtk.gdk.KEY_PRESS_MASK | gtk.gdk.KEY_RELEASE_MASK )

		win_main.connect('key-press-event'  , self._on_key_pressed  )
		win_main.connect('key-release-event', self._on_key_released )

		self.qscene = QuaternionsScene( 10.0 , self.fov , .01 , self.near , self.far )
		self.escene = EulersScene( 10.0 , self.fov , .01 , self.near , self.far )
		self.drawing_area.add( self.escene , (0, 0,1,.5) )
		self.drawing_area.add( self.qscene , (0,.5,1,.5) )

		self.qscene.set_matrix( tr.identity_matrix() , tr.identity_matrix() )
		self.escene.set_matrix( tr.identity_matrix() , tr.identity_matrix() )
		print 'Scene added'

		win_main.show_all()

		width = self.drawing_area.allocation.width
		height = self.drawing_area.allocation.height / 2.0
		ratio = float(width)/float(height)

		self.qscene.set_ratio( ratio )
		self.escene.set_ratio( ratio )

		builder.connect_signals(self)

#        self.statbar = builder.get_object('statbar')

		self.drawing_area.connect('motion_notify_event',self._on_mouse_motion)
		self.drawing_area.connect('button_press_event',self._on_button_pressed)
		self.drawing_area.connect('button_release_event',self._on_button_released)
		self.drawing_area.connect('configure_event',self._on_reshape)
		self.drawing_area.connect_after('expose_event',self._after_draw)

		self.anim = False
		gtk.timeout_add( 1 , self._refresh )

	def on_anim_toggle( self , widget , data=None ) :
		if self.anim :
			self.on_stop()
		else :
			self.on_start()

	def on_start( self ) :
		self.anim = True

	def on_stop( self ) :
		self.anim = False

	def _refresh( self ) :
		self.leuler.set_text( str(self.escene) )
		self.lquaternion.set_text( str(self.qscene) )
		self.qscene.step( self.anim )
		self.escene.step( self.anim )
		self.drawing_area.queue_draw()
		return True

	def _after_draw( self , widget , data=None ) :
		self.update_statusbar()

	def update_statusbar( self ) :
		pass

	def _on_reshape( self , widget , data=None ) :
		width = self.drawing_area.allocation.width
		height = self.drawing_area.allocation.height / 2.0

		ratio = float(width)/float(height)

		self.qscene.set_screen_size( width , height )
		self.escene.set_screen_size( width , height )

	def _on_button_pressed( self , widget , data=None ) :
		if data.button == 1 or data.button == 2 or data.button == 3 :
			self.mouse_pos = data.x , data.y
		self.button[data.button] = True
		self._refresh()

	def _on_button_released( self , widget , data=None ) :
		self.button[data.button] = False


	def _on_mouse_motion( self , widget , data=None ) :
		diff = map( op.sub , self.mouse_pos , (data.x , data.y) )

		self.qscene.mouse_move( diff , self.button )
		self.escene.mouse_move( diff , self.button )

		self.mouse_pos = data.x , data.y
		self._refresh() 

#        gtk.gdk.Keymap

	def _on_key_pressed( self , widget , data=None ) :
		if not any(self.move) :
			gtk.timeout_add( 20 , self._move_callback )

		for i in range(len(self.dirskeys)) :
			if (data.keyval,False) in self.dirskeys[i][0] :
				self.dirskeys[i][0][ self.dirskeys[i][0].index( (data.keyval,False) ) ] = (data.keyval,True)
				self.move[i]+= 1
			elif (data.keyval,False) in self.dirskeys[i][1] :
				self.dirskeys[i][1][ self.dirskeys[i][1].index( (data.keyval,False) ) ] = (data.keyval,True)
				self.move[i]-= 1

	
	def _on_key_released( self , widget , data=None ) :
		for i in range(len(self.dirskeys)) :
			if (data.keyval,True) in self.dirskeys[i][0] :
				self.dirskeys[i][0][ self.dirskeys[i][0].index( (data.keyval,True) ) ] = (data.keyval,False)
				self.move[i]-= 1
			elif (data.keyval,True) in self.dirskeys[i][1] :
				self.dirskeys[i][1][ self.dirskeys[i][1].index( (data.keyval,True) ) ] = (data.keyval,False)
				self.move[i]+= 1

	def _move_callback( self ) :
		self.qscene.key_pressed( self.move )
		self.escene.key_pressed( self.move )
		self._refresh()
		return any(self.move)

	def init_glext(self):
		# Query the OpenGL extension version.
#        print "OpenGL extension version - %d.%d\n" % gtk.gdkgl.query_version()

		# Configure OpenGL framebuffer.
		# Try to get a double-buffered framebuffer configuration,
		# if not successful then try to get a single-buffered one.
		display_mode = (
				gtk.gdkgl.MODE_RGB    |
				gtk.gdkgl.MODE_DEPTH  |
				gtk.gdkgl.MODE_STENCIL|
				gtk.gdkgl.MODE_DOUBLE )
		try:
			glconfig = gtk.gdkgl.Config(mode=display_mode)
		except gtk.gdkgl.NoMatches:
			display_mode &= ~gtk.gdkgl.MODE_DOUBLE
			glconfig = gtk.gdkgl.Config(mode=display_mode)

#        print "is RGBA:",                 glconfig.is_rgba()
#        print "is double-buffered:",      glconfig.is_double_buffered()
#        print "is stereo:",               glconfig.is_stereo()
#        print "has alpha:",               glconfig.has_alpha()
#        print "has depth buffer:",        glconfig.has_depth_buffer()
#        print "has stencil buffer:",      glconfig.has_stencil_buffer()
#        print "has accumulation buffer:", glconfig.has_accum_buffer()
#        print

		return glconfig

	def on_reload( self , widget , data=None ):
		self.qscene.reset()
		self.escene.reset()

	def on_quit(self,widget,data=None):
		gtk.main_quit()

	def on_open( self, widget , data=None ):
		chooser = gtk.FileChooserDialog(
		  	  title=None,
		  	  action=gtk.FILE_CHOOSER_ACTION_SAVE,
		  	  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK)
		  	  )
		chooser.set_current_folder( os.path.dirname(sys.argv[0]) )
		filter = gtk.FileFilter()
		filter.set_name('Numpy dumps')
		filter.add_pattern('*.npy')
		filter.add_pattern('*.npz')
		chooser.add_filter(filter)
		if chooser.run() == gtk.RESPONSE_OK :
			arr = np.load(chooser.get_filename())
			self.qscene.set_matrix( arr['begin'] , arr['end'] )
			self.escene.set_matrix( arr['begin'] , arr['end'] )
		chooser.destroy()

	def on_save( self, widget , data=None ):
		chooser = gtk.FileChooserDialog(
		  	  title=None,
		  	  action=gtk.FILE_CHOOSER_ACTION_SAVE,
		  	  buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK)
		  	  )
		chooser.set_current_folder( os.path.dirname(sys.argv[0]) )
		chooser.set_do_overwrite_confirmation(True)
		if chooser.run() == gtk.RESPONSE_OK :
			np.savez(chooser.get_filename(),
					begin = self.qscene.get_beg_matrix(),
					end   = self.qscene.get_end_matrix() )
		chooser.destroy()

if __name__ == '__main__':
	app = App()
	gtk.main()

