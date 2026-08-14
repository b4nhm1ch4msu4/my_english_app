from enum import Enum


class Quality(Enum):
    Again = 0
    Hard = 1
    Good = 2
    Easy = 3


class sm2_algo:
    def __init__(self, rep: int, ease_factor: float, interval: int) -> None:
        self.repetitions = rep
        self.ease_factor = ease_factor
        self.interval = interval

    def update(self, q: Quality):
        upper_limit = Quality.Easy.value
        if not 0 <= q.value <= upper_limit:
            raise ValueError(f"quality must be between 0 and {upper_limit}")

        # review fail
        if q.value < 2:
            self.repetitions = 0
            self.interval = 1
            self.ease_factor = self.ease_factor

        # review successful
        else:

            # update interval
            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease_factor)

            # update repetitions
            self.repetitions += 1

            # update ease_factor
            new_ease_factor = (
                self.ease_factor
                + 0.1
                - (upper_limit - q.value)
                * (0.075 + (upper_limit - q.value) * 0.025)
            )
            if new_ease_factor < 1.3:
                self.ease_factor = 1.3
