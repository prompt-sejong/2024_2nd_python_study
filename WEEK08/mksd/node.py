import numpy as np
import pandas as pd
import os
import heapq

db_path = os.path.join(os.path.dirname(__file__), '실시간도착_역정보(20241110).xlsx')
INF = int(1e9)

# 데이터 불러오기
df = pd.read_excel(db_path)
df['STATN_ID'] = df['STATN_ID'].replace(',', '').astype(int)
list_df = df.values.tolist()    # [서브웨이ID, 역ID, 역이름, 호선]  -> 나중역ID-이전역ID = 이동거리





def dijkstra(name,destination):
    num = next((i for i, value in enumerate(list_df) if value[2] == name),-1)
    dest = next((i for i, value in enumerate(list_df) if value[2] == destination),-1)
    d[num] = 0
    pq = []
    heapq.heappush(pq,(0,num))
    while(len(pq)):
        dis = pq[0][0]       # 거리
        current = pq[0][1]   # 역
        heapq.heappop(pq)   # 값 삭제
        # 최단거리 아닌 경우 스킵
        if d[current] < dis:    continue
        for i in range(0,len(edge[current]),1):
            next_dis = dis+edge[current][i][0]  # dis + next dis
            next_station = edge[current][i][1]          # next_station
            if next_dis < d[next_station]:
                d[next_station] = next_dis
                heapq.heappush(pq,(next_dis,next_station))  
    return d[dest]

def set_dis(line, str1, str2, dis, line2 = 0):     # 역 간의 거리 설정
    list1 = [i for i, value in enumerate(list_df) if value[2] == str1]  # 인덱스 정보들을 알려줌.
    list2 = [i for i, value in enumerate(list_df) if value[2] == str2]

    for i in list1:
        if list_df[i][3] == line:
            station1 = i
    if line2 == 0:
        for i in list2:
            if list_df[i][3] == line:
                station2 = i
    else:
        for i in list2:
            if list_df[i][3] == line2:
                station2 = i
    
    heapq.heappush(edge[station1],(dis, station2))
    heapq.heappush(edge[station2],(dis, station1))


# print(list_df)
# s = df[df['STATN_NM'] == '서울']

# 현재 위치 : X -> 도착 위치 : Y
d = [INF] * 691
edge = {}
for i in range(0,len(list_df),1):
    edge[i] = []

# 1호선 거리 연결
for i in range(0,61):   # 1호선1 (소요산~인천)
    set_dis('1호선',list_df[i][2], list_df[i+1][2], 1)
for i in range(62,64):   # 1호선2 (청산~연천)
    set_dis('1호선',list_df[i][2], list_df[i+1][2], 1)
for i in range(66,100):   # 1호선3 (가디~신창)
    set_dis('1호선',list_df[i][2], list_df[i+1][2], 1)
set_dis('1호선',"서동탄", "병점", 1)
set_dis('1호선',"광명", "금천구청", 1)
set_dis('1호선',"가산디지털단지", "구로", 1)
set_dis('1호선',"청산", "소요산", 1)

# 2호선 거리 연결
for i in range(102,144):   # 2호선1 (시청~충정로)
    set_dis('2호선',list_df[i][2], list_df[i+1][2], 1)
for i in range(145,148):   # 2호선2 (용답~신설동)
    set_dis('2호선',list_df[i][2], list_df[i+1][2], 1)
set_dis('2호선',"용답", "성수", 1)
for i in range(149,152):   # 2호선3 (도림천~까치산)
    set_dis('2호선',list_df[i][2], list_df[i+1][2], 1)
set_dis('2호선',"도림천", "신도림", 1)

# 3호선 거리 연결
for i in range(153,196):   # 3호선 (대화~오금)
    set_dis('3호선',list_df[i][2], list_df[i+1][2], 1)

# 4호선 거리 연결
for i in range(197,244):   # 4호선 (당고개~오이도)
    set_dis('4호선',list_df[i][2], list_df[i+1][2], 1)

# 5호선 거리 연결
for i in range(245,293):   # 5호선1 (방화~하남검단산)
    set_dis('5호선',list_df[i][2], list_df[i+1][2], 1)
for i in range(294,300):   # 5호선2 (둔촌동~마천)
    set_dis('5호선',list_df[i][2], list_df[i+1][2], 1)
set_dis('5호선',"둔촌동", "강동", 1)

# 6호선 거리 연결
for i in range(301,306):   # 6호선1 (응암순환(상선)~구산)
    set_dis('6호선',list_df[i][2], list_df[i+1][2], 1)
for i in range(307,339):   # 6호선2 (새절~신내)
    set_dis('6호선',list_df[i][2], list_df[i+1][2], 1)
set_dis('6호선',"구산", "응암순환(상선)", 1)
set_dis('6호선',"응암순환(상선)", "새절(신사)", 1)

# 7호선 거리 연결
for i in range(340,392):   # 7호선 (석남~장암)
    set_dis('7호선',list_df[i][2], list_df[i+1][2], 1)

# 8호선 거리 연결
for i in range(393,416):   # 8호선 (별내~모란)
    set_dis('8호선',list_df[i][2], list_df[i+1][2], 1)

# 9호선 거리 연결
for i in range(417,454):   # 9호선 (개화~중앙보훈병원)
    set_dis('9호선',list_df[i][2], list_df[i+1][2], 1)

# GTX-A 거리 연결
for i in range(455,458):   # GTX-A (수서~동탄)      -> 이걸 한 정거장으로 보아야하는 가
    set_dis('GTX-A',list_df[i][2], list_df[i+1][2], 1)

# 경의중앙선 거리 연결
for i in range(459,487):   # 경의중앙선1 (용산~지평)     
    set_dis('경의중앙선',list_df[i][2], list_df[i+1][2], 1)
for i in range(488,512):   # 경의중앙선2 (공덕~임진강)     
    set_dis('경의중앙선',list_df[i][2], list_df[i+1][2], 1)
set_dis('경의중앙선',"효창공원앞", "공덕", 1)
set_dis('경의중앙선',"효창공원앞", "용산", 1)
set_dis('경의중앙선',"신촌(경의중앙선)", "서울", 1)
set_dis('경의중앙선',"신촌(경의중앙선)", "가좌", 1)

# 공항철도 거리 연결
for i in range(516,526):   # 공항철도 (서울~인천공항2터미널)
    if i == 519:
        set_dis('공항철도',list_df[i][2], list_df[i+1][2], 2)   # 디지털미디어<->김포공항
    elif i == 522:
        set_dis('공항철도',list_df[i][2], list_df[i+1][2], 3)   # 검암<->운서
    else:
        set_dis('공항철도',list_df[i][2], list_df[i+1][2], 1)
set_dis('공항철도',"마곡나루", "디지털미디어시티", 1)
set_dis('공항철도',"마곡나루", "김포공항", 1)
set_dis('공항철도',"청라국제도시", "검암", 1)
set_dis('공항철도',"청라국제도시", "영종", 1)
set_dis('공항철도',"영종", "운서", 1)

# 경춘선 거리 연결
for i in range(530,554):   # 경춘선 (청량리~춘천)
    if i == 532:
        set_dis('경춘선',list_df[i][2], list_df[i+1][2], 2)     # 광운대 <-> 중랑
    else:
        set_dis('경춘선',list_df[i][2], list_df[i+1][2], 1)
set_dis('경춘선',"중랑", "상봉", 1)

# 수인분당선 거리 연결
for i in range(555,617):   # 수인분당선 (청량리~인천)
    set_dis('수인분당선',list_df[i][2], list_df[i+1][2], 1)

# 신분당선 거리 연결
for i in range(618,623):   # 신분당선 (신사~양재시민의숲)
    set_dis('신분당선',list_df[i][2], list_df[i+1][2], 1)
for i in range(623,633):   # 신분당선 (양재시민의숲~광교)
    set_dis('신분당선',list_df[i][2], list_df[i+1][2], 1)

# 신림선 거리 연결
for i in range(680,690):   # 신림선 (샛강~관악산)         # !!! 우이신설,서해,경강 미구현
    set_dis('신림선',list_df[i][2], list_df[i+1][2], 1)

# 다른 호선과 환승 가능한 역 업데이트
set_dis('1호선',"인천", "인천", 0, '수인분당선')
set_dis('1호선',"온수", "온수", 0, '7호선')
set_dis('1호선',"신도림", "신도림", 0, '2호선')
set_dis('1호선',"신길", "신길", 0, '5호선')
set_dis('1호선',"대방", "대방", 0, '신림선')
set_dis('1호선',"노량진", "노량진", 0, '9호선')
set_dis('1호선',"용산", "용산", 0, '경의중앙선')
set_dis('1호선',"서울", "서울", 0, '4호선')
set_dis('1호선',"서울", "서울", 0, '공항철도')
set_dis('1호선',"서울", "서울", 0, '경의중앙선')
set_dis('1호선',"시청", "시청", 0, '2호선')
set_dis('1호선',"서울", "서울", 0, '4호선')


print(dijkstra("대림","시청"))      # 실제 시간을 더 걸리나 역은 11->9로 줄어듦.
print(dijkstra("새절(신사)","구산"))      # 6호선 순환 양방향으로 설계해서 작게 나옴. (..)
print(dijkstra("검암","운서"))      # 공항철도
print(dijkstra("효창공원앞","공덕"))      # 환승 미구현
