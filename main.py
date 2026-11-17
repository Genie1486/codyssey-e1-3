from views.input_view import InputView
from views.output_view import OutputView
from services.calculator_service import CalculatorService
from controllers.simulator_controller import SimulatorController


def main() -> None:
    input_view = InputView()
    output_view = OutputView()
    calculator_service = CalculatorService()

    simulator_controller = SimulatorController(
        input_view=input_view,
        output_view=output_view,
        calculator_service=calculator_service
    )
    simulator_controller.run()


if __name__ == "__main__":
    main()
