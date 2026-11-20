from dataclasses import dataclass
from typing import Any, List, Optional
from constants.constants import PatternLabel, TestStatus
from models.mac_result import MacResult


from dataclasses import dataclass
from typing import List
from constants.constants import PatternLabel


@dataclass
class Pattern:
    """모드 2 테스트 패턴 데이터와 정규화된 기대 라벨을 담는 DTO"""

    name: str
    size: int
    input_matrix: List[List[float]]
    expected: PatternLabel
    raw_expected: Optional[Any] = None
