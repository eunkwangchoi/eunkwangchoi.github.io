# Hugo 호환성 이행 실행 결과

실행일: 2026-10-07 (Asia/Seoul)

검토안의 순서에 따라 로컬 구현과 검증을 완료했다. 커밋·푸시·배포는 하지 않았다.
Hugo 0.167.0 및 기존 CI의 Dart Sass 1.101.0을 공통 기준으로 고정했다.

## 적용 결과

| 단계 | 구현 | 확인 결과 |
| --- | --- | --- |
| 기준선 및 API | 원상 복구 사본, `_internal` 7곳 → embedded partial, `.Scratch` 4곳 → `.Store`, Hugo 최소 버전 중첩 설정 수정 | 기존 출력과 비교해 About 밖의 차이 없음 |
| Sass | 공식 SHA-256 검증 후 workspace Dart Sass 설치, `transpiler=dartsass`, 스타일 진입점 및 Markdown 모듈에 `@use` 적용 | 374개 HTML의 변화는 inline style에만 한정; 경로·비스타일 마크업 변화 없음 |
| 템플릿 | 루트·활성 테마 partial, shortcode, home 파일명을 현재 lookup 구조로 이행 | Sass 전환 직후와 비교해 추가 출력 변화 없음 |
| 비활성 구성 | Coming Soon locale·템플릿·예제 Hugo 버전, Netlify 예제 버전 정렬 | Coming Soon 별도 로컬 빌드 성공; Netlify 원격 빌드는 미실행 |
| Vendor | obsolete extended 요구사항 제거, icons partial 이동, 재적용 patch 제공 | 현재 트리에 patch reverse-check 성공 |
| 공통 실행 | `run_hugo.py`의 Hugo/Sass 버전 점검·로그·deprecation 목록, PDF 및 CI 호출 통일 | 일반 개발·배포·minify 빌드 성공 |
| 배포 검사 | HTML minify의 따옴표 생략을 고려하도록 앵커 검사를 HTMLParser로 변경 | minified CV의 writings/press 앵커 검증 성공 |

## 검증 증거

- Python 테스트 **32개**: CV 구조·개인정보·단방향 언어 관리와 신규 toolchain/minify 회귀 검사.
- 컴파일러 변경 전후 주요 11개 경로 × 2개 화면 폭 = **22개** 조건의
  본문·색상·글꼴·요소 위치 비교 통과. 허용 위치 오차는 0.5 CSS px.
- History 및 한·영 CV × 2개 화면 폭 × light/dark = **12개** 메뉴 비교 통과.
- 모바일 History/CV의 JavaScript 비활성 표시와 상세 펼침 검사 통과.
- 관리자 편집·추가·삭제·영문 수정본 보존·한글 역반영 금지·보안 필드 비노출 검증 통과.
- 실제 관리 화면의 177개 선택 항목, 354개 선택 체크박스, 가로 넘침 없음,
  무인증 저장 요청 403 확인.
- 현재 선택에 따른 한·영 PDF **12종 / 총 38페이지** 생성. 글꼴·유니코드·
  페이지 수·넘침·좌측 세로 이름 영역 검사 통과. 전체 페이지 썸네일과
  한·영 첫 페이지/연속 페이지를 렌더링해 확인했다.
- 임시 비공개 print data와 print HTML 경로가 생성 후 제거되었음을 확인했다.
- 루트 CI YAML을 파싱하고 로컬에서 동일한 공통 빌드 경로를 검증했다.
  GitHub Actions 원격 실행 성공을 확인한 것은 아니다.

### PDF 페이지 수

| 종류 | 한글 | 영문 |
| --- | ---: | ---: |
| Summary | 2 | 2 |
| Full | 6 | 8 |
| Art | 2 | 2 |
| Tec | 1 | 1 |
| Ref | 4 | 6 |
| Etc | 2 | 2 |

숫자는 이번 실행의 선택에 해당하며, 향후 이력·선택 변경 시 달라질 수 있다.
PDF는 `dist-local/private-pdf-site/about/`에만 저장되어 자동 공개되지 않는다.

## 남은 경고와 범위

Bootstrap **5.3.0-alpha1**과 이를 연결하는 `_bootstrap.scss`의 legacy import
경계에는 Sass의 import/global-builtin/color/if/abs-percent 관련 경고가 남아 있다.
이 경고를 숨기지 않았다. 기존 Bootstrap 버전을 유지해 화면 변화를 제한한다는
검토안에 따라 라이브러리 전체 업그레이드와 해당 경계의 완전한 Sass 모듈 이행은
별도 작업으로 남겼다. 따라서 Dart Sass 3.x까지의 호환성을 보장하는 결과는 아니다.

Hugo의 구형 `_internal`·페이지 `.Scratch` 호출은 활성 레이아웃에서 제거했다.
비활성 테마와 보관 자료를 경고만으로 삭제하지 않았다. `.OLD`, 기존 콘텐츠,
Obsidian 비공개 원본 및 사용자 공개/PDF 선택은 변경하지 않았다.

## 운영 안내와 복구 자료

- `docs/hugo-toolchain.md`: 버전 고정, Windows 설치, 공통 빌드, vendor 재적용 안내.
- `.local/README.md`: 기존 관리자·PDF 안내에 새 빌드 환경 설명 추가.
- `.build/modernization/recovery/`: 이번 변경 직전 소스 복구 사본(ignored).
- `.build/modernization/pdf-before/`: 기존 로컬 PDF 복구 사본(ignored).
- `.build/modernization/baseline/`: 변경 전 사이트 기준선(ignored).
- `.build/hugo-logs/`: 실행별 INFO 로그 및 deprecation 목록(ignored).
- `dist-local/qa/hugo-migration.json`: 22개 화면 비교 결과(ignored).
- `dist-local/pdf-preview/validation.json`: PDF 12종 검증 결과(ignored).

현재 로컬 미리보기 출력 `.build/review-site/`도 새 도구·구조로 갱신했다.
