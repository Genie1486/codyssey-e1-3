from typing import Any, Dict, List, Optional

from constants.constants import (
    LABEL_ALIAS_MAP,
    ErrorType,
    JudgeResult,
    PatternLabel,
    TestStatus,
)
from models.case_result import CaseResult
from models.filter import Filter
from models.pattern import Pattern
from models.performance_result import PerformanceResult
from models.summary_result import SummaryResult
from repositories.json_repository import JsonRepository
from services.calculator_service import CalculatorService


class AnalysisService:
    """모드 2 JSON 데이터 파싱, 정규화, 검증 및 분석을 전담하는 서비스"""

    def __init__(
        self, calculator: CalculatorService, repository: JsonRepository
    ) -> None:
        self._calculator = calculator
        self._repository = repository
        self._raw_data: Optional[Dict[str, Any]] = None

    def _get_raw_data(self) -> Dict[str, Any]:
        """원본 JSON 데이터를 한 번만 로드하여 캐싱한다."""
        if self._raw_data is None:
            self._raw_data = self._repository.load_data()
        return self._raw_data

    @staticmethod
    def _extract_size_from_key(key: str) -> int:
        """'size_5' 또는 'size_5_1' 형태의 키에서 정수 크기 N을 추출한다."""
        parts = key.split("_")
        if len(parts) < 2 or parts[0] != "size":
            raise ValueError(f"{key}: {ErrorType.SCHEMA_ERROR.value}")
        try:
            size = int(parts[1])
        except ValueError as e:
            raise ValueError(f"{key}: {ErrorType.SCHEMA_ERROR.value}") from e

        if size <= 0:
            raise ValueError(f"{key}: {ErrorType.SCHEMA_ERROR.value}")
        return size

    def _normalize_label(self, label: Any) -> Optional[PatternLabel]:
        """외부 라벨 문자열을 표준 PatternLabel Enum으로 정규화한다."""
        if not isinstance(label, str):
            return None
        return LABEL_ALIAS_MAP.get(label.strip().lower())

    @staticmethod
    def _validate_matrix_shape(rows: int, cols: int, matrix: Any) -> bool:
        """행렬이 rows × cols 크기의 2차원 리스트인지 검증한다."""
        if not isinstance(matrix, list) or len(matrix) != rows:
            return False
        return all(isinstance(row, list) and len(row) == cols for row in matrix)

    def load_filters(self) -> Dict[int, Filter]:
        """JSON의 filters 항목을 파싱 및 검증하여 {크기: Filter} 딕셔너리로 반환한다."""
        raw_data = self._get_raw_data()
        raw_filters = raw_data.get("filters")
        if not isinstance(raw_filters, dict):
            raise ValueError(ErrorType.SCHEMA_ERROR.value)

        filters: Dict[int, Filter] = {}
        for size_key, filter_pair in raw_filters.items():
            if not isinstance(filter_pair, dict):
                raise ValueError(f"{size_key}: {ErrorType.SCHEMA_ERROR.value}")

            size = self._extract_size_from_key(size_key)
            cross_matrix = filter_pair.get("cross")
            x_matrix = filter_pair.get("x")

            if not (
                self._validate_matrix_shape(size, size, cross_matrix)
                and self._validate_matrix_shape(size, size, x_matrix)
            ):
                raise ValueError(f"{size_key}: {ErrorType.SIZE_MISMATCH.value}")

            filters[size] = Filter(size=size, filter_a=cross_matrix, filter_b=x_matrix)

        return filters

    def load_patterns(self) -> List[Pattern]:
        """JSON의 patterns 항목을 파싱하고 라벨을 정규화하여 Pattern 리스트로 반환한다."""
        raw_data = self._get_raw_data()
        raw_patterns = raw_data.get("patterns")
        if not isinstance(raw_patterns, dict):
            raise ValueError(ErrorType.SCHEMA_ERROR.value)

        patterns: List[Pattern] = []
        for case_name, case_data in raw_patterns.items():
            if not isinstance(case_data, dict):
                raise ValueError(f"{case_name}: {ErrorType.SCHEMA_ERROR.value}")

            size = self._extract_size_from_key(case_name)
            input_matrix = case_data.get("input")
            expected_label = self._normalize_label(case_data.get("expected"))

            if expected_label is None:
                raise ValueError(f"{case_name}: {ErrorType.INVALID_LABEL.value}")

            patterns.append(
                Pattern(
                    name=case_name,
                    size=size,
                    input_matrix=input_matrix,
                    expected=expected_label,
                )
            )

        return patterns

    def analyze_patterns(
        self, patterns: List[Pattern], filters: Dict[int, Filter]
    ) -> List[CaseResult]:
        """모든 패턴 케이스를 순회하며 개별 분석 결과를 수집한다."""
        return [self._analyze_single_pattern(p, filters) for p in patterns]

    def _analyze_single_pattern(
        self, pattern: Pattern, filters: Dict[int, Filter]
    ) -> CaseResult:
        """단일 패턴 케이스의 크기 검증, MAC 연산 및 PASS/FAIL 판정을 수행한다."""
        target_filter = filters.get(pattern.size)
        if target_filter is None:
            return CaseResult.fail(pattern, ErrorType.FILTER_NOT_FOUND)

        if not self._validate_matrix_shape(
            pattern.size, pattern.size, pattern.input_matrix
        ):
            return CaseResult.fail(pattern, ErrorType.SIZE_MISMATCH)

        mac_result = self._calculator.calculate_result(
            target_filter.filter_a, target_filter.filter_b, pattern.input_matrix
        )

        if mac_result.judge_result == JudgeResult.UNDECIDED:
            return CaseResult.fail(
                pattern,
                ErrorType.UNDECIDED,
                mac_result=mac_result,
                predicted_label="UNDECIDED",
            )

        predicted_label = self._map_judge_to_label(mac_result.judge_result)
        if predicted_label is None or predicted_label != pattern.expected:
            return CaseResult.fail(
                pattern,
                ErrorType.PREDICTION_MISMATCH,
                mac_result=mac_result,
                predicted_label=predicted_label.value if predicted_label else None,
            )

        return CaseResult.success(pattern, mac_result, predicted_label)

    @staticmethod
    def _map_judge_to_label(judge: JudgeResult) -> Optional[PatternLabel]:
        """CalculatorService의 JudgeResult를 표준 PatternLabel로 변환한다."""
        if judge == JudgeResult.FILTER_A:
            return PatternLabel.CROSS
        if judge == JudgeResult.FILTER_B:
            return PatternLabel.X
        return None

    def measure_performance(
        self, case_results: List[CaseResult]
    ) -> List[PerformanceResult]:
        """분석 완료된 케이스 결과들을 크기별로 집계하여 평균 연산 시간을 계산한다."""
        time_sums: Dict[int, float] = {}
        counts: Dict[int, int] = {}

        for case_result in case_results:
            if (
                case_result.size is None
                or case_result.mac_result is None
                or case_result.mac_result.avg_time_ms is None
            ):
                continue

            size = case_result.size
            time_sums[size] = (
                time_sums.get(size, 0.0) + case_result.mac_result.avg_time_ms
            )
            counts[size] = counts.get(size, 0) + 1

        # 3×3처럼 JSON 패턴에 없던 기본 측정 대상 크기 보완 (필요 시)
        if 3 not in time_sums:
            default_filter = Filter.create_default_filters(3)
            dummy_input = [[1.0] * 3 for _ in range(3)]
            mac_res = self._calculator.calculate_result(
                default_filter.filter_a, default_filter.filter_b, dummy_input
            )
            time_sums[3] = mac_res.avg_time_ms
            counts[3] = 1

        results = [
            PerformanceResult(
                size=size,
                avg_time_ms=time_sums[size] / counts[size],
                operation_count=size**2,
            )
            for size in sorted(time_sums.keys())
        ]
        return results

    def summarize_result(self, case_results: List[CaseResult]) -> SummaryResult:
        """개별 분석 결과 리스트를 집계하여 전체 요약 정보를 생성한다."""
        pass_count = 0
        fail_cases: List[CaseResult] = []

        for case_result in case_results:
            if case_result.status == TestStatus.PASS:
                pass_count += 1
            else:
                fail_cases.append(case_result)

        return SummaryResult(
            total_count=len(case_results),
            pass_count=pass_count,
            fail_count=len(fail_cases),
            fail_cases=fail_cases,
        )
