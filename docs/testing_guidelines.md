# 테스트 작성 규칙

이 문서는 Quiz Game 프로젝트의 테스트 작성/배치 규칙을 정의한다.

## 1) 폴더 구조 미러링 규칙 (최우선)

- 테스트 폴더 구조는 `src` 구조를 그대로 따라간다.
- 기준: `src/<path>/<module>.py` -> `tests/<path>/test_<module>.py`

예시:

- `src/data/default_quizzes.py` -> `tests/data/test_default_quizzes.py`
- `src/models/quiz.py` -> `tests/models/test_quiz.py`
- `src/models/quiz_game.py` -> `tests/models/test_quiz_game.py`

이 규칙은 "테스트 파일을 어디에 둘지"에 대한 기본 원칙이며 예외 없이 적용한다.

## 2) 테스트 파일 네이밍

- 파일명은 `test_*.py` 형식을 사용한다.
- 모듈 단위로 1개 테스트 파일을 기본으로 한다.
- 테스트 클래스/함수 이름은 기능이 드러나게 작성한다.
  - 예: `test_build_default_quizzes_returns_five_or_more_items`

## 3) 단일 책임 테스트

- 한 테스트는 한 가지 동작만 검증한다.
- 실패 시 원인이 바로 보이도록 assert를 좁게 쪼갠다.
- 여러 검증이 필요한 경우 테스트 함수를 분리한다.

## 4) 출력(print) 최소화

- 기본적으로 테스트에서 `print` 사용을 지양한다.
- `print`는 디버깅 목적의 임시 도구로만 사용하고, 최종 테스트에서는 제거한다.
- 검증은 `assert`로 표현한다.

## 5) 외부 상태 의존성 제한

- 테스트는 네트워크/시간/외부 파일 상태에 의존하지 않도록 작성한다.
- 파일 I/O가 필요하면 테스트 전용 임시 파일/디렉터리를 사용한다.
- 실행 순서와 무관하게 항상 동일한 결과가 나오도록 만든다.

## 6) 테스트 데이터 원칙

- 기본 데이터 검증 테스트는 최소 아래 항목을 포함한다.
  - 개수 조건 (예: `len(quizzes) >= 5`)
  - 타입 조건 (예: `Quiz` 인스턴스 여부)
  - 도메인 조건 (선택지 4개, 정답 범위 1..4)

## 7) 실행 규칙

- 단일 모듈 테스트:
  - `python3 -m unittest tests/data/test_default_quizzes.py -v`
- 전체 테스트:
  - `python3 -m unittest discover -s tests -p 'test_*.py' -v`

## 8) 이번 프로젝트에 즉시 적용할 매핑

- 기존 `tests/test_data_init.py`는 아래로 이동/분리하는 것을 권장한다.
  - `tests/data/test___init__.py` (패키지 export 검증)
  - `tests/data/test_default_quizzes.py` (기본 퀴즈 데이터 검증)

