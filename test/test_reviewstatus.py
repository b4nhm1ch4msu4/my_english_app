import unittest
from datetime import date, timedelta

from app.sm_2_algo import Quality, SM2Algorithm
from app.models import ReviewStatus


class TestReviewStatus(unittest.TestCase):

    def test_initial_state(self):
        status = ReviewStatus(
            repetitions=0,
            ease_factor=2.5,
            interval=0,
            next_review=date(2026, 8, 18),
        )

        self.assertEqual(status.repetitions, 0)
        self.assertEqual(status.ease_factor, 2.5)
        self.assertEqual(status.interval, 0)
        self.assertEqual(status.next_review, date(2026, 8, 18))

    def test_good_first_review(self):
        status = ReviewStatus(
            repetitions=0,
            ease_factor=2.5,
            interval=0,
            next_review=date(2026, 8, 18),
        )

        status.update(Quality.Good)

        # inherited sm2_algo state
        self.assertEqual(status.repetitions, 1)
        self.assertEqual(status.interval, 1)
        self.assertAlmostEqual(status.ease_factor, 2.5)

        # ReviewStatus state
        self.assertEqual(
            status.next_review,
            date(2026, 8, 19),
        )

    def test_good_second_review(self):
        status = ReviewStatus(
            repetitions=1,
            ease_factor=2.5,
            interval=1,
            next_review=date(2026, 8, 18),
        )

        status.update(Quality.Good)

        self.assertEqual(status.repetitions, 2)
        self.assertEqual(status.interval, 3)
        self.assertAlmostEqual(status.ease_factor, 2.5)

        self.assertEqual(
            status.next_review,
            date(2026, 8, 21),
        )

    def test_good_later_review(self):
        status = ReviewStatus(
            repetitions=2,
            ease_factor=2.5,
            interval=3,
            next_review=date(2026, 8, 18),
        )

        status.update(Quality.Good)

        self.assertEqual(status.repetitions, 3)
        self.assertEqual(status.interval, 7)
        self.assertAlmostEqual(status.ease_factor, 2.5)

        self.assertEqual(
            status.next_review,
            date(2026, 8, 25),
        )

    def test_easy_review(self):
        status = ReviewStatus(
            repetitions=2,
            ease_factor=2.5,
            interval=3,
            next_review=date(2026, 8, 18),
        )

        status.update(Quality.Easy)

        self.assertEqual(status.repetitions, 3)
        self.assertEqual(status.interval, 7)
        self.assertAlmostEqual(status.ease_factor, 2.6)

        self.assertEqual(
            status.next_review,
            date(2026, 8, 25),
        )

    def test_again_resets_review(self):
        status = ReviewStatus(
            repetitions=5,
            ease_factor=2.5,
            interval=20,
            next_review=date(2026, 8, 18),
        )

        status.update(Quality.Again)

        self.assertEqual(status.repetitions, 0)
        self.assertEqual(status.interval, 1)
        self.assertAlmostEqual(status.ease_factor, 2.5)

        # next_review moves by the new interval
        self.assertEqual(
            status.next_review,
            date(2026, 8, 19),
        )

    def test_hard_resets_review(self):
        status = ReviewStatus(
            repetitions=5,
            ease_factor=2.5,
            interval=20,
            next_review=date(2026, 8, 18),
        )

        status.update(Quality.Hard)

        self.assertEqual(status.repetitions, 0)
        self.assertEqual(status.interval, 1)
        self.assertAlmostEqual(status.ease_factor, 2.5)

        self.assertEqual(
            status.next_review,
            date(2026, 8, 19),
        )

    def test_multiple_reviews(self):
        status = ReviewStatus(
            repetitions=0,
            ease_factor=2.5,
            interval=0,
            next_review=date(2026, 8, 18),
        )

        # Good: interval = 1
        status.update(Quality.Good)

        self.assertEqual(status.interval, 1)
        self.assertEqual(status.next_review, date(2026, 8, 19))

        # Good: interval = 3
        status.update(Quality.Good)

        self.assertEqual(status.interval, 3)
        self.assertEqual(status.next_review, date(2026, 8, 22))

        # Good: interval = 7
        status.update(Quality.Good)

        self.assertEqual(status.interval, 7)
        self.assertEqual(status.next_review, date(2026, 8, 29))


if __name__ == "__main__":
    unittest.main()
