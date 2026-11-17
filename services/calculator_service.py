from typing import List
from constants.constants import EPSILON, REPEAT_COUNT, JudgeResult
from models.mac_result import MacResult


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
        pass

    def _is_valid_shape(
        self,
        filter_a: List[List[float]],
        filter_b: List[List[float]],
        pattern: List[List[float]]
    ) -> bool:
        """두 필터와 패턴이 모두 동일한 N×N 정사각 행렬인지 검증한다."""
        pass

    def _calculate_mac(self, matrix_a: List[List[float]], matrix_b: List[List[float]]) -> float:
        """두 2차원 리스트의 같은 위치 원소를 곱하고 모두 누적하여 합계(float)를 반환한다."""
        pass

    def _judge_scores(self, score_a: float, score_b: float) -> JudgeResult:
        """허용오차(EPSILON) 기준으로 두 점수를 비교하여 판정 결과(JudgeResult)를 반환한다."""
        pass
