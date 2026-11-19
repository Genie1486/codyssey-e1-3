import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

from constants.constants import DEFAULT_DATA_PATH, ErrorType


class JsonRepository:
    """외부 JSON 파일에서 원본 데이터를 읽어오는 저장소 클래스"""

    def __init__(self, file_path: Optional[Union[str, Path]] = None) -> None:
        if file_path is None:
            self._file_path: Path = Path(__file__).parent.parent / DEFAULT_DATA_PATH
        else:
            self._file_path = Path(file_path)

    def load_data(self) -> Dict[str, Any]:
        """JSON 파일을 읽어 파싱된 최상위 딕셔너리를 반환한다."""
        with open(self._file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, dict):
            raise ValueError(ErrorType.SCHEMA_ERROR.value)

        return data
