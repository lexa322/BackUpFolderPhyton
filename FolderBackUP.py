#!/usr/bin/python

import time
import smtplib
import tarfile
import socket
import os
import fnmatch
import datetime
from datetime import datetime

FOLDER_FSALE = ""
FOLDER_BACKUP=""
NAME_BACKUP=""
NAME_FOLDER_FSALE=""
HOSTNAME=socket.gethostname()

Date = datetime.strftime(datetime.now(), "%Y.%m.%d")

def createfolder():
    dirname = os.path.join(FOLDER_BACKUP, NAME_FOLDER_FSALE, HOSTNAME)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return(dirname)

def sendmail ():
    timecopy = runtar()
    fromaddr = "xxx"
    toaddr = "xxx"
    serv = "xxx"
    port = 25
    subj = "Copy folder in " + HOSTNAME
    msgtext = "Copy folder completed successfully!!!\nCopying took %s second" % timecopy
    msg = "From: %s\nTo: %s\nSubject: %s\n\n%s" % (fromaddr, toaddr, subj, msgtext)
    s = smtplib.SMTP(serv, port)
    s.login("xxx", "xxx")
    s.sendmail(fromaddr, toaddr, msg)
    s.quit()

def createtar():
    namecreatefolder = createfolder()
    tar = tarfile.open (namecreatefolder + "\\" + NAME_BACKUP + Date + ".tar.gz", "w:gz")
    tar.add (FOLDER_FSALE)
    tar.close()

def deletebackup(folder1):
    file_exclude = "*.tar.gz"
    days_old = 5
    sort_list = []
    date_now = datetime.now()
    print (date_now)
    for top, dirs, files in os.walk(folder1):
        for nm in files:
            if fnmatch.fnmatch(nm, file_exclude):
                sort_list.append(os.path.join(top, nm))
    for nm in sort_list:
        date_modify = datetime.fromtimestamp(os.path.getmtime(nm))
        days_diff = (date_now-date_modify).days
        if days_diff > days_old:
            os.remove(nm)

def runtar():
    starttime = time.time()
    createtar()
    deletebackup(FOLDER_BACKUP)
    finishtime = time.time()
    totaltime = round((finishtime - starttime), 0)

    return (totaltime)



def main():
    runtar()
    sendmail()

if __name__ == '__main__':
    main()

