import math
from matplotlib import pyplot as plt

def rvalue(t):
    r = 2 * math.cos((math.pi / 6) * (t - 1))
    return r


def q_values(n):
    rvalues = []
    qvalues = []
    q = 0
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            rvalues.append(rvalue(j))

        q = sum(rvalues) / i
        qvalues.append(q)
        print("t = %2d, \t Q%d(a) = %4.3f" % (i, i, q))
        rvalues.clear()
    return qvalues

def a_values(n):
    for t in range(1, n + 1):
        a = ((t-1) % 6) + 1
        print("t = %2d, \t A%d = %4.3f" % (t, t, a))



if __name__ == '__main__':
    qvalues = q_values(12)

    print("--------------------")

    a_values(12)

    print("--------------------")

    # limiting expecting reward Q*(a) for each action a E A as t --> inf
    limit = q_values(1000)
    plt.plot(limit)
    plt.show()
