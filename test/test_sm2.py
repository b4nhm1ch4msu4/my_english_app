import unittest

from app.sm_2_algo import Quality, SM2Algorithm


class TestSM2Algo(unittest.TestCase):

    def test_initial_state(self):
        sm2 = SM2Algorithm(
            repetitions=0,
            ease_factor=2.5,
            interval=0,
        )

        self.assertEqual(sm2.repetitions, 0)
        self.assertEqual(sm2.ease_factor, 2.5)
        self.assertEqual(sm2.interval, 0)

    # --------------------------------------------------
    # Failed review
    # --------------------------------------------------

    def test_again(self):
        sm2 = SM2Algorithm(
            repetitions=5,
            ease_factor=2.6,
            interval=20,
        )

        sm2.update(Quality.Again)

        self.assertEqual(sm2.repetitions, 0)
        self.assertEqual(sm2.interval, 1)
        self.assertEqual(sm2.ease_factor, 2.6)

    def test_hard(self):
        sm2 = SM2Algorithm(
            repetitions=5,
            ease_factor=2.7,
            interval=20,
        )

        sm2.update(Quality.Hard)

        self.assertEqual(sm2.repetitions, 0)
        self.assertEqual(sm2.interval, 1)
        self.assertEqual(sm2.ease_factor, 2.7)

    # --------------------------------------------------
    # Successful review
    # --------------------------------------------------

    def test_good_first_review(self):
        sm2 = SM2Algorithm(
            repetitions=0,
            ease_factor=2.5,
            interval=0,
        )

        sm2.update(Quality.Good)

        self.assertEqual(sm2.repetitions, 1)
        self.assertEqual(sm2.interval, 1)
        self.assertAlmostEqual(sm2.ease_factor, 2.5)

    def test_good_second_review(self):
        sm2 = SM2Algorithm(
            repetitions=1,
            ease_factor=2.5,
            interval=1,
        )

        sm2.update(Quality.Good)

        self.assertEqual(sm2.repetitions, 2)
        self.assertEqual(sm2.interval, 3)
        self.assertAlmostEqual(sm2.ease_factor, 2.5)

    def test_good_later_review(self):
        sm2 = SM2Algorithm(
            repetitions=2,
            ease_factor=2.5,
            interval=3,
        )

        sm2.update(Quality.Good)

        self.assertEqual(sm2.repetitions, 3)
        self.assertEqual(sm2.interval, 7)
        self.assertAlmostEqual(sm2.ease_factor, 2.5)

    def test_easy_increases_ease_factor(self):
        sm2 = SM2Algorithm(
            repetitions=2,
            ease_factor=2.5,
            interval=6,
        )

        sm2.update(Quality.Easy)

        self.assertEqual(sm2.repetitions, 3)
        self.assertEqual(sm2.interval, 15)
        self.assertAlmostEqual(sm2.ease_factor, 2.6)

    # --------------------------------------------------
    # Ease factor lower limit
    # --------------------------------------------------

    def test_ease_factor_cannot_go_below_1_3(self):
        sm2 = SM2Algorithm(
            repetitions=2,
            ease_factor=1.3,
            interval=6,
        )

        sm2.update(Quality.Good)

        self.assertGreaterEqual(sm2.ease_factor, 1.3)
        self.assertAlmostEqual(sm2.ease_factor, 1.3)

    # --------------------------------------------------
    # Multiple reviews
    # --------------------------------------------------

    def test_multiple_reviews(self):
        sm2 = SM2Algorithm(
            repetitions=0,
            ease_factor=2.5,
            interval=0,
        )

        # First successful review
        sm2.update(Quality.Good)

        self.assertEqual(sm2.repetitions, 1)
        self.assertEqual(sm2.interval, 1)

        # Second successful review
        sm2.update(Quality.Good)

        self.assertEqual(sm2.repetitions, 2)
        self.assertEqual(sm2.interval, 3)

        # Third successful review
        sm2.update(Quality.Good)

        self.assertEqual(sm2.repetitions, 3)
        self.assertEqual(sm2.interval, 7)

    # --------------------------------------------------
    # Reset after failure
    # --------------------------------------------------

    def test_failure_resets_repetitions(self):
        sm2 = SM2Algorithm(
            repetitions=5,
            ease_factor=2.5,
            interval=20,
        )

        sm2.update(Quality.Again)

        self.assertEqual(sm2.repetitions, 0)
        self.assertEqual(sm2.interval, 1)

        # Next successful review starts again
        sm2.update(Quality.Good)

        self.assertEqual(sm2.repetitions, 1)
        self.assertEqual(sm2.interval, 1)


if __name__ == "__main__":
    unittest.main()
