import unittest
from hw1_rx2119 import state

class MyTest(unittest.TestCase):
    def test_constructor(self):
        a = state(3)
        self.assertEqual(a.returnState(), [[0, 1, 2], [3, 4, 5], [6, 7, 8]])

    def test_moveDirect(self):
        a = state(3)
        current = a
        current = current.moveDirect("LEFT")
        self.assertEqual(current.returnState(), [[1, 0, 2], [3, 4, 5], [6, 7, 8]])
        current = current.moveDirect("LEFT")
        left = current
        self.assertEqual(current.returnState(), [[1, 2, 0], [3, 4, 5], [6, 7, 8]])
        current = current.moveDirect("LEFT")
        self.assertEqual(current, None)
        # moving to right from left most
        current = left.moveDirect("RIGHT")
        self.assertEqual(current.returnState(), [[1, 0, 2], [3, 4, 5], [6, 7, 8]])
        current = current.moveDirect("RIGHT")
        right = current
        self.assertEqual(current.returnState(), [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        current = current.moveDirect("RIGHT")
        self.assertEqual(current, None)
        # moving down
        current = right.moveDirect("DOWN")
        self.assertEqual(current.returnState(), [[3, 1, 2], [0, 4, 5], [6, 7, 8]])
        current = current.moveDirect("DOWN")
        down = current
        self.assertEqual(current.returnState(), [[3, 1, 2], [6, 4, 5], [0, 7, 8]])
        current = current.moveDirect("DOWN")
        self.assertEqual(current, None)
        # moving up
        current = down.moveDirect("UP")
        self.assertEqual(current.returnState(), [[3, 1, 2], [0, 4, 5], [6, 7, 8]])
        current = current.moveDirect("UP")
        self.assertEqual(current.returnState(), [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        current = current.moveDirect("UP")
        self.assertEqual(current, None)
        self.assertEqual(down.parent.parent.child.child, down)
        self.assertEqual(left.parent.parent.child.child.returnState(), left.returnState())

    def test_isGoalState(self):
        a = state(3)
        current = a
        self.assertEqual(current.isGoalState(), True)
        current = current.moveDirect("LEFT")
        self.assertEqual(current.isGoalState(), False)

    def test_shuffle(self):
        a = state(3)
        a.shuffle()
        self.assertEqual(a.isGoalState(), False)

if __name__ == "__main__":
    unittest.main(exit = False)