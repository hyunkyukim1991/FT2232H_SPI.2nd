import pandas as pd

df = pd.read_excel('RSC201_DR_v0_250418 (002)_UM232H.xlsx', header=None)

print('Excel 파일 전체 구조 분석:')
print('=' * 80)

# 전체 파일에서 "Meaning" 문자열이 있는 위치 찾기
meaning_positions = []
for row_idx in range(len(df)):
    for col_idx in range(len(df.columns)):
        cell_value = df.iat[row_idx, col_idx]
        if pd.notna(cell_value) and str(cell_value).strip() == "Meaning":
            meaning_positions.append((row_idx, col_idx))
            print(f"🔍 'Meaning' 발견: Row {row_idx}, Col {col_idx}")

print(f"\n총 {len(meaning_positions)}개의 Meaning 열 발견")

# 각 Meaning 열 주변의 데이터 확인
for i, (row_idx, col_idx) in enumerate(meaning_positions):
    print(f"\n=== Meaning 테이블 #{i+1} (Row {row_idx}, Col {col_idx}) ===")
    
    # 해당 행의 헤더 정보 확인
    header_row = df.iloc[row_idx]
    headers = []
    for j in range(max(0, col_idx-5), min(len(df.columns), col_idx+3)):
        if pd.notna(header_row.iloc[j]):
            headers.append(f"Col{j}: {header_row.iloc[j]}")
    print("헤더:", " | ".join(headers))
    
    # 다음 몇 행의 데이터 확인 (실제 데이터)
    for data_row_idx in range(row_idx + 1, min(row_idx + 8, len(df))):
        data_row = df.iloc[data_row_idx]
        # Name과 Meaning 열만 확인
        name_col = col_idx - 4  # Name은 보통 Meaning보다 4칸 앞
        if name_col >= 0:
            name_val = data_row.iloc[name_col] if name_col < len(data_row) else None
            meaning_val = data_row.iloc[col_idx] if col_idx < len(data_row) else None
            
            if pd.notna(name_val) or pd.notna(meaning_val):
                print(f"  Row {data_row_idx}: Name='{name_val}' | Meaning='{meaning_val}'")
        
        # 빈 행이거나 다른 테이블 시작하면 중단
        if pd.isna(data_row.iloc[name_col]) and pd.isna(data_row.iloc[col_idx]):
            break
        elif pd.notna(data_row.iloc[name_col]) and str(data_row.iloc[name_col]).strip() == "Name":
            print(f"  다음 테이블 시작 감지 at Row {data_row_idx}")
            break