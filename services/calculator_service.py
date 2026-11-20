from typing import List
from constants.constants import EPSILON, REPEAT_COUNT, JudgeResult
from models.mac_result import MacResult

import time


class CalculatorService:
    """핵심 MAC 연산, 점수 판정 및 성능 측정을 담당하는 서비스 클래스"""

    def calculate_result(
        self,
        filter_a: List[List[float]],
        filter_b: List[List[float]],
        pattern: List[List[float]],
    ) -> MacResult:
        """
        두 필터와 패턴의 크기를 검증한 뒤, REPEAT_COUNT(10회) 반복 MAC 연산을 수행하여
        2D(기존) 및 1D(최적화) 성능 결과를 담은 MacResult 객체를 반환한다.
        """
        is_valid_shape = self._is_valid_shape(filter_a, filter_b, pattern)

        if not is_valid_shape:
            return MacResult(judge_result=JudgeResult.SIZE_MISMATCH)

        # 1. 기존 2차원 배열 MAC 연산 측정
        start_2d = time.perf_counter()
        for _ in range(REPEAT_COUNT):
            score_a = self._calculate_mac(filter_a, pattern)
            score_b = self._calculate_mac(filter_b, pattern)
        end_2d = time.perf_counter()

        avg_time_ms = ((end_2d - start_2d) * 1000) / REPEAT_COUNT

        # 2. 1차원 평탄화(Flatten) 후 MAC 연산 측정 (변환 시간 제외, 순수 접근 연산 비교)
        flat_filter_a = self._flatten(filter_a)
        flat_filter_b = self._flatten(filter_b)
        flat_pattern = self._flatten(pattern)

        start_1d = time.perf_counter()
        for _ in range(REPEAT_COUNT):
            _ = self._calculate_mac_1d(flat_filter_a, flat_pattern)
            _ = self._calculate_mac_1d(flat_filter_b, flat_pattern)
        end_1d = time.perf_counter()

        opt_avg_time_ms = ((end_1d - start_1d) * 1000) / REPEAT_COUNT

        judge_result = self._judge_scores(score_a, score_b)

        return MacResult(
            score_a=score_a,
            score_b=score_b,
            avg_time_ms=avg_time_ms,
            opt_avg_time_ms=opt_avg_time_ms,
            judge_result=judge_result,
        )

    @staticmethod
    def _flatten(matrix: List[List[float]]) -> List[float]:
        """2차원 행렬을 길이 N²의 1차원 리스트로 평탄화한다."""
        return [value for row in matrix for value in row]

    def _is_valid_shape(
        self,
        filter_a: List[List[float]],
        filter_b: List[List[float]],
        pattern: List[List[float]],
    ) -> bool:
        """두 필터와 패턴이 모두 동일한 M×N 행렬인지 검증한다."""
        if not filter_a or not filter_b or not pattern:
            return False

        if len(filter_a) != len(filter_b) or len(filter_b) != len(pattern):
            return False

        expected_cols = len(filter_a[0])

        for i in range(len(filter_a)):
            if (
                len(filter_a[i]) != expected_cols
                or len(filter_b[i]) != expected_cols
                or len(pattern[i]) != expected_cols
            ):
                return False

        return True

    def _calculate_mac(
        self, matrix_a: List[List[float]], matrix_b: List[List[float]]
    ) -> float:
        """두 2차원 리스트의 같은 위치 원소를 곱하고 모두 누적하여 합계(float)를 반환한다."""
        total = 0.0
        row = len(matrix_a)
        col = len(matrix_a[0])

        for i in range(row):
            for j in range(col):
                total += matrix_a[i][j] * matrix_b[i][j]

        return total

    def _calculate_mac_1d(self, flat_a: List[float], flat_b: List[float]) -> float:
        """1차원으로 평탄화된 두 리스트의 같은 인덱스 원소를 곱해 누적 합계(float)를 반환한다."""
        total = 0.0
        for i in range(len(flat_a)):
            total += flat_a[i] * flat_b[i]
        return total

    def _judge_scores(self, score_a: float, score_b: float) -> JudgeResult:
        """허용오차(EPSILON) 기준으로 두 점수를 비교하여 판정 결과(JudgeResult)를 반환한다."""
        if abs(score_a - score_b) < EPSILON:
            return JudgeResult.UNDECIDED

        if score_a > score_b:
            return JudgeResult.FILTER_A

        return JudgeResult.FILTER_B
