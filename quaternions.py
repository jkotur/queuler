
from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

import transformations as tr

from frame import Frame
from scene import Scene

class QuaternionsScene( Scene ) :
	
	def __init__( self , maxt , fovy , ratio , near , far ) :
		Scene.__init__(self,fovy,ratio,near,far)

		self.maxt = maxt

		self.frame = Frame()

		self.b = np.array((-5,0,0) , np.float64 )
		self.c = np.array(( 0,0,0) , np.float64 )
		self.e = np.array(( 5,0,0) , np.float64 )

		self.qb = tr.random_quaternion()
		self.qc = self.qb
		self.qe = tr.random_quaternion()

	def set_matrix( self , mb , me ) :
		self.qb = tr.quaternion_from_matrix( mb )
		self.qe = tr.quaternion_from_matrix( me )

	def _step( self , t , dt ) :
		if t <= self.maxt :
			self.c  = (self. e-self. b) * t / self.maxt
			self.qc = tr.quaternion_slerp( self.qb, self.qe, t/self.maxt )

	def _draw_scene( self ) :
		glPushMatrix()
		glTranslatef( *self.b )
		glPushMatrix()
		glMultMatrixd( tr.quaternion_matrix( self.qb ) )
		self.frame.draw()
		glPopMatrix()

		glTranslatef( *self.c )
		glMultMatrixd( tr.quaternion_matrix( self.qc ) )
		self.frame.draw()
		glPopMatrix()

		glPushMatrix()
		glTranslatef( *self.e )
		glMultMatrixd( tr.quaternion_matrix( self.qe ) )
		self.frame.draw()
		glPopMatrix()

	def mouse_move( self , df , buts ) :
		Scene.mouse_move( self , df , buts )
		if 1 in buts and buts[1] :
			self.qb = self.__modify_quaternion( self.qb , df )
		if 2 in buts and buts[2] :
			self.qe = self.__modify_quaternion( self.qe , df )

	def __modify_quaternion( self , q , d ) :
		glPushMatrix()
		glLoadMatrixf( tr.quaternion_matrix( q ) )
		glRotatef( d[0] , 0 , 1 , 0 )
		glRotatef( d[1] , 1 , 0 , 0 )
		q = tr.quaternion_from_matrix( glGetDoublev(GL_MODELVIEW_MATRIX) )
		glPopMatrix()
		return q

	def get_beg_matrix( self ) :
		return tr.quaternion_matrix(self.qb)

	def get_end_matrix( self ) :
		return tr.quaternion_matrix(self.qe)

