from models.mac_result import MacResult


class OutputView:
    """콘솔 화면 출력을 담당하는 뷰 클래스"""

    DIVIDER: str = "#----------------------------------------"

    def display_title(self) -> None:
        """시뮬레이터 시작 타이틀을 출력한다."""
        pass

    def display_mode_choice(self) -> None:
        """선택 가능한 실행 모드 목록을 출력한다."""
        pass

    def display_header(self, title: str) -> None:
        """구분선과 함께 섹션 헤더(예: [1] 필터 입력)를 출력한다."""
        pass

    def display_filter_saved(self, filter_name: str) -> None:
        """필터 저장 완료 확인 메시지를 출력한다."""
        pass

    def display_mac_result(self, result: MacResult) -> None:
        """MacResult 객체를 받아 MAC 점수, 평균 연산 시간(ms), 최종 판정 결과를 출력한다."""
        pass

    def display_performance_table(self, results: list) -> None:
        """크기별(N×N) 평균 연산 시간(ms)과 연산 횟수(N²) 성능 분석 표를 출력한다."""
        pass
