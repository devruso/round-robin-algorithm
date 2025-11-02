import unittest

from src.round_robin import default_example, RoundRobinScheduler


class TestRoundRobin(unittest.TestCase):
    def test_example(self):
        processos = default_example()
        scheduler = RoundRobinScheduler(processos, quantum=2)
        ordem, respostas, media, _ = scheduler.simulate()

        expected_ordem = ["P1", "P2", "P3", "P1", "P2", "P3", "P1", "P3"]
        self.assertEqual(ordem, expected_ordem)

        expected_respostas = {"P1": 0, "P2": 1, "P3": 2}
        self.assertEqual(respostas, expected_respostas)

        self.assertAlmostEqual(media, 1.0)


if __name__ == '__main__':
    unittest.main()
