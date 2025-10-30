import pandas as pd

df = pd.read_excel('RSC201_DR_v0_250418 (002)_UM232H.xlsx', header=None)

print('Excel 파일 구조 분석:')
print('=' * 50)

# 6행 근처의 데이터를 확인하여 Name, Description, Meaning 열 위치 파악
for i in range(5, 20):
    if i < len(df):
        row_data = df.iloc[i]
        # NaN이 아닌 값들만 출력
        non_nan_values = [(j, val) for j, val in enumerate(row_data) if pd.notna(val)]
        if non_nan_values:
            print(f'Row {i}: {non_nan_values}')

print('\n=' * 50)
print('특정 셀 값 확인:')
print(f'df.iloc[6, 1]: {df.iloc[6, 1]}')  # Name
print(f'df.iloc[6, 2]: {df.iloc[6, 2]}')  # Description  
print(f'df.iloc[6, 4]: {df.iloc[6, 4]}')  # Meaning