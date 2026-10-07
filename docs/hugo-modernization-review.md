# Hugo 최신 버전 호환성 전수 조사 및 수정 검토안

작성일: 2026-10-07 (Asia/Seoul)  
상태: 검토안 — 구현 소스 변경 전

후속 실행: 승인 후 순차 적용 결과는 `docs/hugo-modernization-result.md`를 참조한다.
아래 내용은 구현 전 조사·계획의 기록이다.

## 결론

최신 공개 안정 버전은 **Hugo v0.167.0**이며, 로컬 실행 파일과 루트 GitHub
Actions의 고정 버전도 v0.167.0이다. 따라서 실행 파일 업그레이드보다 기존
테마의 폐기 예정 API·호환 호출·컴파일러 의존성을 정리하는 작업이 우선이다.
현재 빌드는 성공하며, 즉시 수정 없이는 빌드가 불가능한 상태는 아니다.
[Hugo 공식 릴리스](https://github.com/gohugoio/hugo/releases/tag/v0.167.0)

권고 순서는 ① 구형 호출과 페이지 상태 관리 정리 → ② Dart Sass 전환 →
③ 템플릿 디렉터리·홈 파일명 이행 → ④ 비활성 구성 정리이다.
Bootstrap 전체 교체나 비활성 파일 삭제를 동시에 진행하지 않는다.

## 조사 범위와 방법

프로젝트 루트 설정, 루트 CI, `scripts/`, `tests/`, `.local/`, `layouts/`,
`assets/`, archetype, 활성 `write-only` 테마, 비활성 `coming-soon` 테마,
테마에 동봉된 `_vendor`와 `.OLD`를 대상으로 파일 목록·패턴 검색과 호출 경로를 조사했다.
콘텐츠는 템플릿·shortcode 사용 여부 확인 대상으로 포함했다.

조사 목록은 `.build/hugo-audit/inventory.json`에 경로·분류·SHA-256·검색 신호의
행 번호로 저장했다. 이 파일에는 원문 코드·인증값·비공개 이력 내용을 복사하지 않았다.

| 분류 | 파일 수 | 확인 범위 |
| --- | ---: | --- |
| 활성 소스·검사·로컬 운영 파일 | 106 | Hugo 호출, 템플릿 API, 스타일 진입점, 버전·경로 의존성 |
| 콘텐츠·archetype 성격의 콘텐츠 경로 | 252 | shortcode·layout 연결 및 구형 API 패턴 |
| vendored 소스·설정 | 207 | 모듈 버전, mount, Hugo 요구사항, Sass 의존성 |
| 비활성 Coming Soon 테마 | 11 | 별도 설정·워크플로·템플릿 |
| `.OLD` 보관 파일 | 49 | 보관 구분 및 구형 호출 패턴; 현행 이행 대상에서 제외 |
| 루트 설정·패키지·안내 파일 | 7 | Hugo·의존성·Git 구성 |
| 합계 | **632** | 아래 제외 대상은 포함하지 않음 |

실행 스크립트는 Python 12개, JavaScript 모듈 7개, 로컬 PowerShell 2개를 확인했다.
이미지·동영상·글꼴 바이너리, 설치된 `node_modules`, 빌드 캐시·산출물,
`.git`, `.env`, Obsidian 비공개 원본은 코드 이행 조사 대상에서 제외했다.
이번 조사는 Hugo 호환성 조사이며 타사 라이브러리 전체 보안 감사는 아니다.

## 실제 확인한 빌드 결과

1. 일반 배포 환경 빌드 + INFO 로그 + 경로 경고 + 미사용 템플릿 + 실행 통계:
   종료 코드 **0**, 명시적인 deprecation 메시지 **0**, 미사용 경고 **22**.
2. 별도 `resourceDir`와 출력 폴더를 사용하는 추가 빌드: 종료 코드 **0**,
   명시적인 deprecation/WARN/ERROR 메시지 **0**. HTTP 캐시까지 모두 비운
   완전한 오프라인/온라인 재현 검사는 수행하지 않았다.
3. 현재 로컬 미리보기와 일반 조사 빌드 비교: 기존 검사 기준에서 About 밖의
   출력 차이 **0**. 공개 CV는 이 시점의 선택을 기준으로 이력 53, 저작 59,
   미디어 3개였다. 이 수치를 모든 이력의 고정 기대값으로 사용하지 않는다.
4. `sass` 실행 파일은 현재 로컬 PATH에서 발견되지 않았다. CI는 Dart Sass를
   설치하지만 테마의 Sass 호출에 `transpiler`를 지정하지 않는다.

로그: `.build/hugo-audit/build.log`, `.build/hugo-audit/cold-build.log`.
일반 산출물: `.build/hugo-audit/current/`.

경고가 없다고 모든 API가 현행인 것은 아니다. 예를 들어 `.Scratch`는 경고를
출력하지 않는 soft deprecation이다.
[Hugo 폐기 정책](https://gohugo.io/troubleshooting/deprecation/),
[PAGE.Scratch 공식 안내](https://gohugo.io/methods/page/scratch/)

## 수정 대상과 우선순위

| ID / 우선순위 | 위치·근거 | 제안 | 영향·검증 |
| --- | --- | --- | --- |
| H01 / 높음 | `themes/write-only/layouts/partials/head/_resources.html:3` — `css.Sass`에 transpiler 미지정 | `transpiler: dartsass`를 명시하고 로컬·CI에서 같은 검증된 Sass 버전을 사용 | 기본값 LibSass는 Hugo v0.153.0에서 폐기 예정으로 지정됨. 컴파일러 전환은 사이트 전체 인라인 CSS에 영향을 주므로 별도 단계에서 화면·스타일 검증 |
| H02 / 높음 | 활성 테마의 `_internal` 호출 **7곳** | `template "_internal/..."`를 현재 embedded partial 호출로 교체 | 페이지네이션, GA4, Schema 유지. HTML 구조·페이지 이동 링크·추적 코드 중복 확인 |
| H03 / 보통 | `taxonomy.html:19`, `term.html:9,12,17`의 페이지 `.Scratch` **4곳** | 표시용 임시 값은 지역 변수로 바꾸는 것을 권고. 실제 페이지 영속 상태가 필요하면 `.Store` 사용 | 분류 그룹·표시 제목 및 여러 출력 형식 간 동작 보존 |
| H04 / 보통 | 루트와 활성 테마의 `layouts/partials`, 활성 테마 `layouts/shortcodes`, `layouts/index.html` | `_partials`, `_shortcodes`, `home.html`로 이행 | 프로젝트 override와 테마를 함께 이행. About/CV·RSS·sitemap·shortcode·404의 lookup 확인 |
| H05 / 보통 | `themes/write-only/config.yaml:2`의 literal key `module.hugoVersion` | `module` 아래 `hugoVersion` 중첩 구조로 바로잡고 최소 검증 버전을 명시 | 선언 형식 오류와 버전 정책 정리. 루트에서도 검증 기준 v0.167.0을 명시하는 방안 권고 |
| H06 / 낮음 | vendored Bootstrap 모듈 YAML 및 icons 모듈 TOML의 `hugoVersion.extended` | 모듈 갱신/재-vendor 작업에서 폐기 설정을 제거하거나 프로젝트에서 관리하는 재현 가능한 패치로 기록 | 해당 설정은 v0.153.0에서 폐기 예정으로 지정됨. 일회성 vendor 파일 수정만 남기지 않음 |
| H07 / 낮음 | `themes/write-only/netlify.toml:6`의 Hugo 0.83.1 | 비활성 예제임을 명시하고 유지 시 검증 버전과 정렬 | 루트 GitHub Pages 빌드에는 직접 적용되지 않음. Netlify 배포를 새로 구성하지 않음 |
| H08 / 낮음 | `themes/coming-soon/.github/workflows/main.yml:23`의 0.119.0, `config.toml:2`의 `languageCode`, `_default/baseof.html`, `index.html` | 비활성 테마 유지 정책을 정한 뒤 별도 갱신. locale 설정과 현대 템플릿 구조로 이행 | 중첩 `.github/workflows`는 루트 Actions에서 실행되지 않음. 테마 전환 없이 현 사이트 유지 |
| H09 / 보통 | `scripts/build_cv_pdf.mjs`, `scripts/prepare_pdf.py`, 루트 `.github/workflows/hugo.yaml` | 공통 Hugo 버전 점검·deprecation 로그 수집·Sass 사전 점검 추가 | CLI 옵션 자체의 폐기 문제는 발견하지 못함. 일반 웹, CSL 재빌드, 임시 print mount의 환경 일관성 개선 |

H01 근거: [css.Sass 옵션 및 LibSass 폐기 안내](https://gohugo.io/functions/css/sass/).
H02·H04 근거: [새 템플릿 시스템](https://gohugo.io/templates/new-templatesystem-overview/),
[Embedded partial 호출](https://gohugo.io/templates/embedded/).
H05·H06 근거: [모듈 설정](https://gohugo.io/configuration/module/).
H08 근거: [언어 설정](https://gohugo.io/configuration/languages/).

### H02: 교체할 호출 7곳

- `themes/write-only/layouts/index.html:13`
- `themes/write-only/layouts/list.html:42`
- `themes/write-only/layouts/list-doc.html:40`
- `themes/write-only/layouts/list-post.html:69`
- `themes/write-only/layouts/list-repo.html:40`
- `themes/write-only/layouts/partials/head/_seo.html:2,5`

앞의 5곳은 `partial "pagination.html" .`, 뒤의 두 호출은 각각
`partial "google_analytics.html" .`, `partial "schema.html" .`로 이행한다.
공식 문서가 안내하는 현대 호출로 바꾸되 기존 출력의 기능은 유지한다.

### H01: Sass 이행 시 주의점

활성 테마는 `styles.scss`와 `_bootstrap.scss`에서 `@import`를 사용하고,
vendored Bootstrap은 **5.3.0-alpha1**이다. 테마 `package.json`의 Bootstrap
범위 `^5.1.3`과 실제 vendored 버전이 달라 설치 경로를 바꾸면 결과도 달라질 수 있다.

먼저 현재 Bootstrap 소스를 유지한 채 Dart Sass 컴파일 결과를 확인한다.
애플리케이션 소유 Sass의 `@use`/`@forward` 이행과 Bootstrap 버전 갱신은
별도 변경으로 나눈다. 의존성의 전역 변수·import 순서가 있으므로 전체 파일에
`@import` → `@use`를 기계적으로 치환하지 않는다. 타사 경고를 영구적으로 모두
숨기는 것을 완료 기준으로 삼지 않는다.
[Sass 공식 import 이행 안내](https://sass-lang.com/documentation/breaking-changes/import/)

## 유지할 기능과 오탐 방지

- `css.Sass` 함수 자체는 현행이다. 문제는 기본 LibSass 선택이다.
- `partial`, `partialCached`, `.IsPage`, 메뉴 항목의 `.URL`, `.Permalink`,
  `.Paginate`/`.Paginator`, `resources.GetRemote`와 `try`를 폐기 기능으로
  분류하지 않는다. 구형 문법처럼 보인다는 이유로 일괄 치환하지 않는다.
- 활성 다국어 설정은 이미 `locale`/`label`을 사용한다. 기본 사이트 언어를
  바꾸는 작업은 이번 호환성 정리 범위에 포함하지 않는다.
- `getJSON`, `getCSV`, `resources.ToCSS`, `.Site.IsServer`, `.Hugo`, `.IsNode`
  등의 후보를 활성/비활성 레이아웃에서 검색했으며 발견하지 못했다.
- `_funcs/get-page-images` 의존은 현재 embedded 구현에 연결되어 동작한다.
  공개 API로 교체 가능한지 검토할 수 있으나 이번 조사에서 폐기 판정하지 않는다.
- 미사용 경고 22건 중 `index.html`, `about/cv.html`, `gallery-unsplash.html`
  등은 같은 실행 통계에서 호출 기록이 확인됐다. 미사용 경고만으로 삭제하지 않는다.
  PDF partial과 `cv-print.html`은 일반 웹 빌드에 등장하지 않는 것이 정상이다.
- `.OLD`는 과거 자료로 유지한다. 비활성 Coming Soon 테마와 예제 CI를
  실제 배포 워크플로와 혼동하지 않는다.

## 구현 단계

### 1. 기준선 확보와 작은 API 변경

현재 작업 상태를 기준으로 URL·페이지 수·본문·언어·RSS·sitemap·About/CV
리소스와 대표 화면을 새로 기록한다. 기존 Git 작업과 이력 공개 선택을 보존한다.
H02·H03·H05를 우선 수정하고 기능·마크업 비교를 통과시킨다.

### 2. Dart Sass 전환

로컬과 CI의 Sass 버전을 정렬하고 H01을 적용한다. 캐시를 사용하지 않는
CSS 컴파일 검사를 별도로 수행한다. 외부 이미지 API를 불필요하게 재호출하지
않도록 HTTP 캐시와 CSS 컴파일 캐시를 구분한다.

CSS가 모든 페이지에 인라인으로 삽입되므로 기존의 HTML 바이트 완전 일치
검사만으로는 이 단계를 판정할 수 없다. 변경을 허용한 스타일 영역을 별도로
비교하고, 본문·URL·메타데이터·페이지네이션은 동일해야 한다. DOM 구조,
computed style과 화면 위치를 데스크톱/모바일에서 비교한다.

### 3. 템플릿 구조 이행

H04를 루트 override와 활성 테마에 함께 적용한다. 모든 템플릿·스크립트·검사·안내의
경로 참조를 검색해 갱신한다. 사용자 지정 layout 이름은 단순 파일명 변경에 앞서
front matter와 연결을 확인한다. 임시 PDF mount도 같은 lookup으로 검증한다.

### 4. 비활성 구성과 vendor 정리

H06·H07·H08은 활성 사이트 검증 후 별도 단계로 처리한다. `.gitmodules`에는
테마 선언이 있지만 현재 인덱스의 확인한 테마 파일은 일반 파일(mode 100644)로
추적되어 있다. 자동 submodule 갱신을 전제로 하지 않고 실제 저장소 관리 상태부터
정리한다. 타사 소스 갱신은 버전·재-vendor 절차·로컬 수정 보존을 명시한다.

### 5. 재발 방지

루트 CI와 로컬 PDF 실행에서 Hugo 버전·Sass 존재를 점검하고 INFO deprecation
로그를 보관한다. 단, 모든 WARN을 곧바로 실패시키면 현재 미사용 템플릿 경고까지
실패로 처리할 수 있으므로 deprecated API와 일반 진단을 구분한다.

## 완료 기준

| 영역 | 통과 조건 |
| --- | --- |
| 일반 사이트 | v0.167.0, 개발·배포 환경 빌드 성공; 중복 경로 없음 |
| 템플릿 | 대상 `_internal`·페이지 `.Scratch` 호출 제거, 현대 lookup 확인 |
| 스타일 | Dart Sass로 실제 컴파일 성공, 메뉴·글자색·간격·모바일 동작 보존 |
| 콘텐츠 | 기존 URL·본문·언어 전환·분류·페이지네이션 보존 |
| History/CV | 기존 검사 및 한글 기준/영문 단방향·수정본 보존 테스트 통과 |
| 관리자 | 모바일 편집·추가·삭제·공개/PDF 선택과 보안 필드 비노출 확인 |
| PDF | 현재 선택으로 한·영 12종 생성, 글꼴·넘침·페이지 수·좌측 세로 이름 검증 |
| CI | CSL 생성 전후 및 일반/PDF 빌드의 환경·버전 일관성 확인 |
| 공개 경계 | 임시 print 페이지와 비공개 데이터가 배포 산출물에 포함되지 않음 |

현행 28개 Python 테스트, `check_cv_language_editor.mjs`, `check_cv_manager.mjs`,
`check_about_browser.mjs`, `check_history_header.mjs`, `check_about.py`를 재사용한다.
추가 검사는 폐기 API 재등장, 현대 템플릿 lookup, Sass 실행 보장에 집중한다.
이번 검토 단계에서는 PDF 12종 재생성, CI 실행, 비활성 테마 단독 구동 및
Dart Sass 설치/전환을 수행하지 않았다.

## 이번 단계에서 변경한 것

이 검토 문서와 ignored 조사 산출물만 작성했다. 구현 코드·설정·원문 콘텐츠·
비공개 이력·공개 선택은 변경하지 않았다. 커밋·푸시·배포·타사 모듈 갱신도 하지 않았다.
