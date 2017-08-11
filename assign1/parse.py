import re

pattern = re.compile(r"Regret\s(\d+)\s=\s(.*)\s")
num_arms = "25"
algorithm = ["rr", "epsilon-greedy", "UCB", "KL-UCB", "Thompson-Sampling"]
indices = [10, 20, 30, 40, 50, 60, 70, 80, 90,
           100, 200, 300, 400, 500, 600, 700, 800, 900,
           1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
           10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000,
           100000]

for algo in algorithm:
    points = {k: 0.0 for k in indices}
    for i in range(100):
        job_str = num_arms + "_" + algo + "_" + str(i) + ".txt"
        print job_str
        with open("server/" + job_str, 'r') as f:
            data = f.read()
        matches = pattern.findall(data)
        for index in indices:
            if int(matches[index - 1][0]) != index:
                print "Error!"
            points[index] += float(matches[index - 1][1])
    output = ""
    for k in sorted(points.iterkeys()):
        output += str(k) + "," + str(points[k] / 100.0) + "\n"
    with open("client/report/arms_" + num_arms + "_" + algo + ".log", 'w') as f:
        f.write(output)
