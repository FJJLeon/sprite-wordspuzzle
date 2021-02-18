import unittest
from puzzle_solver import PuzzleSolver


class TestPuzzleSolver(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        SPRITE_DATA_URL = "SpriteData.json"
        cls.ANSWER_URL = "answer.txt"
        cls.solver = PuzzleSolver(SPRITE_DATA_URL)

    def __generate_testcases(self):
        testcases = []
        with open(self.ANSWER_URL, mode='r') as load_file:
            lines = load_file.readlines()
            i = 0
            while i < len(lines):
                testcases.append((lines[i+1], lines[i+4][5:-1]))
                i += 5
        return testcases

    def test_solve(self):
        testcases = self.__generate_testcases()
        for puzzle, expected_ans in testcases:
            with self.subTest(puzzle=puzzle):
                actual_ans = self.solver.solve(puzzle)
                # print(puzzle, expected_ans, actual_ans)
                self.assertTrue(len(actual_ans) > 0)
                if len(actual_ans) == 1:
                    self.assertEqual(expected_ans, actual_ans[0])
                else:
                    expected = expected_ans.split(';')
                    self.assertEqual(set(expected), set(actual_ans))


if __name__ == '__main__':
    unittest.main()
