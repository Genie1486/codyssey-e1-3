from dataclasses import dataclass
from typing import Optional
from constants.constants import PatternLabel, TestStatus
from models.mac_result import MacResult


@dataclass
class CaseResult:
    """모드 2 개별 패턴 케이스의 분석 및 PASS/FAIL 검증 결과를 담는 DTO"""

    case_name: str
    status: TestStatus
    size: Optional[int] = None
    mac_result: Optional[MacResult] = None
    predicted_label: Optional[str] = None
    expected_label: Optional[PatternLabel] = None
    fail_reason: Optional[str] = None
