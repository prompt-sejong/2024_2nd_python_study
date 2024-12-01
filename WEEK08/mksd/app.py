import streamlit        # streamlit run <file_name> 으로 실행
from node import *

streamlit.title('서울 지하철 길찾기 앱')

# print(s)        # 여러번 실행됨
# print(type(s))

# 제목 및 설명 추가
streamlit.title('간단한 streamlit 예제')
streamlit.write('데이터 프레임을 아래에 표시합니다.')

# 데이터 프레임 표시
streamlit.write(s)

# 그래프 시각화
# streamlit.line_chart(s[0][4])

# 슬라이더 예제
값 = streamlit.slider('값을 선택하세요', 0, 10, 5)
streamlit.write('선택한 값:', 값)