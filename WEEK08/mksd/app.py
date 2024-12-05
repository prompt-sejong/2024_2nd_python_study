import streamlit as st       # streamlit run <file_name> 으로 실행
from node import *           # streamlit run WEEK08/mksd/app.py

st.title('서울 지하철 길찾기 앱')

stations = sorted({item[2] for item in list_df})

current_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(current_dir, "subway.jpg")



# 출발역과 도착역 입력
start_station = st.selectbox("출발역을 입력하세요:",options=stations)
end_station = st.selectbox("도착역을 입력하세요:", options=stations)

# 결과 버튼
if st.button("노선 찾기"):
    st.write("")
    if start_station and end_station:
        # 다익스트라 알고리즘 실행
        station_count, route = count_dijkstra(start_station, end_station)

        if route == -1:
            if station_count == -3:
                st.write("### 출발역과 도착역의 이름이 잘못되었습니다. ")
            elif station_count == -2:
                st.write("### 도착역의 이름이 잘못되었습니다. ")
            else:
                st.write("### 출발역의 이름이 잘못되었습니다. ")
        elif station_count == 0:
            st.write(f"### 출발역과 도착역이 같습니다.")
        else:
            # 결과 출력
            st.write("### 경로 정보")
            st.write(f"1. 걸리는 역의 개수: **{station_count}개**")         # 환승역말고만 호선 넣기?
            st.write(f"2. 경로: ")
            st.write(f"{route}")
    else:
        st.warning("출발역과 도착역을 모두 입력해주세요.")

st.image(
    image_path,  
    caption="지하철 노선도"
)