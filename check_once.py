import subprocess

threshold = 85
partition = ["/", "/opt", "/var/lib/backuppc2"]
HOST = ["backup-01.sitesuite.net", "db-01a.sitesuite.net"]
COMMAND = "sudo df -h"


def check_once():
    # df = subprocess.Popen(["df", "-h"], stdout=subprocess.PIPE)
    for thisHost in HOST:
        df = subprocess.Popen(["ssh", "%s" % thisHost, COMMAND],
                          shell=False,
                          stdout=subprocess.PIPE)
        for line in df.stdout:
            splitline = line.decode().split()
            if splitline[5] in partition and splitline[0] != "rootfs":
                if int(splitline[4][:-1]) > threshold:
                    # print(splitline[5])
                    # print(int(splitline[4][:-1]))
                    print(thisHost)
                    print("Partition {} is at {}%".format(str(splitline[5]), str(splitline[4][:-1])))
                    print()


if __name__ == "__main__":
    check_once()