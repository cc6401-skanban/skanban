# para ejecutar: python -m unittest discover
import unittest
from Postit import Postit

class TestPostit(unittest.TestCase):
	def testCreateEmptyPostit(self):
		# Given

		# When
		p = Postit()

		# Then
		self.assertEqual("", p.path)
		self.assertEqual(0, p.posX)
		self.assertEqual(0, p.posY)
		self.assertEqual(0, p.sizeX)
		self.assertEqual(0, p.sizeY)

	def testCreateDataPostit(self):
		# Given

		# When
		p = Postit("hola",1,2,3,4)

		# Then
		self.assertEqual("hola", p.path)
		self.assertEqual(1, p.posX)
		self.assertEqual(2, p.posY)
		self.assertEqual(3, p.sizeX)
		self.assertEqual(4, p.sizeY)
		
	def testMoveTo(self):
		# Given
		p = Postit("hola",1,2,3,4)
		
		# When
		p.moveTo(10,100)

		# Then
		self.assertEqual("hola", p.path)
		self.assertEqual(10, p.posX)
		self.assertEqual(100, p.posY)
		self.assertEqual(3, p.sizeX)
		self.assertEqual(4, p.sizeY)
		
		
	def testgetPosition(self):
		# Given
		p = Postit("hola",1,2,3,4)
		
		# When
		pos = p.getPosition()
		
		# Then
		self.assertEqual(1, pos[0])
		self.assertEqual(2, pos[1])
		
		

