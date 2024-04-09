from collections import deque

L, Q = map(int, input().split())

belt = deque([[] for _ in range(L)] )
t = 0
customer = dict()
for q in range(Q):
    command, *parameter = input().split()
    parameter[0] = int(parameter[0])
    if parameter[0] - t < L:
        for i in range((parameter[0] - t) % L):
            belt.appendleft(belt.pop())
            for k, v in list(customer.items()):
                print(k, belt)
                if k in belt[v[0]]:
                    j = 0
                    try:
                        while True:
                            belt[v[0]].remove(k)
                            j += 1
                            if v[1] - j <= 0:
                                break
                        customer.pop(k, None)
                    except:
                        customer[k] = [v[0], v[1] - j]
    else:
        for i in range((parameter[0] - t) % L):
            belt.appendleft(belt.pop())
        for b in belt:
            for p in b:
                customer[p][1] -= 1
                if customer[p][1] <= 0:
                    customer.pop(p, None)
    t = parameter[0]

    if command == '100':
        belt[int(parameter[1])].append(parameter[2])
        if parameter[2] in customer.keys():
            j = 0
            try:
                while True:
                    belt[customer[parameter[2]][0]].remove(parameter[2])
                    j += 1
                    if customer[parameter[2]][1] - j <= 0:
                        break
                customer.pop(parameter[2], None)
            except:
                customer[parameter[2]] = [int(parameter[1]), customer[parameter[2]][1] - j]
    elif command == '200':
        customer[parameter[2]] = [int(parameter[1]), int(parameter[3])]
        if parameter[2] in belt[int(parameter[1])]:
            j = 0
            try:
                while True:
                    belt[int(parameter[1])].remove(parameter[2])
                    j += 1
                    if int(parameter[3]) - j <= 0:
                        break
                customer.pop(parameter[2], None)
            except:
                customer[parameter[2]] = [int(parameter[1]), int(parameter[3]) - j]
    else:
        sushi = 0
        for b in belt:
            sushi += len(b)
        print(len(customer), sushi)