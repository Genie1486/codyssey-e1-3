from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from constants.constants import ErrorType, PatternLabel, TestStatus
from models.mac_result import MacResult

if TYPE_CHECKING:
    from models.pattern import Pattern


@dataclass
class CaseResult:
    """모드 2 개별 패턴 케이스의 분석 및 PASS/FAIL 검증 결과를 담는 DTO"""

    case_name: str
    status: TestStatus
    size: Optional[int] = None
    mac_result: Optional[MacResult] = None
    predicted_label: Optional[str] = None
    expected_label: Optional[str] = None
    fail_reason: Optional[str] = None

    @classmethod
    def fail(
        cls,
        pattern: "Pattern",
        reason: ErrorType,
        mac_result: Optional[MacResult] = None,
        predicted_label: Optional[str] = None,
    ) -> "CaseResult":
        """실패(FAIL) 상태의 CaseResult 인스턴스를 생성한다."""
        return cls(
            case_name=pattern.name,
            status=TestStatus.FAIL,
            size=pattern.size,
            mac_result=mac_result,
            predicted_label=predicted_label,
            expected_label=pattern.expected,
            fail_reason=reason.value,
        )

    @classmethod
    def success(
        cls,
        pattern: "Pattern",
        mac_result: MacResult,
        predicted_label: PatternLabel,
    ) -> "CaseResult":
        """성공(PASS) 상태의 CaseResult 인스턴스를 생성한다."""
        return cls(
            case_name=pattern.name,
            status=TestStatus.PASS,
            size=pattern.size,
            mac_result=mac_result,
            predicted_label=predicted_label.value,
            expected_label=pattern.expected,
        )
