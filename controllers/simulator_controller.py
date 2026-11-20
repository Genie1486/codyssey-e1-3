import json
from typing import List

from constants.constants import (
    DEFAULT_USER_SIZE,
    FAILED_CASES_PATH,
    NORMAL_PATTERN_RATIO,
    PASSED_CASES_PATH,
    MatrixType,
    Mode,
    SectionHeader,
    TestStatus,
)
from models.filter import Filter
from repositories.json_repository import JsonRepository
from services.analysis_service import AnalysisService
from services.calculator_service import CalculatorService
from services.pattern_generator import PatternGenerator
from views.input_view import InputView
from views.output_view import OutputView


class SimulatorController:
    """뷰와 서비스를 주입받아 전체 실행 흐름을 제어하는 컨트롤러 클래스"""

    ERR_FILE_NOT_FOUND: str = (
        "파일을 찾을 수 없습니다. data.json 파일 경로를 확인해주세요."
    )
    ERR_JSON_DECODE: str = (
        "JSON 형식이 올바르지 않습니다. data.json 문법을 확인해주세요."
    )
    ERR_INVALID_DATA: str = (
        "데이터 구조 또는 값이 올바르지 않습니다 ({detail}). data.json 파일을 확인해주세요."
    )
    ERR_FILE_IO: str = (
        "파일을 읽는 중 오류가 발생했습니다 ({detail}). data.json 파일을 확인해주세요."
    )

    def __init__(
        self,
        input_view: InputView,
        output_view: OutputView,
        calculator_service: CalculatorService,
        json_repository: JsonRepository,
        analysis_service: AnalysisService,
        pattern_generator: PatternGenerator | None = None,
    ) -> None:
        self._input_view = input_view
        self._output_view = output_view
        self._calculator_service = calculator_service
        self._json_repository = json_repository
        self._analysis_service = analysis_service
        self._pattern_generator = pattern_generator or PatternGenerator()

    def run(self) -> None:
        """타이틀 및 메뉴를 출력하고 사용자 선택에 따라 해당 모드를 실행한다."""
        self._output_view.display_title()

        while True:
            self._output_view.display_mode_choice()
            mode = self._input_view.get_mode_choice()

            if mode == Mode.EXIT.value[0]:
                self._output_view.display_exit()
                break

            self._handle_mode(mode)

    def _handle_mode(self, mode: int) -> None:
        if mode == Mode.USER_INPUT.value[0]:
            self._run_user_input_mode()
        elif mode == Mode.JSON_ANALYSIS.value[0]:
            self._run_json_analysis_mode()
        elif mode == Mode.PATTERN_GENERATION.value[0]:
            self._run_pattern_generation_mode()

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
        try:
            loaded_filters = self._analysis_service.load_filters()
            self._output_view.display_loaded_filters(loaded_filters)

            loaded_patterns = self._analysis_service.load_patterns()
            case_results = self._analysis_service.analyze_patterns(
                loaded_patterns, loaded_filters
            )
            self._output_view.display_pattern_analysis(case_results)

            perf_results = self._analysis_service.measure_performance(case_results)
            self._output_view.display_performance_analysis(perf_results)

            summary = self._analysis_service.summarize_result(case_results)
            self._output_view.display_summary(summary)

        except FileNotFoundError:
            self._output_view.display_error(self.ERR_FILE_NOT_FOUND)
        except json.JSONDecodeError:
            self._output_view.display_error(self.ERR_JSON_DECODE)
        except ValueError as e:
            self._output_view.display_error(self.ERR_INVALID_DATA.format(detail=e))
        except (OSError, UnicodeDecodeError) as e:
            self._output_view.display_error(self.ERR_FILE_IO.format(detail=e))

    def _run_pattern_generation_mode(self) -> None:
        """[모드 3] 재현성 SEED 기반 패턴 생성 및 무결성·성능 검증, 결과 JSON 저장을 실행한다."""
        size, count = self._input_view.get_pattern_generation_params()

        normal_count = round(count * NORMAL_PATTERN_RATIO)
        anomaly_count = count - normal_count
        self._output_view.display_pattern_generation_info(
            size=size,
            count=count,
            seed=self._pattern_generator.seed,
            normal_count=normal_count,
            anomaly_count=anomaly_count,
        )

        default_filter = Filter.create_default_filters(size)
        filters = {size: default_filter}
        patterns = self._pattern_generator.generate_patterns(size=size, count=count)

        case_results = self._analysis_service.analyze_patterns(patterns, filters)
        self._output_view.display_pattern_analysis(case_results)

        perf_results = self._analysis_service.measure_performance(case_results)
        self._output_view.display_performance_analysis(perf_results)

        summary = self._analysis_service.summarize_result(case_results)
        self._output_view.display_summary(summary)

        passed_results = [r for r in case_results if r.status == TestStatus.PASS]
        failed_results = [r for r in case_results if r.status == TestStatus.FAIL]

        passed_path = (
            self._json_repository.save_cases(
                filename=PASSED_CASES_PATH,
                patterns=patterns,
                case_results=passed_results,
                seed=self._pattern_generator.seed,
                size=size,
            )
            if passed_results
            else None
        )
        failed_path = (
            self._json_repository.save_cases(
                filename=FAILED_CASES_PATH,
                patterns=patterns,
                case_results=failed_results,
                seed=self._pattern_generator.seed,
                size=size,
            )
            if failed_results
            else None
        )

        self._output_view.display_export_summary(
            passed_count=len(passed_results),
            passed_path=passed_path,
            failed_count=len(failed_results),
            failed_path=failed_path,
        )
