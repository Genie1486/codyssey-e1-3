from repositories.json_repository import JsonRepository
from services.analysis_service import AnalysisService
from views.input_view import InputView
from views.output_view import OutputView
from services.calculator_service import CalculatorService
from controllers.simulator_controller import SimulatorController


def main() -> None:
    input_view = InputView()
    output_view = OutputView()
    calculator_service = CalculatorService()
    json_repository = JsonRepository()
    analysis_service = AnalysisService(
        calculator=calculator_service, repository=json_repository
    )

    simulator_controller = SimulatorController(
        input_view=input_view,
        output_view=output_view,
        calculator_service=calculator_service,
        analysis_service=analysis_service,
    )
    simulator_controller.run()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램을 종료합니다.")
