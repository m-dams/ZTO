from abc import ABC, abstractmethod
import time


class StopCondition(ABC):
    def __init__(self):
        self._is_improvement = False
        self._iters_since_improvement = 0

    @abstractmethod
    def should_stop(self) -> bool:
        raise NotImplemented

    def set_improvement(self, improvement: bool):
        self._is_improvement = improvement
        if not improvement:
            self._iters_since_improvement += 1
        else:
            self._iters_since_improvement = 0


class IterationCondition(StopCondition):
    def __init__(self, n_iter: int):
        super().__init__()
        self.n_iter = n_iter

    def should_stop(self) -> bool:
        self.n_iter -= 1

        return self.n_iter < 0


class SinceLastImprovementCondition(StopCondition):
    def __init__(self, n_iter: int):
        super().__init__()
        self.n_iter = n_iter

    def should_stop(self) -> bool:
        return self._iters_since_improvement == self.n_iter


class CalcTimeCondition(StopCondition):
    def __init__(self, seconds: int):
        super().__init__()
        self.seconds = seconds
        self.__start = time.time()
        self.__end = 0

    def should_stop(self) -> bool:
        self.__end = time.time()
        elapsed = self.__end - self.__start

        return elapsed >= self.seconds

    def how_long(self) -> float:
        return self.__end - self.__start

