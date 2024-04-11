dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 입력값
L, N, Q = map(int, input().split())

chess = [list(map(int, input().split())) for _ in range(L)]

knight = [[] for _ in range(N)]
sheild = [[] for _ in range(N)]
hp = [0] * N
state = [1] * N
damage = [0] * N
for i in range(N):
    npt = list(map(int, input().split()))
    knight[i] = [npt[0] - 1, npt[1] - 1]
    sheild[i] = [npt[2], npt[3]]
    hp[i] = npt[4]

# 기사들이 이동하는 함수 작성.
def fight(who, where, damage_direction, king):

    # 피해 계산(롤백할 때의 데미지 롤백)
    if who != king and damage_direction == -1:
        for x in range(sheild[who][0]):
            for y in range(sheild[who][1]):
                if (0 <= knight[who][0] + x < N and 0 <= knight[who][1] + y < N) and chess[knight[who][0] + x][knight[who][1] + y] == 1:
                    damage[who] += damage_direction

    knight[who][0] += dx[where]
    knight[who][1] += dy[where]

    if state[who] == 0:
        return

    # 이동한 위치에 벽이 있느냐?
    stt = 'commit'
    for x in range(sheild[who][0]):
        for y in range(sheild[who][1]):
            if knight[who][0] + x < 0 or knight[who][1] + y < 0 or knight[who][0] + x >= L or knight[who][1] + y >= L or chess[knight[who][0] + x][knight[who][1] + y] == 2:
                stt = 'roll_back'
    
    # 이동한 위치에 기사가 있느냐?
    idx = []
    if stt != 'roll_back':
        for x in range(sheild[who][0]):
            for y in range(sheild[who][1]):
                for k in range(N):
                    if who == k:
                        continue
                    for xx in range(sheild[k][0]):
                        for yy in range(sheild[k][1]):
                            if knight[who][0] + x == knight[k][0] + xx and knight[who][1] + y == knight[k][1] + yy:
                                idx.append(k)
                                if state[k] == 1:
                                    stt = 'interaction'
    
    # 피해 계산
    if stt != 'roll_back' and who != king and damage_direction == 1:
        for x in range(sheild[who][0]):
            for y in range(sheild[who][1]):
                if chess[knight[who][0] + x][knight[who][1] + y] == 1:
                    damage[who] += damage_direction

    # 상황에 따라 다음 명령문 입력.
    if stt == 'interaction':
        for i in idx:
            fight(i, where, damage_direction, king)
    elif stt == 'roll_back':
        fight(who, (where + 2) % 4, -1, king)
    else:
        return

# 명령문 실행
for i in range(Q):
    who, where = map(int, input().split())
    
    # who를 where 방향으로 이동시켜 본다.
    fight(who - 1, where, 1, who - 1)

    # hp보다 많은 데미지를 받았다면 사라짐 처리.
    for k in range(N):
        if damage[k] >= hp[k]:
            state[k] = 0

# 데미지 점수 합계.
result = 0
for k in range(N):
    if state[k] == 1:
        result += damage[k]

print(result)