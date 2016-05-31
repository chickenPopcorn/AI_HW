import unittest
from hw1_rx2119 import state

class MyTest(unittest.TestCase):
	def test_constructor(self):
		a = state(3)
		self.assertEqual(a.returnState(), [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
		
	def test_move(self):
		a = state(3)
		a.move("LEFT")
		self.assertEqual(a.returnState(), [[1, 0, 2], [3, 4, 5], [6, 7, 8]])
		a.move("LEFT")
		self.assertEqual(a.returnState(), [[1, 2, 0], [3, 4, 5], [6, 7, 8]])	
		a.move("LEFT")
		self.assertEqual(a.returnState(), [[1, 2, 0], [3, 4, 5], [6, 7, 8]])	
		
		a.move("RIGHT")
		self.assertEqual(a.returnState(), [[1, 0, 2], [3, 4, 5], [6, 7, 8]])	
		a.move("RIGHT")
		self.assertEqual(a.returnState(), [[0, 1, 2], [3, 4, 5], [6, 7, 8]])	
		a.move("RIGHT")
		self.assertEqual(a.returnState(), [[0, 1, 2], [3, 4, 5], [6, 7, 8]])	
		
		a.move("DOWN")
		self.assertEqual(a.returnState(), [[3, 1, 2], [0, 4, 5], [6, 7, 8]])
		a.move("DOWN")
		self.assertEqual(a.returnState(), [[3, 1, 2], [6, 4, 5], [0, 7, 8]])
		a.move("DOWN")
		self.assertEqual(a.returnState(), [[3, 1, 2], [6, 4, 5], [0, 7, 8]])
		
		a.move("UP")
		self.assertEqual(a.returnState(), [[3, 1, 2], [0, 4, 5], [6, 7, 8]])
		a.move("UP")
		self.assertEqual(a.returnState(), [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
		a.move("UP")
		self.assertEqual(a.returnState(), [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
		
		a.parent.parent.child.child.returnState()
		self.assertEqual(a.parent.parent.child.child, a)
		self.assertEqual(a.parent.parent.child.child.returnState(), a.returnState())
		
		
		
if __name__ == "__main__":
	unittest.main(exit = False)