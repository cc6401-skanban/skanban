import unittest
from parserimg import Parser

class TestParser(unittest.TestCase):
    def testParserNone(self):
        # Given
        p = Parser()
        # When            
        
        objects = p.parse(None)
        
        # Then
        self.assertEqual(0, len(objects))
        
    def testParserFindAtLeastOne(self):
        # Given
        p = Parser()
        # When            
        
        objects = p.parse("../image.jpg")
        
        # Then
        self.assertGreaterEqual(len(objects), 1)

    def testParserFindNone(self):
        # Given
        p = Parser()
        # When            
        
        objects = p.parse("../blanco.jpg")
        
        # Then
        self.assertEqual(len(objects), 0)

    def testParserFindNone(self):
        # Given
        p = Parser()
        # When            
        
        objects = p.parse("../blanco.jpg")
        
        # Then
        self.assertEqual(len(objects), 0)
        
    def testParserFindOne(self):
        # Given
        p = Parser()
        # When            
        
        objects = p.parse("../1postit.jpg")
        
        # Then
        self.assertEqual(len(objects), 1)
        
     #testear imagen en blanco
     #testear imagen con 1 solo postit
     #testear imagen invalida (un .doc)
     #testear imagen not found

"""
    def testPeekOnEmptyStack(self):
        # Given
        s = Stack()

        # When # Then
        self.assertRaises(EmptyStackException, s.peek)

    def testPushOnEmptyStack(self):
        # Given
        s = Stack()
        elem="hola"

        # When
        s.push(elem)

        # Then
        self.assertEqual(False,s.is_empty())
        self.assertEqual(elem,s.peek())

    def testPushPop(self):
        # Given
        s = Stack()
        elem = "hola"
        s.push(elem)

        # When
        received_elem = s.pop()

        # Then
        self.assertEqual(elem,received_elem)
        self.assertEqual(True, s.is_empty())

    def testPushPushPop(self):
        # Given
        s = Stack()     
        elem0 = "hola"   
        s.push(elem0)
        elem1 = "como"
        s.push(elem1)
        # When
        received_elem = s.pop()
       
        # Then
        self.assertEqual(elem1,received_elem)
        self.assertEqual(False, s.is_empty())
        self.assertEqual(elem0,s.peek())
        self.assertEqual(elem0,s.pop())

    def testPopOnEmptyStack(self):
        # Given
        s = Stack() 
        # When #Then
        self.assertRaises(EmptyStackException, s.pop)
        self.assertEqual(True, s.is_empty())
        
"""
	
