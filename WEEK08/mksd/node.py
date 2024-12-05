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
d = [INF] * 691
edge = {}

def init():
    global d
    d = [INF] * 691
    for i in range(0,len(list_df),1):
        edge[i] = []
    # 다른 호선과 환승 가능한 역 업데이트
    init_edge()
    trans()

def count_dijkstra(start,destination):
    init()      # 초기화
    num = next((i for i, value in enumerate(list_df) if value[2] == start),-1)
    dest = next((i for i, value in enumerate(list_df) if value[2] == destination),-1)

    if dest == -1 and num == -1:            # 사용자 실수 예외처리
        return (-3,-1)               # 출발, 도착역 이름 오류
    if dest == -1:                  
        return (-2,-1)               # 도착역 이름 오류
    if num == -1:
        return (-1,-1)               # 출발역 이름 오류
    if num == dest:                  # 출발역과 도착역이 같은 경우
        return 0, str(list_df[num])

    d, prev = dijkstra(num)
    # 경로 추적
    path = get_path(prev, dest)

     # 환승 경로 처리
    route = str()
    for i in range(len(path) - 1):
        current_station = list_df[path[i]]      # 인덱스에서 현재 역 이름으로 변경
        next_station = list_df[path[i + 1]]     # 다음 역 이름
        if not route:
            if current_station[2] != next_station[2]:
                route += (f"{current_station[2]}({next_station[3]}) -> ")
                continue
        if (current_station[2] != next_station[2]):  # 중복 방지
            route += (f"{current_station[2]}({current_station[3]}) -> ")  # 역(호선) 형식으로 추가        # 리스트로 할려면 route = [], route.append(~~)
            # ({current_station[3]}) : 호선인데 에러 많이 남. ({list_df[path[-1]][3]})
    if len(path) < 2: 
        route += (f"{list_df[path[-1]][2]}({list_df[path[-1]][3]})")  # 최종 도착역 추가

    route += (f"{list_df[path[-1]][2]}({list_df[path[-2]][3]})")  # 최종 도착역 추가

    return d[dest], route

def dijkstra(start_num):     # 다익스트라 start : 출발지 , destination : 도착지

    d[start_num] = 0
    pq = []
    heapq.heappush(pq,(0,start_num))
    prev = [-1] * 691  # 각 역의 이전 역 정보를 저장

    while(len(pq)):
        dis, current = heapq.heappop(pq)   # 거리, 역 

        # 최단거리 아닌 경우 스킵
        if d[current] < dis:    continue

        for next_dis, next_station in edge[current]:
            total_dis = dis+ next_dis          # dis + next dis
            if total_dis < d[next_station]:
                d[next_station] = total_dis
                prev[next_station] = current  # 이전 역 갱신
                heapq.heappush(pq,(total_dis,next_station))  

    return d, prev

def get_path(prev, dest):
    path = []
    while dest != -1:
        path.append(dest)
        dest = prev[dest]
    path.reverse()
    return path

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

# 역 간의 거리 업데이트 (환승 미포함)
def init_edge():    
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
    set_dis('6호선',"응암순환(상선)", "새절(신사)", 1)

    # 구산 -> 응암 거리 1 추가 (양방향 추가 X)
    list1 = [i for i, value in enumerate(list_df) if value[2] == "구산"]
    list2 = [i for i, value in enumerate(list_df) if value[2] == "응암순환(상선)"]
    for i in list1:
        if list_df[i][3] == '6호선':
            station1 = i
    for i in list2:
        if list_df[i][3] == '6호선':
            station2 = i
    heapq.heappush(edge[station1],(1, station2))    # 구산 -> 응암 거리 1 추가 (양방향 추가 X)

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
    for i in range(680,690):   # 신림선 (샛강~관악산)      
        set_dis('신림선',list_df[i][2], list_df[i+1][2], 1)

    # 우이신설선 거리 연결
    for i in range(646,658):   # 우이신설선 (북한산우이~신설동)
        set_dis('우이신설선',list_df[i][2], list_df[i+1][2], 1)
    
    # 서해선 거리 연결
    for i in range(659,679):   # 서해선 (일산~원시)
        set_dis('서해선',list_df[i][2], list_df[i+1][2], 1)

    # 경강선 거리 연결
    for i in range(634,645):   # 경강선 (판교~여주)
        set_dis('경강선',list_df[i][2], list_df[i+1][2], 1)

# 환승 업데이트 거리 0
def trans():        
    for n in range(0,690):   # 모든 역
        list1 = [i for i, value in enumerate(list_df) if value[2] == list_df[n][2]]
        if(len(list1) > 1):  # 모든 호선을 서로 연결
            for i in range(len(list1)):
                for j in range(i + 1, len(list1)):
                    set_dis(list_df[list1[i]][3], list_df[list1[i]][2], list_df[list1[i]][2], 0, list_df[list1[j]][3])


# print(count_dijkstra("대림","시청"))      # 9
# print(count_dijkstra("새절(신사)","구산")) # 6 단방향 체크
# print(count_dijkstra("검암","운서"))      # 3 (공항철도)
# print(count_dijkstra("효창공원앞","공덕")) # 1 (경로 에러)
# print(count_dijkstra("용산","공덕")) # 2
# print(count_dijkstra("구로","샛강"))      # 5
# print(count_dijkstra("구로","영등포구청")) # 3
# print(count_dijkstra("구로","이촌"))      # 7
# print(count_dijkstra("구로","대흥(서강대앞)"))      # 8
# print(count_dijkstra("대방","노들"))      # 2
# print(count_dijkstra("종각","동대문역사문화공원"))      # 2
# print(count_dijkstra("신원","잠실나루"))      # 16
# print(count_dijkstra("원시","월드컵경기장(성산)"))      # 17

# 호선만 미추가