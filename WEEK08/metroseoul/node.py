import numpy as np
import pandas as pd
import os

db_path = os.path.join(os.path.dirname(__file__), '실시간도착_역정보(20241110).xlsx')

# 데이터 불러오기
df = pd.read_excel(db_path)
s = df[df['STATN_NM'] == '서울']
print(s)