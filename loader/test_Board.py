# para ejecutar: python -m unittest discover
import unittest
from Board import Board
from Postit import Postit

class TestPostit(unittest.TestCase):
	def testCreateEmptyBoard(self):
		# Given

		# When
		b = Board()

		# Then
		self.assertEqual(0, len(b.postits))
		self.assertEqual("", b.title)
		self.assertEqual("", b.background)
		self.assertEqual(800, b.sizeX)
		self.assertEqual(600, b.sizeY)
		
		
	def testCreateEmptyBoard(self):
		# Given
		l=[Postit("hola",1,2,3,4), Postit("chao",4,3,2,1)]
			
		# When
		b = Board(l, "titulo", "referencia imagen", 100, 200)

		# Then
		self.assertEqual(2, len(b.postits))
		self.assertEqual("titulo", b.title)
		self.assertEqual("referencia imagen", b.background)
		self.assertEqual(100, b.sizeX)
		self.assertEqual(200, b.sizeY)
		
	def testAddPostit(self):
		# Given
		l=[Postit("hola",1,2,3,4), Postit("chao",4,3,2,1)]
		p = Postit("nuevo",1,2,3,4)
		b = Board(l, "titulo", "referencia imagen", 100, 200)
		
		# When
		b.addPostit(p)

		# Then
		self.assertEqual(3, len(b.postits))
