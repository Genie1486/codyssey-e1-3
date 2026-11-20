import random
from enum import Enum
from typing import Any, List

from constants.constants import (
    MAX_CELL_VALUE,
    NOISE_MAX_VALUE,
    NORMAL_PATTERN_RATIO,
    PATTERN_SEED,
    SIGNAL_MIN_VALUE,
    PatternLabel,
)
from models.pattern import Pattern


class AnomalyType(Enum):
    """패턴 생성기가 주입하는 비정상 결함 5종"""

    ROW_MISMATCH = "ROW_MISMATCH"
    COL_MISMATCH = "COL_MISMATCH"
    SIZE_MISMATCH = "SIZE_MISMATCH"
    INVALID_VALUE = "INVALID_VALUE"
    INVALID_LABEL = "INVALID_LABEL"


class PatternGenerator:
    """재현 가능한 시드 기반으로 정상(80%) 및 비정상(20%) 테스트 패턴을 생성하는 서비스"""

    INVALID_LABELS: List[str] = ["Criss", "Plus", "XX", "UNKNOWN", ""]

    def __init__(self, seed: int = PATTERN_SEED) -> None:
        self._seed = seed

    @property
    def seed(self) -> int:
        return self._seed

    def generate_patterns(self, size: int, count: int) -> List[Pattern]:
        """N×N(양의 홀수) 크기 패턴 count개를 정상 80% / 비정상 20% 비율로 생성한다."""
        if size <= 0 or size % 2 == 0:
            raise ValueError("패턴 크기는 양의 홀수여야 합니다.")
        if count <= 0:
            raise ValueError("생성할 패턴 개수는 1 이상의 정수여야 합니다.")

        rng = random.Random(self._seed)
        patterns: List[Pattern] = []

        normal_count = round(count * NORMAL_PATTERN_RATIO)
        anomaly_count = count - normal_count

        # 정상 케이스(True)와 비정상 케이스(False) 순서를 시드 기반으로 섞음
        flags = [True] * normal_count + [False] * anomaly_count
        rng.shuffle(flags)

        for idx, is_normal in enumerate(flags, start=1):
            case_name = f"gen_size_{size}_{idx}"
            if is_normal:
                patterns.append(self._create_normal_pattern(rng, case_name, size))
            else:
                patterns.append(self._create_anomaly_pattern(rng, case_name, size))

        return patterns

    def _create_normal_pattern(
        self, rng: random.Random, case_name: str, size: int
    ) -> Pattern:
        """배경 노이즈(0.0~0.2)와 신호(0.8~1.0)를 가진 정상 Cross 또는 X 패턴을 생성한다."""
        label = rng.choice([PatternLabel.CROSS, PatternLabel.X])
        matrix = self._build_signal_matrix(rng, size, label)
        return Pattern(
            name=case_name,
            size=size,
            input_matrix=matrix,
            expected=label,
            raw_expected=label.value,
        )

    def _create_anomaly_pattern(
        self, rng: random.Random, case_name: str, size: int
    ) -> Pattern:
        """5종의 비정상 결함 중 하나를 무작위로 주입한 패턴을 생성한다."""
        anomaly = rng.choice(list(AnomalyType))
        label = rng.choice([PatternLabel.CROSS, PatternLabel.X])
        matrix = self._build_signal_matrix(rng, size, label)

        if anomaly == AnomalyType.ROW_MISMATCH:
            # 행 개수 축소 (N-1행, N=1일 경우 빈 행렬)
            broken_matrix = matrix[:-1] if size > 1 else []
            return Pattern(
                name=case_name,
                size=size,
                input_matrix=broken_matrix,
                expected=label,
                raw_expected=label.value,
            )

        if anomaly == AnomalyType.COL_MISMATCH:
            # 특정 행의 열 개수 축소 (Ragged 행렬)
            target_row = rng.randrange(size)
            matrix[target_row] = matrix[target_row][:-1]
            return Pattern(
                name=case_name,
                size=size,
                input_matrix=matrix,
                expected=label,
                raw_expected=label.value,
            )

        if anomaly == AnomalyType.SIZE_MISMATCH:
            # 선언된 size(N)와 다른 크기((N+2)×(N+2)) 행렬 주입
            wrong_matrix = self._build_signal_matrix(rng, size + 2, label)
            return Pattern(
                name=case_name,
                size=size,
                input_matrix=wrong_matrix,
                expected=label,
                raw_expected=label.value,
            )

        if anomaly == AnomalyType.INVALID_VALUE:
            # 임의 위치에 범위 이탈(-9999.0, 9999.0) 또는 NaN/inf 주입
            r = rng.randrange(size)
            c = rng.randrange(size)
            matrix[r][c] = rng.choice([float("nan"), float("inf"), -9999.0, 9999.0])
            return Pattern(
                name=case_name,
                size=size,
                input_matrix=matrix,
                expected=label,
                raw_expected=label.value,
            )

        # AnomalyType.INVALID_LABEL: 오타 라벨 주입
        bad_label = rng.choice(self.INVALID_LABELS)
        return Pattern(
            name=case_name,
            size=size,
            input_matrix=matrix,
            expected=None,
            raw_expected=bad_label,
        )

    def _build_signal_matrix(
        self, rng: random.Random, size: int, label: PatternLabel
    ) -> List[List[float]]:
        """지정된 라벨 위치에는 신호 강도(0.8~1.0), 그 외에는 노이즈(0.0~0.2)를 채운다."""
        center = size // 2
        matrix: List[List[float]] = []

        for i in range(size):
            row: List[float] = []
            for j in range(size):
                is_signal = (
                    (i == center or j == center)
                    if label == PatternLabel.CROSS
                    else (i == j or i + j == size - 1)
                )
                val = (
                    rng.uniform(SIGNAL_MIN_VALUE, MAX_CELL_VALUE)
                    if is_signal
                    else rng.uniform(0.0, NOISE_MAX_VALUE)
                )
                row.append(round(val, 4))
            matrix.append(row)

        return matrix
