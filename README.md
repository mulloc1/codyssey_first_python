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
  "best_score": 1
}
```

- `quizzes`: 퀴즈 목록(객체 배열)
  - `question`: 질문 문자열
  - `choices`: 선택지 4개 문자열 배열
  - `answer`: 정답 번호(1..4 범위의 정수)
  - `hint`: 힌트 문자열
- `best_score`: 최고 점수(정수)
