# Mini NPU 시뮬레이터

패턴과 필터 간의 MAC(Multiply-Accumulate) 연산을 수행하고, 연산 성능(평균 실행 시간) 및 판정 정확도를 분석하는 콘솔 기반 시뮬레이터입니다.

## 📂 프로젝트 구조

```text
├── constants/      # 상수, 허용오차(EPSILON), 실행 모드 및 판정 결과 Enum
├── models/         # 연산 및 판정 결과를 담는 DTO (MacResult)
├── views/          # 콘솔 사용자 입력 검증(InputView) 및 결과 출력(OutputView)
├── services/       # 핵심 MAC 연산, 성능 측정 및 판정 로직(CalculatorService)
├── controllers/    # 계층 조립 및 실행 흐름 제어(SimulatorController)
└── main.py         # 의존성 주입(DI) 및 프로그램 진입점
```

## 📝 커밋 컨벤션 (Commit Convention)

작업 성격(Type)과 기능 영역(Scope)을 명확히 구분하여 커밋 히스토리를 관리합니다.

### 기본 형식
```text
<type>(<scope>): <제목>

- <상세 변경 내역 1>
- <상세 변경 내역 2>
```

### Type (작업 성격)
- `chore` / `init`: 프로젝트 초기 구조 세팅, 환경 설정, 기타 잡무
- `feat`: 새로운 기능 구현
- `fix`: 버그 및 예외 케이스 수정
- `refactor`: 동작 변경 없는 코드 구조 개선 및 리팩토링
- `docs`: README 등 문서 작성 및 수정

### Scope (기능 영역)
- `core`: 모드 1·2에서 공통으로 사용하는 핵심 연산 및 판정 엔진
- `mode1`: 모드 1 (사용자 3×3 직접 입력 및 판정) 관련 기능
- `mode2`: 모드 2 (`data.json` 파싱, 실패 분석 및 성능 표) 관련 기능
- *(생략 가능)*: 전체 구조나 문서 작업 등 특정 모드에 국한되지 않는 경우