import matplotlib.pyplot as plt

points = []

f1 = open("data", "r")
N = int(f1.readline())
for i in range(N):
    points.append([float(i) for i in f1.readline().split()])
f1.close()

hp = []

f1 = open("van_path", "r")
M = int(f1.readline())
for i in range(M):
    hp.append([float(i) for i in f1.readline().split()])
f1.close()

plt.scatter(
    [i[0] for i in points],
    [i[1] for i in points],
    s = 0.01,
    color="#aaaaaa",
    label="Unvaccinated user"
)

plt.plot(
    [i[0] for i in hp] + [hp[0][0]],
    [i[1] for i in hp] + [hp[0][1]],
    c = "#86bbd8",
    linewidth=2
)

plt.scatter(
    [i[0] for i in hp],
    [i[1] for i in hp],
    s = 25,
    color="#c92a2a",
    label="Hotspot (waypoint)",
)

plt.legend()
plt.axes().set_facecolor("#333333")
plt.show()