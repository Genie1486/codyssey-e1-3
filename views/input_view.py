from typing import List, Optional, Tuple
from constants.constants import MatrixType, Mode


class InputView:
    """콘솔 사용자 입력 및 유효성 검증을 담당하는 뷰 클래스"""

    PROMPT_MODE: str = "선택: "

    ERR_INVALID_MODE: str = "[오류] 1, 2, 3, 4 중 하나를 입력해 주세요."

    PROMPT_PATTERN_SIZE: str = "생성할 패턴/필터 크기 N (양의 홀수)을 입력하세요: "
    ERR_INVALID_ODD_SIZE: str = "[오류] 1 이상의 양의 홀수를 입력해 주세요."

    PROMPT_PATTERN_COUNT: str = "생성할 패턴 개수 K (양의 정수)를 입력하세요: "
    ERR_INVALID_PATTERN_COUNT: str = "[오류] 1 이상의 양의 정수를 입력해 주세요."

    PROMPT_MATRIX_GUIDE: str = "{matrix_name} ({size}줄 입력, 공백 구분)"
    PROMPT_ROW_INPUT: str = "{row_num}행 입력해주세요: "

    ERR_EMPTY_INPUT: str = (
        "빈 값을 입력하였습니다. {min}~{max} 사이의 숫자를 입력해주세요."
    )
    ERR_OUT_OF_RANGE: str = (
        "범위에 맞지 않는 숫자입니다. {min}~{max} 사이의 숫자를 입력해주세요."
    )
    ERR_INVALID_INT: str = (
        "숫자로 변환할 수 없습니다. {min}~{max} 사이의 숫자를 입력해주세요."
    )
    ERR_EMPTY_ROW: str = "아무 숫자도 입력하지 않았습니다."
    ERR_INVALID_COUNT: str = "{size}개의 숫자가 아닙니다."
    ERR_INVALID_FLOAT: str = "{token}는 실수로 변환할 수 없습니다."

    def get_mode(self) -> Mode:
        """사용자로부터 유효한 실행 모드(1, 2, 3, 4)를 입력받아 Mode Enum으로 반환한다."""
        mode_map = {mode.value[0]: mode for mode in Mode}

        while True:
            raw = input(self.PROMPT_MODE).strip()
            if raw.isdigit() and int(raw) in mode_map:
                return mode_map[int(raw)]
            print(self.ERR_INVALID_MODE)

    def get_mode_choice(self) -> int:
        """사용자로부터 유효한 모드 번호(min_val ~ max_val)를 입력받아 반환한다."""
        return self._get_number_until_valid(1, len(Mode))

    def _get_number_until_valid(self, min_val: int, max_val: int) -> int:
        """유효한 범위의 정수가 입력될 때까지 반복해서 입력받는다."""
        while True:
            user_input = input(self.PROMPT_MODE).strip()
            parsed_num = self._parse_int_in_range(user_input, min_val, max_val)

            if parsed_num is not None:
                return parsed_num

    def _parse_int_in_range(
        self, raw_input: str, min_val: int, max_val: int
    ) -> Optional[int]:
        if len(raw_input) == 0:
            print(self.ERR_EMPTY_INPUT.format(min=min_val, max=max_val))
            return None

        try:
            parsed_num = int(raw_input)

            if parsed_num < min_val or parsed_num > max_val:
                print(self.ERR_OUT_OF_RANGE.format(min=min_val, max=max_val))
                return None

            return parsed_num

        except ValueError:
            print(self.ERR_INVALID_INT.format(min=min_val, max=max_val))
            return None

    def get_n_by_n_matrix(self, n: int, matrix_type: MatrixType) -> List[List[float]]:
        """n×n 크기의 2차원 행렬(필터 또는 패턴)을 한 줄씩 입력받아 반환한다."""
        result = []
        print(self.PROMPT_MATRIX_GUIDE.format(matrix_name=matrix_type.value, size=n))

        for i in range(n):
            row = self._get_row_until_valid(i, n)
            result.append(row)

        return result

    def _get_row_until_valid(self, row_idx: int, n: int) -> List[float]:
        """유효한 n개의 실수로 이루어진 한 행이 입력될 때까지 재입력을 유도한다."""
        while True:
            input_row = input(self.PROMPT_ROW_INPUT.format(row_num=row_idx + 1)).split()
            parsed_row = self._parse_valid_row(input_row, n)

            if parsed_row is not None:
                return parsed_row

    def _parse_valid_row(self, tokens: List[str], n: int) -> Optional[List[float]]:
        if len(tokens) == 0:
            print(self.ERR_EMPTY_ROW)
            return None

        if len(tokens) != n:
            print(self.ERR_INVALID_COUNT.format(size=n))
            return None

        result = []
        for token in tokens:
            try:
                result.append(float(token))
            except ValueError:
                print(self.ERR_INVALID_FLOAT.format(token=token))
                return None

        return result

    def get_pattern_generation_params(self) -> Tuple[int, int]:
        """패턴 크기 N(양의 홀수)과 생성 개수 K(양의 정수)를 입력받아 튜플로 반환한다."""
        while True:
            raw_size = input(self.PROMPT_PATTERN_SIZE).strip()
            if raw_size.isdigit():
                size = int(raw_size)
                if size > 0 and size % 2 == 1:
                    break
            print(self.ERR_INVALID_ODD_SIZE)

        while True:
            raw_count = input(self.PROMPT_PATTERN_COUNT).strip()
            if raw_count.isdigit():
                count = int(raw_count)
                if count > 0:
                    break
            print(self.ERR_INVALID_COUNT)

        return size, count
