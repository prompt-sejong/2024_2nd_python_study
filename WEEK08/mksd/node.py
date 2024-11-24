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





def dijkstra(name):
    num = int(name)
    cost_list[num] = 0
    pq = []
    heapq.heappush(pq,(0,name))
    while(pq):
        current = pq[0][1]   # 역
        dis = pq[0][0]       # 거리
        heapq.heappop(pq)   # 값 삭제
        # 최단거리 아닌 경우 스킵
        if cost_list[current] < dis:    continue
        for i in range(0,len(edge[current]),1):
            next = edge[current][i][1]
            next_dis = dis+edge[current][i][0]
            if next_dis < cost_list[next]:
                cost_list[next] = next_dis
                heapq.heappush(pq,(next_dis,next))  

def set_dis(line, str1, str2, dis):     # 역 간의 거리 설정
    list1 = [i for i, value in enumerate(list_df) if value[2] == str1]  # 인덱스 정보들을 알려줌.
    list2 = [i for i, value in enumerate(list_df) if value[2] == str2]

    for i in list1:
        if list_df[i] == line:
            station1 = i
    for i in list2:
        if list_df[i] == line:
            station2 = i
    heapq.heappush(edge[station1],())



# for i in range()

# 1~... 호선까지 처리


# print(list_df)
# s = df[df['STATN_NM'] == '서울']

# 현재 위치 : X -> 도착 위치 : Y
cost_list = [INF] * 691
edge = {}
for i in range(0,len(list_df),1):
    edge[i] = []
print(len(edge))

list1 = [i for i, value in enumerate(list_df) if value[2] == "신도림"]  # 0부터여서 -1, 맨 위에 태그 없애서 -1 -> 총 -2
# -> 인덱스 정보를 나타냄

print(list1)
print(list_df[40])

# print(dijkstra(0))