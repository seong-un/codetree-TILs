from collections import deque

L, Q = map(int, input().split())

belt = deque([dict() for _ in range(L)] )
t = 0
customer = dict()
for q in range(Q):
    command, *parameter = input().split()
    parameter[0] = int(parameter[0])
    if parameter[0] - t < L:
        for i in range((parameter[0] - t) % L):
            belt.appendleft(belt.pop())
            for k, v in list(customer.items()):
                if k in belt[v[0]]:
                    if belt[v[0]][k] >= v[1]:
                        customer.pop(k, None)
                    else:
                        customer[k][1] -= belt[v[0]][k]
                    belt[v[0]].pop(k, None)
    else:
        for i in range((parameter[0] - t) % L):
            belt.appendleft(belt.pop())
        for d, b in enumerate(belt):
            for k, v in list(b.items()):
                if v >= customer[k]:
                    customer.pop(k, None)
                else:
                    customer[k] -= v
                belt[d].pop(k, None)
    t = parameter[0]

    if command == '100':
        if parameter[2] in belt[int(parameter[1])]:
            belt[int(parameter[1])][parameter[2]] += 1
        else:
            belt[int(parameter[1])][parameter[2]] = 1
        if parameter[2] in customer and int(parameter[1]) == customer[parameter[2]][0]:
            if customer[parameter[2]][1] > belt[int(parameter[1])][parameter[2]]:
                customer[parameter[2]][1] -= belt[int(parameter[1])][parameter[2]]
            else:
                customer.pop(parameter[2], None)
            belt[int(parameter[1])].pop(parameter[2], None)
    elif command == '200':
        customer[parameter[2]] = [int(parameter[1]), int(parameter[3])]
        if parameter[2] in belt[int(parameter[1])]:
            if customer[parameter[2]][1] > belt[int(parameter[1])][parameter[2]]:
                customer[parameter[2]][1] -= belt[int(parameter[1])][parameter[2]]
            else:
                customer.pop(parameter[2], None)
            belt[int(parameter[1])].pop(parameter[2], None)
    else:
        sushi = 0
        for b in belt:
            sushi += sum(b.values())
        print(len(customer), sushi)