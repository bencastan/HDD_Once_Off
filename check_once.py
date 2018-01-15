import subprocess
import email.message
import email.policy
import email.utils
import sys


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


def print_header():
    print('------------------------------------')
    print('     HDD Partition Checker')
    print('------------------------------------')
    print()


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
    return urgents, warns, norms


def build_text(urgs, warn, norm):
    message = "URGENT: \n"
    message = "{0}{1}".format(message, ('\n'.join(map(str, urgs))))
    message = "{0}{1}".format(message,("\nWARN:\n"))
    message = "{0}{1}".format(message, ('\n'.join(map(str, warn))))
    message = "{0}{1}".format(message, ("\nNORM:\n"))
    message = "{0}{1}".format(message, ('\n'.join(map(str, norm))))

    return message


def send_emails(text):

    # Foundations of Python network Programming, Third Edition
    # https://github.com/brandon-rhodes/fonp/bvlob/m/py3/chapter12/build_bhasic_email.py


    # text = """Hello,
    # This is a basic message from Chapter 12.
    # - Anonymous"""

    message = email.message.EmailMessage(email.policy.SMTP)
    message['To'] = 'recipient@example.com'
    message['From'] = 'Test Sender <sender@example.com>'
    message['Subject'] = 'Test Message, Chapter 12'
    message['Date'] = email.utils.formatdate(localtime=True)
    message['Message-ID'] = email.utils.make_msgid()
    message.set_content(text)
    sys.stdout.buffer.write(message.as_bytes())


if __name__ == "__main__":
    print_header()
    results = check_once()
    #print('Urgents:')
    urgents = (dedupe(urgents))
    #print('Warns:')
    warns = (dedupe(warns))
    if checkNorms:
        #print("NORMS")
        norms = (dedupe(norms))
    text = build_text(urgents, warns, norms)
    send_emails(text)