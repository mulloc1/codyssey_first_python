# Quiz Game

터미널에서 실행하는 파이썬 객관식 퀴즈 게임입니다. 기본 퀴즈를 불러와 진행하고, 게임 중/추가된 퀴즈와 최고 점수를 `state.json`에 저장합니다.

## 퀴즈 주제와 선정 이유

기본 퀴즈는 파이썬 기초 개념을 확인하는 내용으로 구성되어 있습니다. 예를 들어 `int` 타입, 분기(`if/elif/else`), 길이(`len`), 함수 정의(`def`), 클래스 초기화(`__init__`) 같은 주제를 다뤄서 초보 학습자가 핵심 문법을 빠르게 점검할 수 있도록 했습니다.

## 실행 방법

프로젝트 디렉터리 `first_python`에서 다음을 실행합니다.

```bash
python main.py
```

## 기능 목록

1. 기본 퀴즈 로드 및 시작
2. 퀴즈 풀기(`play_quiz`)
3. 퀴즈 추가(`add_quiz`) 및 상태 저장
4. 퀴즈 목록 출력(`list_quizzes`)
5. 최고 점수 확인(`show_best_score`)
6. 퀴즈 삭제(`delete_quiz`) 및 상태 저장
7. 상태 파일 저장/불러오기(`save_state`, `load_state`)
8. 문제 수 선택 및 랜덤 출제
9. 풀이 중 힌트 보기와 힌트 사용 시 점수 차감
10. 입력 오류 방지(비어 있는 입력, 숫자 범위 등 재입력 처리)

메인 메뉴: 1 퀴즈 풀기, 2 퀴즈 추가, 3 퀴즈 목록, 4 점수 확인, 5 퀴즈 삭제, 6 종료.

## 파일 구조

```text
first_python/
├─ main.py
├─ README.md
├─ .gitignore
├─ src/
│  ├─ data/
│  │  ├─ __init__.py
│  │  └─ default_quizzes.py
│  └─ models/
│     ├─ __init__.py
│     ├─ quiz.py
│     └─ quiz_game.py
├─ tests/
│  ├─ data/
│  │  └─ test_default_quizzes.py
│  └─ models/
│     ├─ test_quiz_game.py
│     └─ test_quiz.py
└─ docs/
   ├─ subject.md
   ├─ plan.md
   ├─ testing_guidelines.md
   └─ insights/
      └─ python_package_and_object_lifecycle_insights.md
```

## 유닛 테스트 개요

`tests/` 아래 모듈은 `unittest`로 작성되어 있으며, **도메인 모델(`Quiz`)**, **앱 흐름(`QuizGame`)**, **기본 시드 데이터**를 각각 나누어 검증한다.

### 실행 방법

`first_python` 디렉터리에서 `PYTHONPATH`를 프로젝트 루트로 두고 모듈 경로를 지정해 실행한다(패키지 구조상 `discover`만으로는 테스트를 잡지 못할 수 있다).

```bash
cd first_python
PYTHONPATH=. python3 -m unittest tests.models.test_quiz tests.models.test_quiz_game tests.data.test_default_quizzes -v
```

### 테스트 파일별 목적

| 파일 | 목적 |
|------|------|
| [`tests/data/test_default_quizzes.py`](tests/data/test_default_quizzes.py) | `build_default_quizzes()`가 **`Quiz` 인스턴스 리스트**를 반환하는지, 개수·질문 중복·의도한 파이썬 기초 주제 문구 포함·**비어 있지 않은 힌트** 등 **초기 시드 데이터 품질**을 검증한다. |
| [`tests/models/test_quiz.py`](tests/models/test_quiz.py) | **`Quiz` 한 문항**에 대해 생성자 검증(타입·빈 문자열·선택지 4개·정답 범위 등), **공백 trim 정규화**, `from_dict` 역직렬화·잘못된 입력 시 예외·필수 키 누락 시 `KeyError` 등 **문항 도메인 규칙과 메시지**를 검증한다. |
| [`tests/models/test_quiz_game.py`](tests/models/test_quiz_game.py) | **`QuizGame`**의 메뉴 분기, `play_quiz`(출제 수 선택·셔플·정답/오답·힌트·점수·히스토리·`save_state`/재로드), `add_quiz`/`delete_quiz`/`list_quizzes`/`show_best_score`, **`load_state`**(`history` 생략·손상 기록·손상 문항 시 복구), **Ctrl+C·EOF 안전 종료** 등 **터미널 게임 전체 흐름**을 `input`/`print` 모킹과 임시 `state.json`으로 검증한다. |

## 데이터 파일 설명 (`state.json` 경로/역할/스키마)

- `state.json`은 게임 실행 중 사용자의 진행 상황을 저장하는 파일입니다.
- 기본적으로 `QuizGame(state_file_path="state.json")`처럼, **현재 실행 위치의 `state.json`** (작업 디렉터리 기준 경로)에 생성됩니다.
- `load_state()`에서 `state.json`이 없으면 기본 퀴즈(`build_default_quizzes()`)로 시작하고, 파일이 손상되었거나 읽기/스키마 오류가 나면 기본 데이터로 복구합니다.
- 현재 스키마는 각 퀴즈에 필수 `hint`를 포함합니다. 예전 스키마의 `state.json`은 자동 마이그레이션하지 않으며, 필요하면 새 파일을 다시 생성해 사용합니다.

### 스키마(최소 예시)

```json
{
  "quizzes": [
    {
      "question": "문제 질문",
      "choices": ["선택1", "선택2", "선택3", "선택4"],
      "answer": 2,
      "hint": "정답을 유추할 수 있는 짧은 설명"
    }
  ],
  "best_score": 1,
  "history": [
    {
      "at": "2026-04-04T14:30:00",
      "question_count": 3,
      "score": 2
    }
  ]
}
```

- `quizzes`: 퀴즈 목록(객체 배열)
  - `question`: 질문 문자열
  - `choices`: 선택지 4개 문자열 배열
  - `answer`: 정답 번호(1..4 범위의 정수)
  - `hint`: 힌트 문자열
- `best_score`: 최고 점수(정수)
- `history`: 플레이 기록 배열(선택). 없으면 빈 배열로 간주한다.
  - `at`: 기록 시각(ISO 형식 문자열)
  - `question_count`: 해당 라운드 출제 문제 수(정수)
  - `score`: 해당 라운드 획득 점수(정수, 힌트 반영 후)

---

## GitHub 저장소 및 커밋 확인

- **저장소 URL(제출 시 본인 주소로 교체)**: `https://github.com/<사용자명>/<저장소명>`
- 원격 저장소가 연결되어 있는지 확인하려면 프로젝트 루트(또는 `first_python`의 상위 저장소 루트)에서 다음을 실행합니다.

```bash
git remote -v
```

- **커밋 개수(10개 이상 여부)** 확인:

```bash
git rev-list --count HEAD
```

- **최근 커밋 내역** 확인:

```bash
git log --oneline --decorate -20
```

## 브랜치·병합 기록 확인

기능 단위로 브랜치를 나누어 작업했다면, 로컬·원격 브랜치 목록과 병합 여부는 아래로 확인할 수 있습니다.

```bash
git branch -a
git log --oneline --graph --all -30
```

- **브랜치를 분리하는 이유**: `main`(또는 `master`)은 항상 동작 가능한 기준선으로 두고, 새 기능·실험·과제 단계는 별도 브랜치에서 진행하면 기존 코드를 깨뜨리지 않은 채로 개발할 수 있다.
- **병합(merge)의 의미**: 브랜치에서 완성한 변경을 기준 브랜치에 합쳐, 한 줄기 히스토리(또는 merge 커밋)로 프로젝트 전체에 반영하는 과정이다. PR(Pull Request) 후 병합하면 코드 리뷰와 CI와 연계하기 쉽다.

## 커밋 단위 분리 및 커밋 메시지 규칙

- **커밋 단위**: 한 커밋에는 하나의 논리적 변경(예: 퀴즈 삭제 기능 추가, 히스토리 저장, 테스트 보강, README 수정)만 담는 것을 권장한다. 서로 무관한 수정을 한 커밋에 섞으면 되돌리기·리뷰·이력 추적이 어려워진다.
- **메시지 컨벤션(예시)**:
  - 첫 줄: 무엇을 했는지 한 문장(50자 내외 권장).
  - 필요 시 본문에서 이유·주의사항을 적는다.
  - 타입 접두어를 쓰는 경우: `feat:`, `fix:`, `docs:`, `test:`, `refactor:` 등([Conventional Commits](https://www.conventionalcommits.org/) 스타일).
- 이 저장소에서는 과제 진행 단계별로 커밋을 쌓아 **총 10개 이상**의 커밋을 유지하는 것을 목표로 한다(위 `git rev-list --count HEAD`로 확인).

## 클래스 책임 분리: `Quiz`와 `QuizGame`

| 클래스 | 책임 |
|--------|------|
| **`Quiz`** (`src/models/quiz.py`) | **한 문항**의 데이터를 표현한다. 질문·선택지·정답·힌트의 유효성 검사, 화면용 문자열(`format_question`), 정답 판정(`is_correct`), JSON 직렬화(`to_dict` / `from_dict`)만 담당한다. 터미널 입출력·메뉴·파일 경로·점수 누적은 모른다. |
| **`QuizGame`** (`src/models/quiz_game.py`) | **애플리케이션/게임 흐름**을 맡는다. 메뉴, 사용자 입력 루프, 출제·채점 루프, `state.json` 로드/저장, 최고 점수·히스토리, 퀴즈 목록 CRUD를 처리한다. 개별 문항 규칙은 `Quiz`에 위임한다. |

이렇게 나누면 “문항 데이터 규칙”과 “게임이 돌아가는 방식”이 섞이지 않아 수정 범위를 줄일 수 있다.

## 입력 처리·게임 진행·데이터 처리의 분리 기준

- **입력 처리**: `QuizGame`의 `_get_quiz_answer`, `_get_answer_with_hint`, `_get_question_count`, `get_menu_choice` 등 `_*` 접두 입력 헬퍼가 담당한다. 공통 패턴은 “빈 입력·형식 오류 시 재요청, `KeyboardInterrupt`/`EOFError` 시 안전 종료 위임”이다.
- **게임 진행**: `run` → 메뉴 → `_dispatch_menu` → `play_quiz` / `add_quiz` 등이 담당한다. 사용자와의 대화 순서와 라운드 진행만 여기서 조율한다.
- **데이터 처리**: `Quiz`가 문항 단위 검증·변환, `load_state`/`save_state`가 파일과 메모리 동기화, `src/data/default_quizzes.py`가 초기 시드 데이터를 제공한다. JSON 파싱 결과는 신뢰하지 않고 `Quiz.from_dict`·히스토리 파싱에서 타입을 검증한다.

## Ctrl+C·EOF 안전 종료(Graceful Shutdown)

- 터미널에서 **Ctrl+C**는 파이썬에서 `KeyboardInterrupt`로 올라온다. 입력이 파이프 등으로 끊기면 **`EOFError`**가 난다.
- `QuizGame`은 메뉴·각종 `input` 루프와 `run`의 최상위에서 이 예외를 잡아 **`_handle_safe_shutdown()`**을 호출한다. 이 메서드는 안내 문구를 출력한 뒤 **`save_state()`**로 가능한 범위에서 `state.json`을 저장하고, **`_is_running`을 `False`로** 두어 메인 루프가 자연스럽게 빠져나가게 한다. 저장 중 예외가 나도 프로세스를 강제로 죽이지 않고 메시지를 남긴다.

구현 위치: `src/models/quiz_game.py`의 `_handle_safe_shutdown`.

## 클래스를 쓰는 이유와 함수만 쓰는 방식과의 차이

- **클래스(`Quiz`, `QuizGame`)**: 상태(퀴즈 목록, 최고 점수, 히스토리, 실행 플래그)와 그 상태를 다루는 메서드를 한곳에 묶을 수 있다. 같은 데이터에 대해 여러 함수에 인자를 반복해서 넘기지 않아도 되고, 테스트에서 `QuizGame` 인스턴스만 만들면 된다.
- **절차지향(함수만)**: 전역 변수나 긴 인자 목록으로 상태를 넘기기 쉬워지고, 파일이 커질수록 “누가 무엇을 바꾸는지” 추적이 어려워질 수 있다.
- 이 프로젝트는 규모가 작지만, 과제·확장(새 메뉴, 새 필드)을 고려해 도메인 객체(`Quiz`)와 애플리케이션 서비스(`QuizGame`)를 분리한 객체지향 구조로 정리했다.

## JSON을 선택한 이유와 형식 특징

- **가독성**: 텍스트 기반이라 에디터·diff로 내용을 바로 확인할 수 있다.
- **언어 중립·표준**: 파이썬 `json` 모듈과 대부분의 언어·도구와 호환되어, 나중에 다른 클라이언트가 같은 파일을 읽기 쉽다.
- **구조 표현**: 객체·배열로 퀴즈 목록과 메타데이터(`best_score`, `history`)를 한 파일에 계층적으로 담기 좋다.
- **한계(트레이드오프)**: 스키마 검증·버전 관리는 JSON 자체에 내장되어 있지 않아, 애플리케이션 코드(`load_state`, `Quiz.from_dict` 등)에서 검증 책임을 진다. 동시에 여러 프로세스가 같은 파일을 쓰면 경쟁 상태가 생길 수 있어, 이 과제 범위에서는 단일 사용자·단일 프로세스 가정에 맞는다.

## 퀴즈 데이터가 많아질 때 JSON 파일 방식의 한계

- **메모리**: `load_state()` 시 파일 전체를 문자열로 읽고 파싱한 뒤 리스트로 올리므로, 퀴즈 수가 매우 크면 **한 번에 메모리에 올라가는 크기**가 커진다.
- **저장 비용**: `save_state()`마다 전체 `quizzes` 배열을 다시 쓰면, 항목이 수만 개일 때 **쓰기 시간·디스크 I/O**가 커진다.
- **부분 갱신**: JSON 파일 하나는 보통 “통째로 읽고 통째로 쓰는” 패턴이라, 한 문항만 고칠 때도 전체를 다시 직렬화해야 한다.
- **동시성**: 여러 인스턴스가 동시에 같은 파일을 갱신하면 마지막 저장이 이기는 식으로 **데이터 유실** 위험이 있다.
- 확장 시에는 DB(SQLite 등), 분할 파일, 또는 append-only 로그 후 집계 같은 방식을 검토할 수 있다.

## 요구사항 변경 시 수정 포인트(유지보수·확장)

| 변경 내용 | 주로 손댈 위치 |
|-----------|----------------|
| 문항 필드 추가·규칙 변경 | `Quiz` (`quiz.py`), `to_dict`/`from_dict`, `state.json` 스키마·`load_state` 검증 |
| 기본 제공 퀴즈 내용 | `src/data/default_quizzes.py` |
| 메뉴 항목·입력 프롬프트 | `Menu`, `show_menu`, `get_menu_choice`, `_dispatch_menu` (`quiz_game.py`) |
| 출제·채점·점수 규칙 | `play_quiz` 및 관련 `_get_*` (`quiz_game.py`) |
| 저장 형식·경로·복구 정책 | `load_state`, `save_state`, `_parse_history_from_state` (`quiz_game.py`) |
| 앱 진입점·실행 방식 | `main.py` |
| 자동 검증(회귀) | `tests/` 아래 해당 모듈의 테스트 메서드 추가·수정 |

새 기능을 넣을 때는 가능하면 **`Quiz`는 문항 도메인**, **`QuizGame`은 유스케이스**에만 얹어서, 책임이 섞이지 않게 유지하는 것이 좋다.
