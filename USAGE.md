# PocketDev 사용 가이드

이 문서는 PocketDev 시스템의 상세 사용 방법을 설명합니다.

## 목차
1. [시스템 요구사항](#시스템-요구사항)
2. [초기 설정](#초기-설정)
3. [기본 사용법](#기본-사용법)
4. [명령어 상세](#명령어-상세)
5. [실행 결과 확인](#실행-결과-확인)
6. [트러블슈팅](#트러블슈팅)

---

## 시스템 요구사항

### 집 PC (Self-hosted Runner)
- **OS**: Windows 10/11 (x64)
- **필수 소프트웨어**:
  - Git for Windows
  - Node.js 20 LTS 이상
  - Python 3.11 이상
- **네트워크**: 인터넷 연결 (GitHub와 통신)
- **권장**: PC가 항상 켜져 있거나, Wake-on-LAN 설정

### GitHub 저장소
- Self-hosted Runner 등록 완료
- Repository Secrets 설정 (`GEMINI_API_KEY` 등)
- Actions 권한 설정 완료

---

## 초기 설정

### 1. Self-hosted Runner 설치

```powershell
# 1. Runner 다운로드 및 압축 해제
mkdir C:\actions-runner && cd C:\actions-runner
Invoke-WebRequest -Uri https://github.com/actions/runner/releases/download/v2.330.0/actions-runner-win-x64-2.330.0.zip -OutFile runner.zip
Expand-Archive -Path runner.zip -DestinationPath .

# 2. GitHub에서 등록 토큰 받기 (gh CLI 사용)
gh api -X POST repos/{owner}/{repo}/actions/runners/registration-token --jq ".token"

# 3. Runner 등록
.\config.cmd --url https://github.com/{owner}/{repo} --token {TOKEN} --name home-desktop --labels home-desktop --unattended

# 4. Runner 실행 (수동)
.\run.cmd

# 또는 서비스로 등록 (권장 - PC 재시작 시 자동 실행)
.\svc.cmd install
.\svc.cmd start
```

### 2. GitHub 저장소 설정

#### Secrets 설정
`Settings` > `Secrets and variables` > `Actions` > `New repository secret`

| Secret 이름 | 설명 |
|------------|------|
| `GEMINI_API_KEY` | Google Gemini API 키 |
| `ANTHROPIC_API_KEY` | (선택) Anthropic Claude API 키 |
| `OPENAI_API_KEY` | (선택) OpenAI API 키 |

#### Actions 권한 설정
`Settings` > `Actions` > `General` > `Workflow permissions`

- [x] **Read and write permissions** 선택
- [x] **Allow GitHub Actions to create and approve pull requests** 체크

이 설정이 없으면 PR 생성이 실패합니다.

### 3. OpenCode 설치 확인

Runner PC에서 실행:
```powershell
npm install -g opencode-ai@1.1.3
opencode --version
```

---

## 기본 사용법

### Step 1: 이슈 생성

GitHub 저장소에서 새 이슈를 생성합니다.

**예시:**
- 제목: `로그인 기능 구현`
- 본문: 구현하고자 하는 기능의 상세 설명

### Step 2: `/oc` 명령어 입력

이슈의 **댓글**에 `/oc` 명령어와 함께 지시사항을 작성합니다.

```
/oc
로그인 페이지를 만들어줘.
- Flask 기반으로 작성
- ID/PW 입력 폼 포함
- 간단한 유효성 검사 추가
- pytest 테스트 코드 포함
```

### Step 3: 자동 실행 대기

1. GitHub Actions가 댓글을 감지
2. Self-hosted Runner가 작업 수행
3. OpenCode AI 에이전트가 코드 작성
4. 자동으로 PR 생성
5. 이슈에 결과 댓글 추가

### Step 4: PR 검토 및 병합

생성된 PR을 검토하고, 문제가 없으면 병합합니다.

---

## 명령어 상세

### 기본 형식

```
/oc
[지시사항]
```

`/oc` 뒤에 오는 모든 텍스트가 AI 에이전트에게 전달됩니다.

### 지시사항 작성 팁

#### 좋은 예시

```
/oc
사용자 인증 기능을 추가해줘.
- JWT 토큰 기반 인증
- /api/login, /api/logout 엔드포인트
- 비밀번호는 bcrypt로 해싱
- 기존 User 모델 활용
```

```
/oc
버그 수정: calculate_total() 함수에서 할인율이 적용되지 않는 문제
- tests/test_calculator.py의 실패하는 테스트 참고
- 할인율은 0~100 사이의 정수
```

#### 피해야 할 예시

```
/oc
좋은 코드 만들어줘
```
→ 너무 모호함. 구체적인 요구사항 필요.

```
/oc
전체 리팩토링
```
→ 범위가 너무 넓음. 작은 단위로 나누어 요청.

### 지시사항이 없는 경우

`/oc`만 입력하면 이슈 본문을 기반으로 자동 해결을 시도합니다.

```
/oc
```
→ "Resolve this issue. Commit changes and run tests, then create a summary report."

---

## 실행 결과 확인

### 1. GitHub Actions 로그

`Actions` 탭에서 워크플로우 실행 상태 확인:
- **OpenCode Agent (Windows self-hosted, Python)**: 메인 워크플로우
- **OpenCode Simple Test**: 간단한 테스트 워크플로우

### 2. 생성되는 파일

| 파일명 | 설명 |
|-------|------|
| `opencode_report.md` | AI 에이전트 작업 요약 리포트 |
| `pytest_output.txt` | pytest 실행 결과 |

### 3. PR 구조

자동 생성되는 PR:
- **제목**: `OpenCode: Issue #{번호} - {이슈 제목}`
- **브랜치**: `oc/issue-{번호}-{run_id}`
- **본문**: 이슈 링크 + 리포트 파일 참조

### 4. 이슈 댓글

작업 완료 후 이슈에 자동으로 댓글이 추가됩니다:
- PR 링크
- 리포트 미리보기 (3500자까지)

---

## 트러블슈팅

### 워크플로우가 실행되지 않음

**원인 1**: PR 댓글에 작성함
- **해결**: 이슈 댓글에만 `/oc` 명령어가 작동합니다.

**원인 2**: 권한 없는 계정
- **해결**: 저장소 Owner, Member, Collaborator만 트리거 가능합니다.

**원인 3**: Runner가 오프라인
- **해결**: Runner PC 확인, `run.cmd` 또는 서비스 재시작

```powershell
# Runner 상태 확인
gh api repos/{owner}/{repo}/actions/runners

# Runner 재시작
cd C:\actions-runner
.\run.cmd
```

### PR 생성 실패

**에러**: `GitHub Actions is not permitted to create or approve pull requests`

**해결**:
```bash
# API로 권한 설정
gh api repos/{owner}/{repo}/actions/permissions/workflow -X PUT \
  -f default_workflow_permissions=write \
  -F can_approve_pull_request_reviews=true
```

또는 GitHub 웹에서:
`Settings` > `Actions` > `General` > `Workflow permissions` 설정

### 한글 깨짐

Windows 인코딩 문제입니다. 워크플로우에서 UTF-8 설정이 포함되어 있지만, 일부 환경에서 깨질 수 있습니다.

**해결**: PowerShell에서 UTF-8 강제:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
```

### OpenCode 실행 오류

**원인**: API 키 미설정 또는 만료

**해결**:
1. GitHub Secrets에서 `GEMINI_API_KEY` 확인
2. API 키가 유효한지 확인
3. 필요시 새 키 발급 후 업데이트

---

## 자주 묻는 질문

**Q: 여러 저장소에서 같은 Runner를 사용할 수 있나요?**

A: 아니요. Runner는 하나의 저장소에만 등록됩니다. Organization 레벨 Runner를 사용하면 여러 저장소에서 공유 가능합니다.

**Q: Runner PC가 꺼져 있으면?**

A: 워크플로우가 `queued` 상태로 대기합니다. Runner가 온라인되면 자동으로 실행됩니다. (기본 24시간 후 만료)

**Q: AI가 잘못된 코드를 작성하면?**

A: PR이 생성되므로 병합 전에 반드시 코드 리뷰를 하세요. pytest 결과도 확인하세요.

**Q: 비용이 발생하나요?**

A: Self-hosted Runner는 무료입니다. AI API (Gemini/Claude/OpenAI) 사용량에 따라 비용이 발생합니다.

---

## 참고 링크

- [GitHub Actions Self-hosted Runners](https://docs.github.com/en/actions/hosting-your-own-runners)
- [OpenCode AI](https://github.com/opencode-ai/opencode)
- [Google Gemini API](https://ai.google.dev/)
