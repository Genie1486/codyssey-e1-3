from typing import List
from constants.constants import MatrixType


class InputView:
    """콘솔 사용자 입력 및 유효성 검증을 담당하는 뷰 클래스"""

    def get_mode_choice(self, min_val: int, max_val: int) -> int:
        """사용자로부터 유효한 모드 번호(min_val ~ max_val)를 입력받아 반환한다."""
        pass

    def _get_number_until_valid(self, min_val: int, max_val: int) -> int:
        """유효한 범위의 정수가 입력될 때까지 반복해서 입력받는다."""
        pass

    def _validate_int_num(self, raw_input: str, min_val: int, max_val: int) -> bool:
        """입력 문자열이 정수인지, 지정된 범위(min_val ~ max_val) 내에 있는지 검증한다."""
        pass

    def get_n_by_n_matrix(self, n: int, matrix_type: MatrixType) -> List[List[float]]:
        """n×n 크기의 2차원 행렬(필터 또는 패턴)을 한 줄씩 입력받아 반환한다."""
        pass

    def _get_row_until_valid(self, row_idx: int, n: int) -> List[float]:
        """유효한 n개의 실수로 이루어진 한 행이 입력될 때까지 재입력을 유도한다."""
        pass

    def _validate_row(self, raw_row: str, n: int) -> bool:
        """공백으로 분리된 원소가 n개인지, 모두 실수(float)로 변환 가능한지 검증한다."""
        pass
