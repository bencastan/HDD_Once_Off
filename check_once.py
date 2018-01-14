import subprocess

# Value to check for:: Panic indicates immediate attention required
alert = 90
warn = 85

# If you don't want all partitions reported on set to False
checkNorms = False
debug = False
urgents = []
warns = []
norms = []
CLUSTER = ".sitesuite.net"
AWS = ".external.prd.sitesuite.io"
HOST = ["db-01a" + CLUSTER, "db-01b" + CLUSTER, "backup-01" + CLUSTER, "nfs-01" + CLUSTER, "cpanel" + CLUSTER,
        "mfilter-a-0" + AWS, "mfilter-b-0" + AWS, "mda-a-0" + AWS, "webmail-a-0" + AWS, "webmail-b-0" + AWS]
COMMAND = "sudo df -h"


def dedupe(x):
    y = []
    for i in x:
        if i not in y:
            y.append(i)
    return y


def check_once():
    for thisHost in HOST:
        df = subprocess.Popen(["ssh", "%s" % thisHost, COMMAND],
                              shell=False,
                              stdout=subprocess.PIPE)
        for line in df.stdout:
            splitline = line.decode().split()
            if splitline[0] != "Filesystem":
                if warn <= float(splitline[4][:-1]) < alert:
                    warns.append(thisHost + ',' + splitline[5] + ',' + splitline[4][:-1])
                    if debug:
                        print("ALERT::Urgent atttention required")
                        print("Host: {}".format(thisHost))
                        print("Partition {} is at {}%".format(str(splitline[5]), str(splitline[4][:-1])))
                        print()

                if float(splitline[4][:-1]) >= alert:
                    urgents.append(thisHost + ',' + splitline[5] + ',' + splitline[4][:-1])
                    if debug:
                        print("WARN::Atttention required")
                        print("Host: {}".format(thisHost))
                        print("Partition {} is at {}%".format(str(splitline[5]), str(splitline[4][:-1])))
                        print()

                if checkNorms:
                    if float(splitline[4][:-1]) < warn:
                        norms.append(thisHost + ',' + splitline[5] + ',' + splitline[4][:-1])
                        if debug:
                            print("NORMS::Happy Days!!!")
                            print("Host: {}".format(thisHost))
                            print("Partition {} is at {}%".format(str(splitline[5]), str(splitline[4][:-1])))
                            print()

    print('Urgents:')
    print(dedupe(urgents))
    print('Warns:')
    print(dedupe(warns))
    if checkNorms:
        print("NORMS")
        print(dedupe(norms))


if __name__ == "__main__":
    check_once()
