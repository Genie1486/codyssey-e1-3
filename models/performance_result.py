from dataclasses import dataclass


@dataclass
class PerformanceResult:
    """크기별 패턴 분석 평균 소요 시간 및 연산 횟수를 담는 DTO"""

    size: int
    avg_time_ms: float
    opt_avg_time_ms: float
    operation_count: int

    @property
    def improvement_rate(self) -> float:
        """2D 대비 1D 평탄화 연산의 시간 단축률(%)을 반환한다."""
        if self.avg_time_ms <= 0:
            return 0.0
        return ((self.avg_time_ms - self.opt_avg_time_ms) / self.avg_time_ms) * 100
