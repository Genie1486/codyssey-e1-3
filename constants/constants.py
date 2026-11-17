from enum import Enum

EPSILON: float = 1e-9          # 부동소수점 동점 판정 허용오차
REPEAT_COUNT: int = 10         # 성능 측정 반복 횟수
DEFAULT_USER_SIZE: int = 3     # 모드 1 기본 행렬 크기


class Mode(Enum):
    """프로그램 실행 모드"""
    USER_INPUT = (1, "사용자 입력 (3x3)")
    JSON_ANALYSIS = (2, "data.json 분석")


class MatrixType(Enum):
    """사용자 입력 시 행렬의 종류"""
    FILTER_A = "필터 A"
    FILTER_B = "필터 B"
    PATTERN = "패턴"


class JudgeResult(Enum):
    """MAC 연산 판정 결과 상태"""
    FILTER_A = "FILTER_A"       # 첫 번째 필터(A 또는 Cross) 우세
    FILTER_B = "FILTER_B"       # 두 번째 필터(B 또는 X) 우세
    UNDECIDED = "UNDECIDED"     # 허용오차 이내 동점
    SIZE_MISMATCH = "MISMATCH"  # 행렬 크기 불일치 오류
