from pathlib import Path
from typing import Dict, List, Optional

from constants.constants import (
    REPEAT_COUNT,
    JudgeResult,
    Mode,
    PatternLabel,
    SectionHeader,
    TestStatus,
)
from models.case_result import CaseResult
from models.filter import Filter
from models.mac_result import MacResult
from models.performance_result import PerformanceResult
from models.summary_result import SummaryResult


class OutputView:
    """콘솔 화면 출력을 담당하는 뷰 클래스"""

    DIVIDER_WIDTH: int = 65
    TOTAL_WIDTH: int = DIVIDER_WIDTH + 1
    DIVIDER: str = "#" + "-" * DIVIDER_WIDTH
    SUB_DIVIDER: str = "-" * TOTAL_WIDTH

    TITLE_SIMULATOR: str = "=== Mini NPU Simulator ==="
    HEADER_MODE_SELECT: str = "[모드 선택]"

    # 모드 1 메시지 포맷
    MSG_MODE_ITEM: str = "{idx}. {mode_name}"
    MSG_FILTER_SAVED: str = "✅ {filter_name} 저장 완료"
    MSG_SCORE_A: str = "A 점수: {score}"
    MSG_SCORE_B: str = "B 점수: {score}"
    MSG_AVG_TIME: str = "연산 시간(평균/{repeat}회): {time:.3f} ms"
    MSG_OPT_AVG_TIME: str = (
        "연산 시간 최적화 로직 적용(평균/{repeat}회): {opt_time:.3f} ms"
    )
    MSG_JUDGE_RESULT: str = "판정: {result}"

    # 모드 2 메시지 포맷
    MSG_FILTER_LOADED: str = "✓ size_{size} 필터 로드 완료 ({cross}, {x})"
    MSG_CASE_HEADER: str = "- -- {case_name} ---"
    MSG_PATTERN_SCORE: str = "{label} 점수: {score}"
    MSG_CASE_RESULT: str = "판정: {predicted} | expected: {expected} | {status}{reason}"

    # 전체 폭(TOTAL_WIDTH)을 5개 열 비율로 자동 배분
    COL_1_W: int = max(8, int(TOTAL_WIDTH * 0.12))  # 크기
    COL_2_W: int = max(14, int(TOTAL_WIDTH * 0.23))  # 기존 2D(ms)
    COL_3_W: int = max(16, int(TOTAL_WIDTH * 0.26))  # 최적화 1D(ms)
    COL_4_W: int = max(12, int(TOTAL_WIDTH * 0.20))  # 개선율(%)
    COL_5_W: int = TOTAL_WIDTH - (COL_1_W + COL_2_W + COL_3_W + COL_4_W)  # 연산 횟수

    # 전각 한글 글자 수만큼 포맷 폭 보정 (크기:2자, 기존:2자, 최적화:3자, 개선율:3자, 연산횟수:4자)
    MSG_PERF_HEADER: str = (
        f"{'크기':<{COL_1_W - 2}}"
        f"{'기존 2D(ms)':>{COL_2_W - 2}}"
        f"{'최적화 1D(ms)':>{COL_3_W - 3}}"
        f"{'개선율(%)':>{COL_4_W - 3}}"
        f"{'연산 횟수':>{COL_5_W - 4}}"
    )
    MSG_PERF_ROW: str = (
        f"{{size:<{COL_1_W}}}"
        f"{{avg_time:>{COL_2_W}.3f}}"
        f"{{opt_time:>{COL_3_W}.3f}}"
        f"{{rate:>{COL_4_W - 1}.1f}}%"
        f"{{op_count:>{COL_5_W}}}"
    )

    MSG_SUMMARY_TOTAL: str = "총 테스트: {count}개"
    MSG_SUMMARY_PASS: str = "통과: {count}개"
    MSG_SUMMARY_FAIL: str = "실패: {count}개"
    MSG_SUMMARY_FAIL_ITEM: str = "- {case_name}: {reason} 처리 규칙에 따라 {status}"
    MSG_ERROR: str = "\n[오류] {message}"

    LABEL_NONE: str = "없음"
    REASON_UNKNOWN: str = "알 수 없는 오류"

    MSG_GEN_CONFIG: str = (
        "크기: {size}×{size} | 총 {count}개 패턴 생성 (SEED={seed}, 정상 {normal}개 / 비정상 {anomaly}개)"
    )
    MSG_SAVED_PASSED: str = "[PASS] 예측 성공 케이스 저장 완료 ({count}건): {path}"
    MSG_SAVED_FAILED: str = "[FAIL] 검증 실패 케이스 저장 완료 ({count}건): {path}"
    MSG_NO_FAILED_CASES: str = (
        "[FAIL] 검증 실패 케이스가 없어 실패 파일을 생성하지 않았습니다."
    )

    MSG_EXIT: str = "프로그램을 종료합니다."

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

    def display_error(self, message: str) -> None:
        """오류 메시지를 출력한다."""
        print(self.MSG_ERROR.format(message=message))

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

            if result.opt_avg_time_ms is not None:
                print(
                    self.MSG_OPT_AVG_TIME.format(
                        repeat=REPEAT_COUNT, opt_time=result.opt_avg_time_ms
                    )
                )

        if result.judge_result is not None:
            print(self.MSG_JUDGE_RESULT.format(result=result.judge_result.value))

    def display_loaded_filters(self, filters: Dict[int, Filter]) -> None:
        """[1] 필터 로드 섹션을 출력한다."""
        self.display_header(SectionHeader.JSON_FILTER_LOAD)

        for size in sorted(filters.keys()):
            print(
                self.MSG_FILTER_LOADED.format(
                    size=size,
                    cross=PatternLabel.CROSS.value,
                    x=PatternLabel.X.value,
                )
            )

    def display_pattern_analysis(self, case_results: List[CaseResult]) -> None:
        """[2] 패턴 분석 섹션을 출력한다."""
        self.display_header(SectionHeader.JSON_PATTERN_ANALYSIS)
        for case_result in case_results:
            self._display_single_case_result(case_result)

    def _display_single_case_result(self, case_result: CaseResult) -> None:
        """개별 패턴 케이스의 분석 및 판정 결과를 출력한다."""
        print(self.MSG_CASE_HEADER.format(case_name=case_result.case_name))

        expected_str = (
            case_result.expected_label
            if case_result.expected_label is not None
            else self.LABEL_NONE
        )
        reason_suffix = (
            f" ({case_result.fail_reason})"
            if case_result.status == TestStatus.FAIL and case_result.fail_reason
            else ""
        )

        if case_result.mac_result is None:
            print(
                self.MSG_CASE_RESULT.format(
                    predicted=self.LABEL_NONE,
                    expected=expected_str,
                    status=case_result.status.value,
                    reason=reason_suffix,
                )
            )
            return

        precision = (
            16 if case_result.mac_result.judge_result == JudgeResult.UNDECIDED else 1
        )
        print(
            self.MSG_PATTERN_SCORE.format(
                label=PatternLabel.CROSS.value,
                score=f"{case_result.mac_result.score_a:.{precision}f}",
            )
        )
        print(
            self.MSG_PATTERN_SCORE.format(
                label=PatternLabel.X.value,
                score=f"{case_result.mac_result.score_b:.{precision}f}",
            )
        )
        print(
            self.MSG_CASE_RESULT.format(
                predicted=case_result.predicted_label,
                expected=expected_str,
                status=case_result.status.value,
                reason=reason_suffix,
            )
        )

    def display_performance_analysis(
        self, perf_results: List[PerformanceResult]
    ) -> None:
        """[3] 성능 분석 섹션을 출력한다."""
        self.display_header(SectionHeader.JSON_PERFORMANCE_ANALYSIS)

        print(self.MSG_PERF_HEADER)
        print(self.SUB_DIVIDER)

        for perf_result in perf_results:
            size_str = f"{perf_result.size}×{perf_result.size}"
            print(
                self.MSG_PERF_ROW.format(
                    size=size_str,
                    avg_time=perf_result.avg_time_ms,
                    opt_time=perf_result.opt_avg_time_ms,
                    rate=perf_result.improvement_rate,
                    op_count=perf_result.operation_count,
                )
            )

    def display_summary(self, summary: SummaryResult) -> None:
        """[4] 결과 요약 섹션을 출력한다."""
        self.display_header(SectionHeader.JSON_RESULT_SUMMARY)

        print(self.MSG_SUMMARY_TOTAL.format(count=summary.total_count))
        print(self.MSG_SUMMARY_PASS.format(count=summary.pass_count))
        print(self.MSG_SUMMARY_FAIL.format(count=summary.fail_count))

        if summary.fail_cases:
            print()
            for case_result in summary.fail_cases:
                reason = case_result.fail_reason or self.REASON_UNKNOWN
                print(
                    self.MSG_SUMMARY_FAIL_ITEM.format(
                        case_name=case_result.case_name,
                        reason=reason,
                        status=case_result.status.value,
                    )
                )

    def display_pattern_generation_info(
        self, size: int, count: int, seed: int, normal_count: int, anomaly_count: int
    ) -> None:
        """모드 3 패턴 생성 설정 요약을 출력한다."""
        self.display_header(SectionHeader.GEN_PATTERN_CONFIG)
        print(
            self.MSG_GEN_CONFIG.format(
                size=size,
                count=count,
                seed=seed,
                normal=normal_count,
                anomaly=anomaly_count,
            )
        )

    def display_export_summary(
        self,
        passed_count: int,
        passed_path: Optional[Path],
        failed_count: int,
        failed_path: Optional[Path],
    ) -> None:
        """모드 3 PASS/FAIL JSON 파일 저장 결과를 출력한다."""
        self.display_header(SectionHeader.GEN_FILE_EXPORT)
        if passed_path is not None:
            print(self.MSG_SAVED_PASSED.format(count=passed_count, path=passed_path))
        if failed_path is not None:
            print(self.MSG_SAVED_FAILED.format(count=failed_count, path=failed_path))
        elif failed_count == 0:
            print(self.MSG_NO_FAILED_CASES)

    def display_exit(self) -> None:
        """프로그램 종료 안내 메시지를 출력한다."""
        print(self.MSG_EXIT)
