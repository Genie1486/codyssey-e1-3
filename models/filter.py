from typing import List


class Filter:
    """N×N 크기의 Cross(filter_a) 및 X(filter_b) 필터 쌍을 보관하는 모델 클래스"""

    DEFAULT_WEIGHT: float = 1.0

    def __init__(
        self, size: int, filter_a: List[List[float]], filter_b: List[List[float]]
    ) -> None:
        self.size = size
        self.filter_a = filter_a
        self.filter_b = filter_b

    @classmethod
    def create_default_filters(cls, size: int) -> "Filter":
        """홀수 크기 N을 받아 기본 N×N Cross 및 X 필터 쌍 객체를 생성한다."""
        if size <= 0 or size % 2 == 0:
            raise ValueError("필터 크기는 양의 홀수여야 합니다.")

        filter_a = cls._create_default_cross(size)
        filter_b = cls._create_default_x(size)
        return cls(size, filter_a, filter_b)

    @classmethod
    def _create_default_cross(cls, size: int) -> List[List[float]]:
        result: List[List[float]] = []
        center = size // 2

        for i in range(size):
            row: List[float] = []
            for j in range(size):
                if i == center or j == center:
                    row.append(cls.DEFAULT_WEIGHT)
                else:
                    row.append(0.0)
            result.append(row)

        return result

    @classmethod
    def _create_default_x(cls, size: int) -> List[List[float]]:
        result: List[List[float]] = []

        for i in range(size):
            row: List[float] = []
            for j in range(size):
                if i == j or i + j == size - 1:
                    row.append(cls.DEFAULT_WEIGHT)
                else:
                    row.append(0.0)
            result.append(row)

        return result
