from dataclasses import dataclass
from typing import Optional
from constants.constants import JudgeResult


@dataclass
class MacResult:
    """MAC 연산 및 판정 결과를 담는 데이터 전달 객체"""

    score_a: Optional[float] = None
    score_b: Optional[float] = None
    avg_time_ms: Optional[float] = None
    opt_avg_time_ms: Optional[float] = None
    judge_result: JudgeResult = JudgeResult.UNDECIDED
    fail_reason: Optional[str] = None
