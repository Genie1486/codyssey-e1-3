from dataclasses import dataclass
from typing import List
from models.case_result import CaseResult


@dataclass
class SummaryResult:
    """모드 2 전체 패턴 검증 결과 요약을 담는 DTO"""

    total_count: int
    pass_count: int
    fail_count: int
    fail_cases: List[CaseResult]
