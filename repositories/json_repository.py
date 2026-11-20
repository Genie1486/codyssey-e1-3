import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from constants.constants import DEFAULT_DATA_PATH, ErrorType
from models.case_result import CaseResult
from models.pattern import Pattern


class JsonRepository:
    """외부 JSON 파일 읽기 및 검증 결과 저장을 담당하는 저장소 클래스"""

    def __init__(self, file_path: Optional[Union[str, Path]] = None) -> None:
        self._base_dir: Path = Path(__file__).parent.parent
        if file_path is None:
            self._file_path: Path = self._base_dir / DEFAULT_DATA_PATH
        else:
            self._file_path = Path(file_path)

    def load_data(self) -> Dict[str, Any]:
        """JSON 파일을 읽어 파싱된 최상위 딕셔너리를 반환한다."""
        with open(self._file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError(ErrorType.SCHEMA_ERROR.value)

        return data

    def save_cases(
        self,
        filename: str,
        patterns: List[Pattern],
        case_results: List[CaseResult],
        seed: int,
        size: int,
    ) -> Path:
        """검증 결과(PASS 또는 FAIL) 케이스 목록을 JSON 파일로 저장하고 저장 경로를 반환한다."""
        pattern_map = {p.name: p for p in patterns}
        cases_payload: Dict[str, Any] = {}

        for res in case_results:
            pattern = pattern_map.get(res.case_name)
            entry: Dict[str, Any] = {
                "status": res.status.value,
                "expected": (
                    pattern.raw_expected
                    if pattern is not None
                    else (res.expected_label.value if res.expected_label else None)
                ),
                "predicted": res.predicted_label,
            }
            if res.fail_reason is not None:
                entry["fail_reason"] = res.fail_reason

            if res.mac_result is not None and res.mac_result.score_a is not None:
                entry["scores"] = {
                    "cross": self._sanitize_value(res.mac_result.score_a),
                    "x": self._sanitize_value(res.mac_result.score_b),
                }

            if pattern is not None:
                entry["input"] = self._sanitize_matrix(pattern.input_matrix)

            cases_payload[res.case_name] = entry

        payload = {
            "meta": {
                "seed": seed,
                "size": size,
                "total_saved": len(case_results),
            },
            "cases": cases_payload,
        }

        output_path = self._base_dir / filename
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        return output_path

    @classmethod
    def _sanitize_matrix(cls, matrix: Any) -> Any:
        """NaN, inf 등 비표준 JSON 수치를 안전한 문자열로 변환한다."""
        if not isinstance(matrix, list):
            return cls._sanitize_value(matrix)
        return [cls._sanitize_matrix(item) for item in matrix]

    @staticmethod
    def _sanitize_value(val: Any) -> Any:
        if isinstance(val, float) and not math.isfinite(val):
            return str(val)
        return val
