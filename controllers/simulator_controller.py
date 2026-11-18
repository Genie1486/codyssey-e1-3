from typing import List

from constants.constants import (
    DEFAULT_USER_SIZE,
    MatrixType,
    Mode,
    SectionHeader,
)
from views.input_view import InputView
from views.output_view import OutputView
from services.calculator_service import CalculatorService


class SimulatorController:
    """뷰와 서비스를 주입받아 전체 실행 흐름을 제어하는 컨트롤러 클래스"""

    def __init__(
        self,
        input_view: InputView,
        output_view: OutputView,
        calculator_service: CalculatorService,
    ) -> None:
        self._input_view = input_view
        self._output_view = output_view
        self._calculator_service = calculator_service

    def run(self) -> None:
        """타이틀 및 메뉴를 출력하고 사용자 선택에 따라 해당 모드를 실행한다."""
        self._output_view.display_title()

        while True:
            self._output_view.display_mode_choice()
            choice = self._input_view.get_mode_choice()

            self._handle_mode(choice)

    def _handle_mode(self, choice: int) -> None:
        if choice == Mode.USER_INPUT.value[0]:
            self._run_user_input_mode()
        elif choice == Mode.JSON_ANALYSIS.value[0]:
            self._run_json_analysis_mode()

    def _run_user_input_mode(self) -> None:
        """모드 1(사용자 3×3 직접 입력)의 전체 실행 흐름을 조립하고 제어한다."""

        self._output_view.display_header(SectionHeader.FILTER_INPUT)

        filter_a = self._input_matrix_with_confirm(MatrixType.FILTER_A)

        filter_b = self._input_matrix_with_confirm(MatrixType.FILTER_B)

        self._output_view.display_header(SectionHeader.PATTERN_INPUT)

        pattern = self._input_matrix_with_confirm(MatrixType.PATTERN)

        result = self._calculator_service.calculate_result(filter_a, filter_b, pattern)

        self._output_view.display_mac_result(result)

    def _input_matrix_with_confirm(self, matrix_type: MatrixType) -> List[List[float]]:
        """행렬을 입력받고 저장 완료 메시지를 출력한다."""
        matrix = self._input_view.get_n_by_n_matrix(DEFAULT_USER_SIZE, matrix_type)
        self._output_view.display_filter_saved(matrix_type.value)
        return matrix

    def _run_json_analysis_mode(self) -> None:
        """모드 2(data.json 분석)의 전체 실행 흐름을 조립하고 제어한다."""
        print("모드2")
