from constants.constants import REPEAT_COUNT, JudgeResult, Mode, SectionHeader
from models.mac_result import MacResult


class OutputView:
    """콘솔 화면 출력을 담당하는 뷰 클래스"""

    DIVIDER: str = "#----------------------------------------"
    TITLE_SIMULATOR: str = "=== Mini NPU Simulator ==="
    HEADER_MODE_SELECT: str = "[모드 선택]"

    MSG_MODE_ITEM: str = "{idx}. {mode_name}"
    MSG_FILTER_SAVED: str = "✅ {filter_name} 저장 완료"
    MSG_SCORE_A: str = "A 점수: {score}"
    MSG_SCORE_B: str = "B 점수: {score}"
    MSG_AVG_TIME: str = "연산 시간(평균/{repeat}회): {time:.3f} ms"
    MSG_JUDGE_RESULT: str = "판정: {result}"

    def display_title(self) -> None:
        """시뮬레이터 시작 타이틀을 출력한다."""
        print(self.TITLE_SIMULATOR)

    def display_mode_choice(self) -> None:
        """선택 가능한 실행 모드 목록을 출력한다."""
        print()
        print(self.HEADER_MODE_SELECT)
        print()
        for mode in Mode:
            print(self.MSG_MODE_ITEM.format(idx=mode.value[0], mode_name=mode.value[1]))

    def display_header(self, title: SectionHeader) -> None:
        """구분선과 함께 섹션 헤더(예: [1] 필터 입력)를 출력한다."""
        print()
        print(self.DIVIDER)
        print(title.value)
        print(self.DIVIDER)

    def display_filter_saved(self, filter_name: str) -> None:
        """필터 저장 완료 확인 메시지를 출력한다."""
        print()
        print(self.MSG_FILTER_SAVED.format(filter_name=filter_name))
        print()

    def display_mac_result(self, result: MacResult) -> None:
        """MacResult 객체를 받아 MAC 점수, 평균 연산 시간(ms), 최종 판정 결과를 출력한다."""

        if result.judge_result == JudgeResult.UNDECIDED:
            self.display_header(SectionHeader.MAC_RESULT_UNDECIDED)
        else:
            self.display_header(SectionHeader.MAC_RESULT)
        if (
            result.score_a is not None
            and result.score_b is not None
            and result.avg_time_ms is not None
        ):
            if result.judge_result == JudgeResult.UNDECIDED:
                score_a_str = f"{result.score_a:.16f}"
                score_b_str = f"{result.score_b:.16f}"
            else:
                score_a_str = f"{result.score_a}"
                score_b_str = f"{result.score_b}"

            print(self.MSG_SCORE_A.format(score=score_a_str))
            print(self.MSG_SCORE_B.format(score=score_b_str))
            print(
                self.MSG_AVG_TIME.format(repeat=REPEAT_COUNT, time=result.avg_time_ms)
            )

        if result.judge_result is not None:
            print(self.MSG_JUDGE_RESULT.format(result=result.judge_result.value))

    def display_performance_table(self, results: list) -> None:
        """크기별(N×N) 평균 연산 시간(ms)과 연산 횟수(N²) 성능 분석 표를 출력한다."""
        # 모드 2 구현 시 작성
        pass
