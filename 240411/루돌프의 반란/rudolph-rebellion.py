dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 입력
N, M, P, C, D = map(int, input().split())
Rr, Rc = map(int, input().split())

# 산타 위치와 상태, 점수 입력
santa = [[] for _ in range(P)]
for p in range(P):
    Pn, Sr, Sc = map(int, input().split())
    santa[Pn-1] = [Sr, Sc, 1, 0]

# 충돌 시 수행할 함수
def conflict(RorS):
    for Pn, S in enumerate(santa):
        if S[0] == Rr and S[1] == Rc:
            if RorS == 'R':
                santa[Pn][0] += r * C
                santa[Pn][1] += c * C
                if santa[Pn][0] <= 0 or santa[Pn][0] > N or santa[Pn][1] <= 0 or santa[Pn][1] > N:
                    santa[Pn][2] = -1
                else:
                    santa[Pn][2] = 0
                santa[Pn][3] += C        
            else:
                santa[Pn][0] -= r * D
                santa[Pn][1] -= c * D
                if santa[Pn][0] <= 0 or santa[Pn][0] > N or santa[Pn][1] <= 0 or santa[Pn][1] > N:
                    santa[Pn][2] = -1
                else:
                    santa[Pn][2] = 0
                santa[Pn][3] += D

            # 상호작용 검사
            interaction(santa[Pn][0], santa[Pn][1], Pn, RorS)

# 상호작용 함수
def interaction(x, y, Pn, RorS):
    for Pnn, Sn in enumerate(santa):
        if Pn != Pnn and Sn[0] == x and Sn[1] == y:
            if RorS == 'R':
                santa[Pnn][0] += r
                santa[Pnn][1] += c
            else:
                santa[Pnn][0] -= r
                santa[Pnn][1] -= c
            if santa[Pnn][0] <= 0 or santa[Pnn][0] > N or santa[Pnn][1] <= 0 or santa[Pnn][1] > N:
                santa[Pnn][2] = -1
                break
            interaction(santa[Pnn][0], santa[Pnn][1], Pnn, RorS)

# 명령어 입력
while M > 0:
    # 산타의 위치와 루돌프 위치 비교
    object = (-1, int(1e9))
    for Pn, S in enumerate(santa):
        # 탈락 상태면 continue
        if S[2] == -1:
            continue
        elif S[2] == 0:
            santa[Pn][2] = '0'
        elif S[2] == '0':
            santa[Pn][2] = 1
        
        # 거리 비교
        distance = (Rr - S[0]) ** 2 + (Rc - S[1]) **2
        if distance < object[1]:
            object = (Pn, distance)
        elif distance == object[1]:
            if santa[object[0]][0] < S[0]:
                object = (Pn, distance)
            elif santa[object[0]][0] == S[0]:
                if santa[object[0]][1] < S[1]:
                    object = (Pn, distance)
    
    # 목표 산타를 향한 루돌프의 움직임(세로 방향)
    r = 0
    if Rr < santa[object[0]][0]:
        Rr += 1
        r = 1
    elif Rr > santa[object[0]][0]:
        Rr -= 1
        r = -1
    
    # 목표 산타를 향한 루돌프의 움직임(가로 방향)
    c = 0
    if Rc < santa[object[0]][1]:
        Rc += 1
        c = 1
    elif Rc > santa[object[0]][1]:
        Rc -= 1
        c = -1

    # 충돌 검사. 충돌했을 경우 산타의 위치 수정과 함께 상태 갱신.
    conflict('R')

    # 1부터 P까지의 산타 위치 수정
    for Pn, S in enumerate(santa):
        if S[2] in [0, -1, '0']:
            continue

        distance = (S[0] - Rr) ** 2 + (S[1] - Rc) ** 2
        x, y = S[0], S[1]
        for k in range(4):
            d = (S[0] + dx[k] - Rr) ** 2 + (S[1] + dy[k] - Rc) ** 2
            if distance > d:
                # 가려는 위치에 산타가 있는지?
                for_break = False
                for Pnn, Sn in enumerate(santa):
                    if Sn[0] == S[0] + dx[k] and Sn[1] == S[1] + dy[k]:
                        for_break = True
                        break

                # 없다면?
                if not for_break:
                    distance = d
                    x = S[0] + dx[k]
                    y = S[1] + dy[k]
                    r = dx[k]
                    c = dy[k]
        santa[Pn][0] = x
        santa[Pn][1] = y

        # 산타 위치 수정될 때마다 충돌검사.
        conflict('S')

    M -= 1
    for_break = False
    for S in santa:
        if S[2] != -1:
            for_break = True
            break
    
    if not for_break:
        break

    for Pn, S in enumerate(santa):
        if S[2] != -1:
            santa[Pn][3] += 1

for S in santa:
    print(S[3], end=' ')