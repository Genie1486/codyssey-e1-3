from constants.constants import DEFAULT_USER_SIZE, MatrixType, Mode
from views.input_view import InputView
from views.output_view import OutputView
from services.calculator_service import CalculatorService


class SimulatorController:
    """뷰와 서비스를 주입받아 전체 실행 흐름을 제어하는 컨트롤러 클래스"""

    def __init__(
        self,
        input_view: InputView,
        output_view: OutputView,
        calculator_service: CalculatorService
    ) -> None:
        self._input_view = input_view
        self._output_view = output_view
        self._calculator_service = calculator_service

    def run(self) -> None:
        """타이틀 및 메뉴를 출력하고 사용자 선택에 따라 해당 모드를 실행한다."""
        pass

    def _run_user_input_mode(self) -> None:
        """모드 1(사용자 3×3 직접 입력)의 전체 실행 흐름을 조립하고 제어한다."""
        pass

    def _run_json_analysis_mode(self) -> None:
        """모드 2(data.json 분석)의 전체 실행 흐름을 조립하고 제어한다."""
        pass
