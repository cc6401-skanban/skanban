import unittest
from Postit import Postit

class TestPostit(unittest.TestCase):
	def testCreatePostit(self):
		# Given

		# When
		p = Postit()

		# Then
		self.assertEqual("", p.path)
		self.assertEqual(0, p.posX)
		self.assertEqual(0, p.posY)
		self.assertEqual(0, p.sizeX)
		self.assertEqual(0, p.sizeY)

		
