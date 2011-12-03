import sys

import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

from drawable import Drawable

class Frame( Drawable ) :
	def __init__( self ) :
		Drawable.__init__( self )

	def draw( self ) :
		glColor3f( 1 , 0 , 0 )
		self.draw_arrow( 1 , 0 , 0 )
		glColor3f( 0 , 1 , 0 )
		self.draw_arrow( 0 , 1 , 0 )
		glColor3f( 0 , 0 , 1 )
		self.draw_arrow( 0 , 0 , 1 )

	def draw_arrow( self , x , y , z ) :
		glBegin(GL_LINES)
		glVertex3f(0,0,0)
		glVertex3f(x,y,z)
		glEnd()

