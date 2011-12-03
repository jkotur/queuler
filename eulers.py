
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

import transformations as tr

from frame import Frame
from scene import Scene

class EulersScene( Scene ) :
	
	def __init__( self , maxt , fovy , ratio , near , far ) :
		Scene.__init__(self,fovy,ratio,near,far)

		self.maxt = maxt 

		self.frame = Frame()

		self.a = 0.0
		self.b = 0.0
		self.c = 0.0

		self.b = np.array((-5,0,0) , np.float64 )
		self.c = np.array(( 0,0,0) , np.float64 )
		self.e = np.array(( 5,0,0) , np.float64 )

		self.ab = np.array(( 0,0,0) , np.float64 )
		self.ac = self.ab
		self.ae = np.array((.5,.2,.1) , np.float64 )

	def set_matrix( self , mb , me ) :
		self.ab = np.array( tr.euler_from_matrix( mb ) , np.float64 )
		self.ae = np.array( tr.euler_from_matrix( me ) , np.float64 )

	def _step( self , t , dt ) :
		if t < self.maxt :
			self. c = (self. e-self. b) * t / self.maxt
			self.ac = (self.ae-self.ab) * t / self.maxt + self.ab

	def _draw_scene( self ) :
		glPushMatrix()
		glTranslatef( *self.b )
		glPushMatrix()
		glMultMatrixd( tr.euler_matrix( *self.ab ) )
		self.frame.draw()
		glPopMatrix()

		glTranslatef( *self.c )
		glMultMatrixd( tr.euler_matrix( *self.ac ) )
		self.frame.draw()
		glPopMatrix()

		glPushMatrix()
		glTranslatef( *self.e )
		glMultMatrixd( tr.euler_matrix( *self.ae ) )
		self.frame.draw()
		glPopMatrix()

	def mouse_move( self , df , buts ) :
		Scene.mouse_move( self , df , buts )
		if 1 in buts and buts[1] :
			self.ab = self.__modify_euler( self.ab , df )
		if 2 in buts and buts[2] :
			self.ae = self.__modify_euler( self.ae , df )

	def __modify_euler( self , a , d ) :
		glPushMatrix()
		glLoadMatrixf( tr.euler_matrix( *a ) )
		glRotatef( d[0] , 0 , 1 , 0 )
		glRotatef( d[1] , 1 , 0 , 0 )
		a = np.array( tr.euler_from_matrix( glGetDoublev(GL_MODELVIEW_MATRIX) ) )
		glPopMatrix()
		return a

