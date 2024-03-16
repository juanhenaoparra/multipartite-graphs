import unittest.mock
from app.services.gen_graph import GenerateGraph
from app.schemas.generation import GenGraphInput

class TestGraphGeneration(unittest.TestCase):
    def test_generate_graph_complete(self):
        inp = GenGraphInput(nodesNumber=5, connected=False, complete=True, weighted=True)
        adjacencyList = GenerateGraph(inp)

        for key, value in adjacencyList.items():
            self.assertEqual(len(value), 4) # We expect 4 neighbors for each node because self-loops are not allowed
            for neighbor in value:
                self.assertEqual(neighbor.parentId, key)
                self.assertNotEqual(neighbor.weight, None)

        self.assertEqual(len(adjacencyList), 5)

    def test_generate_graph_connected(self):
        expectedDegree = 2
        inp = GenGraphInput(nodesNumber=5, connected=True,probability=0.5, degree=expectedDegree, weighted=True)
        adjacencyList = GenerateGraph(inp)

        for key, value in adjacencyList.items():
            self.assertEqual(len(value), expectedDegree)
            for neighbor in value:
                self.assertEqual(neighbor.parentId, key)
                self.assertNotEqual(neighbor.weight, None)

        self.assertEqual(len(adjacencyList), 5)

if __name__ == '__main__':
    unittest.main()