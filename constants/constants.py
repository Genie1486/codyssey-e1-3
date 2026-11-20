from enum import Enum
from typing import Dict

EPSILON: float = 1e-9  # 부동소수점 동점 판정 허용오차
REPEAT_COUNT: int = 10  # 성능 측정 반복 횟수
DEFAULT_USER_SIZE: int = 3  # 모드 1 기본 행렬 크기
DEFAULT_DATA_PATH: str = "data.json"  # 모드 2 기본 데이터 파일 경로

# 입력 허용 범위 및 패턴 생성기 설정 상수
MIN_CELL_VALUE: float = 0.0
MAX_CELL_VALUE: float = 1.0
PATTERN_SEED: int = 42  # 패턴 생성 재현성 고정 시드
NORMAL_PATTERN_RATIO: float = 0.8  # 정상 패턴 비율 (80%)
NOISE_MAX_VALUE: float = 0.2  # 정상 패턴 배경 노이즈 최댓값
SIGNAL_MIN_VALUE: float = 0.8  # 정상 패턴 신호 최솟값
PASSED_CASES_PATH: str = "passed_cases.json"  # 성공 케이스 저장 경로
FAILED_CASES_PATH: str = "failed_cases.json"  # 실패 케이스 저장 경로


class Mode(Enum):
    """프로그램 실행 모드"""

    USER_INPUT = (1, "사용자 입력 (3x3)")
    JSON_ANALYSIS = (2, "data.json 분석")
    PATTERN_GENERATION = (3, "패턴 생성 및 검증")
    EXIT = (4, "종료")


class MatrixType(Enum):
    """사용자 입력 시 행렬의 종류"""

    FILTER_A = "필터 A"
    FILTER_B = "필터 B"
    PATTERN = "패턴"


class JudgeResult(Enum):
    """MAC 연산 판정 결과 상태"""

    FILTER_A = "A"  # 첫 번째 필터(A 또는 Cross) 우세
    FILTER_B = "B"  # 두 번째 필터(B 또는 X) 우세
    UNDECIDED = "판정 불가 (|A-B| < 1e-9)"  # 허용오차 이내 동점
    SIZE_MISMATCH = "MISMATCH"  # 행렬 크기 불일치 오류


class PatternLabel(Enum):
    """모드 2 표준 패턴/필터 라벨"""

    CROSS = "Cross"
    X = "X"


# 외부 입력 키/기호를 표준 라벨(PatternLabel)로 변환하기 위한 정규화 매핑표
LABEL_ALIAS_MAP: Dict[str, PatternLabel] = {
    "cross": PatternLabel.CROSS,
    "+": PatternLabel.CROSS,
    "x": PatternLabel.X,
}


class TestStatus(Enum):
    """모드 2 테스트 케이스 검증 결과"""

    PASS = "PASS"
    FAIL = "FAIL"


class ErrorType(Enum):
    """모드 2 테스트 케이스 검증 실패 유형"""

    SCHEMA_ERROR = "스키마/형식 오류"
    FILTER_NOT_FOUND = "매칭 필터 없음"
    SIZE_MISMATCH = "행렬 크기 불일치"
    INVALID_VALUE = "비정상 수치 원소 포함"
    INVALID_LABEL = "유효하지 않은 라벨"
    UNDECIDED = "판정 불가 (동점)"
    PREDICTION_MISMATCH = "예측 불일치"


class SectionHeader(Enum):
    """콘솔 출력 섹션 헤더"""

    # 모드 1 헤더
    FILTER_INPUT = "# [1] 필터 입력"
    PATTERN_INPUT = "# [2] 패턴 입력"
    MAC_RESULT = "# [3] MAC 결과"
    MAC_RESULT_UNDECIDED = "# [3] MAC 결과 (판정 불가)"

    # 모드 2 헤더
    JSON_FILTER_LOAD = "# [1] 필터 로드"
    JSON_PATTERN_ANALYSIS = "# [2] 패턴 분석 (라벨 정규화 적용)"
    JSON_PERFORMANCE_ANALYSIS = f"# [3] 성능 분석 (평균/{REPEAT_COUNT}회)"
    JSON_RESULT_SUMMARY = "# [4] 결과 요약"

    # 모드 3 헤더
    GEN_PATTERN_CONFIG = "# [1] 패턴 생성 설정 및 실행"
    GEN_FILE_EXPORT = "# [5] 검증 결과 파일 저장"
