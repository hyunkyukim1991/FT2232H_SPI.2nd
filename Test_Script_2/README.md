# Test_Script_2 - 사용하지 않는 파일 보관소

## 📁 개요

이 폴더에는 FT2232H Register Controller 개발 과정에서 생성되었지만 현재 사용하지 않는 파일들이 보관되어 있습니다.

## 📋 파일 분류

### 🔬 분석 및 디버그 도구
- `analyze_all_meanings.py` - Excel Meaning 테이블 전체 분석 도구
- `check_excel_structure.py` - Excel 파일 구조 검증 도구
- `read_excel_debug.py` - Excel 읽기 디버깅 도구
- `test_overflow.py` - 오버플로우 테스트 도구

### 🏗️ 초기 개발 파일들
- `Excel_To_Tree.py` - 초기 Excel to Tree 변환기
- `Excel_To_Tree_FromUI.py` - UI 기반 Excel 변환기
- `create_json.py` - JSON 생성 도구

### 🖥️ 구형 GUI 파일들
- `ft2232h_spi_gui*` - 구형 SPI GUI 시스템 (7개 파일)
  - `ft2232h_spi_gui.py` - 메인 GUI 파일
  - `ft2232h_spi_gui.ui` - UI 디자인 파일
  - `ft2232h_spi_gui_simple.py` - 간단한 버전
  - `ft2232h_spi_gui_from_ui.py` - UI 기반 버전
  - 기타 관련 파일들

### 🌳 구형 Tree Viewer 파일들
- `register_tree_viewer*` - 구형 레지스터 트리 뷰어 (6개 파일)
  - `register_tree_viewer.ui` - 구형 UI 디자인
  - `register_tree_viewer_clean.ui` - 정리된 UI 버전
  - `register_tree_viewer.ui.old` - 백업 UI 파일
  - 관련 Python 파일들

### 🔄 백업 및 구형 컨트롤러
- `Register_Controller_backup.py` - 메인 컨트롤러 백업
- `register_controller_fixed*` - 수정된 컨트롤러 버전들
- `register_controller_ui.py` - 구형 UI 바인딩 파일

### 📊 구형 데이터 파일들
- `register_tree.json` - 구형 레지스터 트리 데이터
- `Sample.json` - 구형 샘플 JSON
- `RSC201_DR_v0_250418*` - 구형 RSC201 관련 파일들

## ⚠️ 주의사항

- 이 폴더의 파일들은 현재 프로젝트에서 사용되지 않습니다
- 참고용으로만 보관되며, 삭제해도 메인 애플리케이션에 영향 없습니다
- 일부 파일들은 개발 과정의 히스토리를 보여주는 교육적 가치가 있습니다

## 🗑️ 정리 권장

개발이 완전히 완료되고 안정화된 후에는 다음 파일들을 삭제할 수 있습니다:
- 모든 `ft2232h_spi_gui*` 파일들
- 모든 `register_tree_viewer*` 파일들  
- 백업 파일들 (`*_backup.py`, `*.old`)
- 테스트/디버그 도구들 (필요 시 보관)

## 📈 현재 활성 시스템

메인 디렉토리의 활성 파일들:
- `Register_Controller.py` - 메인 애플리케이션
- `register_controller.ui` - 현재 UI 파일
- `uint32_spinbox.py` - 커스텀 위젯
- `Sample.xlsx` - 샘플 데이터
- `README.md` - 프로젝트 문서