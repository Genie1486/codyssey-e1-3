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
        pattern: List[List[float]]
    ) -> MacResult:
        """
        두 필터와 패턴의 크기를 검증한 뒤, REPEAT_COUNT(10회) 반복 MAC 연산을 수행하여
        MacResult 객체를 반환한다.
        """
        is_valid_shape = self._is_valid_shape(filter_a, filter_b, pattern)

        if not is_valid_shape :
            return MacResult(judge_result= JudgeResult.SIZE_MISMATCH)

        start = time.perf_counter()
        
        for _ in range(REPEAT_COUNT):
            score_a = self._calculate_mac(filter_a, pattern)
            score_b = self._calculate_mac(filter_b, pattern)

        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000

        # REPEAT_COUNT는 0이 아님을 믿자...
        avg_time_ms = elapsed_ms / REPEAT_COUNT

        judge_result = self._judge_scores(score_a, score_b)

        return MacResult(score_a=score_a, score_b=score_b, avg_time_ms=avg_time_ms, judge_result=judge_result)

    def _is_valid_shape(
        self,
        filter_a: List[List[float]],
        filter_b: List[List[float]],
        pattern: List[List[float]]
    ) -> bool:
        """두 필터와 패턴이 모두 동일한 M×N 행렬인지 검증한다."""

        is_valid = False

        # 하나라도 빈 행렬이면 MAC 연산 불가하다고 판정
        if not filter_a or not filter_b or not pattern:
            return is_valid

        # 이제 빈 행렬은 없음
        if len(filter_a) != len(filter_b) or len(filter_b) != len(pattern) :
            return is_valid

        expected_cols = len(filter_a[0])

        for i in range(len(filter_a)):
            if len(filter_a[i]) != expected_cols or len(filter_b[i]) != expected_cols or len(pattern[i]) != expected_cols:
                return is_valid

        is_valid = True

        return is_valid

    def _calculate_mac(self, matrix_a: List[List[float]], matrix_b: List[List[float]]) -> float:
        """두 2차원 리스트의 같은 위치 원소를 곱하고 모두 누적하여 합계(float)를 반환한다."""
        
        total = 0.0

        row = len(matrix_a)
        col = len(matrix_a[0])

        for i in range(row) :
            for j in range(col) :
                total += matrix_a[i][j] * matrix_b[i][j]
        
        return total

    def _judge_scores(self, score_a: float, score_b: float) -> JudgeResult:
        """허용오차(EPSILON) 기준으로 두 점수를 비교하여 판정 결과(JudgeResult)를 반환한다."""

        if abs(score_a-score_b) < EPSILON:
            return JudgeResult.UNDECIDED

        if score_a > score_b : 
            return JudgeResult.FILTER_A

        if score_a < score_b : 
            return JudgeResult.FILTER_B