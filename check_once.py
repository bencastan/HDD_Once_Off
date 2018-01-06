import subprocess

threshold = 20
partition = "/"


def check_once():
    df = subprocess.Popen(["df", "-h"], stdout=subprocess.PIPE)
    for line in df.stdout:
        splitline = line.decode().split()
        if splitline[5] == partition:
            if int(splitline[4][:-1]) > threshold:
                #print(splitline[5])
                #print(int(splitline[4][:-1]))
                print("Partition {} is at {}%".format(str(splitline[5]), str(splitline[4][:-1])))



check_once()