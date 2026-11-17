from dataclasses import dataclass
from typing import Optional
from constants.constants import JudgeResult


@dataclass
class MacResult:
    """MAC 연산 및 판정 결과를 담는 데이터 전달 객체"""
    score_a: Optional[float]
    score_b: Optional[float]
    avg_time_ms: Optional[float]
    judge_result: JudgeResult
    fail_reason: Optional[str] = None
