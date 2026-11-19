from dataclasses import dataclass


@dataclass
class PerformanceResult:
    """크기별 패턴 분석 평균 소요 시간 및 연산 횟수를 담는 DTO"""

    size: int
    avg_time_ms: float
    operation_count: int
