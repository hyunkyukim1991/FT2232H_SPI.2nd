import pandas as pd
import sys

try:
    df = pd.read_excel('RSC201_DR_v0_250418 (002)_UM232H.xlsx', header=None)
    print(f'Excel 파일 크기: {df.shape[0]}행 x {df.shape[1]}열')
    print()
    
    # 전체 데이터에서 Addr과 EN 관련 정보 찾기
    for row_idx in range(min(100, len(df))):
        for col_idx in range(min(20, len(df.columns))):
            cell = df.iloc[row_idx, col_idx]
            if isinstance(cell, str) and ('Addr' in cell or 'EN' in cell or '0x01' in cell):
                print(f'관련 데이터 발견: "{cell}" at Row {row_idx}, Col {col_idx}')
                
                # 주변 10행 정도의 데이터 출력
                print("주변 데이터:")
                for r in range(max(0, row_idx-3), min(len(df), row_idx+15)):
                    row_data = []
                    for c in range(max(0, col_idx), min(len(df.columns), col_idx+4)):
                        val = df.iloc[r, c]
                        if pd.isna(val):
                            val = ''
                        row_data.append(str(val)[:20])
                    print(f'  Row {r}: {row_data}')
                print("-" * 50)
                
except Exception as e:
    print(f'오류: {e}')
    import traceback
    traceback.print_exc()