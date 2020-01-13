#-*- coding: latin_1 -*-
# Python library for Brugis deploy

import os
import sys
import datetime
import time
import tarfile
import shutil
import sqlite3
import socket
from xml.etree import ElementTree
import psycopg2

def stopService(serviceName):
    print(os.name)
    if os.name != "nt":
        #Linux
        return stopLinuxService(serviceName)      
    else:
        #Windows
        return stopWinService(serviceName)

def startService(serviceName):
    print(os.name)
    if os.name != "nt":
        return startLinuxService(serviceName)
    else:
        return startWinService(serviceName)

def startLinuxService(serviceName):
    from subprocess import call
    return_code = call(["systemctl","start",serviceName])
    return return_code == 0

def stopLinuxService(serviceName):
    from subprocess import call
    return_code = call(["systemctl","stop",serviceName])
    return return_code == 0

################################################################################
def stopWinService(serviceName):
    '''
    '''
    import win32serviceutil
    import win32service
    serviceStatus = win32serviceutil.QueryServiceStatus(serviceName)[1]
    #print serviceStatus
    statusListToStop = [win32service.SERVICE_RUNNING,
                        win32service.SERVICE_START,
                        win32service.SERVICE_START_PENDING]
    #print statusListToStop
    #print serviceStatus in statusListToStop
    if serviceStatus in statusListToStop:
        print "Service %s started, stopping it..." % serviceName
        returnCode = win32serviceutil.StopService(serviceName)
        elapsed = 0
        while not win32serviceutil.QueryServiceStatus(serviceName)[1] == 1 and elapsed < 120:
            print "Service %s stopping... Please wait while it stops." % serviceName
            time.sleep(3)
            elapsed += 3
        if not win32serviceutil.QueryServiceStatus(serviceName)[1] in [1, 3]:
            print "Service %s can't be stopped. Please stop it manually and re-execute this script." % serviceName
            return False
        else:
            print "Service stopped in %s seconds" % elapsed
            #time.sleep(15)
            return True
    elif serviceStatus in [1, 3] :
        print "Service %s already stopped" % serviceName
        return True
    else:
        print "Service %s has status %s" % (serviceName, win32serviceutil.QueryServiceStatus(serviceName)[1])
        return False

def startWinService(serviceName):
    '''
    '''
    import win32serviceutil
    import win32service
    returnCode = win32serviceutil.StartService(serviceName)
    if win32serviceutil.QueryServiceStatus(serviceName)[1] == win32service.SERVICE_START_PENDING:
        print "Service %s starting..." % serviceName
        return True
    else:
        print "Service %s can't be started. Please start it manually." % serviceName
        return False

 
def chmodAll(rootDirPath):
    '''
    '''
    os.chmod(rootDirPath, 0o777)
    for (root, dirs, files) in os.walk(rootDirPath):
        for file in files:
            try:
                os.chmod(os.path.join(root, file), 0o666)
            except:
                print "%s could not be chmodded to RW for everyone" % file
        for dir in dirs:
            try:
                os.chmod(os.path.join(root, dir), 0o777)
            except:
                print "%s could not be chmodded to RW for everyone" % dir

def deployFile(ftpRepositoryDirectoryPath, fileNameIn, fileNameOut, destinationDirectoryPath, backupDirectoryPath = ''):
    '''
    '''
    if backupDirectoryPath == '':
        backupDirectoryPath = destinationDirectoryPath
    if not os.path.isdir(backupDirectoryPath):
        print "creation of %s" % backupDirectoryPath
        os.mkdir(backupDirectoryPath)
    try:
        # Migration of file if present
        if os.path.isdir(ftpRepositoryDirectoryPath) and os.path.exists(os.path.join(ftpRepositoryDirectoryPath, fileNameIn)):
            print "file %s to deploy..." % fileNameIn
            if os.path.isdir(destinationDirectoryPath):
                # creation of a backup of the existing file if existing
                if os.path.exists(os.path.join(destinationDirectoryPath, fileNameOut)):
                    fileExtension = os.path.splitext(fileNameOut)[1]
                    newName = fileNameOut.replace(fileExtension, fileExtension + ".%4i%02i%02i-%02i_%02i_%02i.old" % (datetime.date.today().year,
                                                                                               datetime.date.today().month,
                                                                                               datetime.date.today().day,
                                                                                               datetime.datetime.now().hour,
                                                                                               datetime.datetime.now().minute,
                                                                                               datetime.datetime.now().second))
                    print "Backup of old %s as %s" % (fileNameOut, newName)
                    shutil.move(os.path.join(destinationDirectoryPath, fileNameOut), os.path.join(backupDirectoryPath, newName))
                    #time.sleep(15)
                # copy of the new file from the ftp repository to its place
                print "Moving new %s into %s" % (fileNameOut, destinationDirectoryPath)
                shutil.move(os.path.join(ftpRepositoryDirectoryPath, fileNameIn),os.path.join(destinationDirectoryPath, fileNameOut))
                # Erasing of deployed war present in Tomcat webapps directory
                dirToDelete = os.path.join(destinationDirectoryPath, os.path.splitext(fileNameOut)[0])
                if os.path.isdir(dirToDelete):
                    print "erasing folder %s" % dirToDelete
                    shutil.rmtree(dirToDelete)
            else:
                print "no %s valid" % destinationDirectoryPath
        else:
            print "no path %s or file %s" % (ftpRepositoryDirectoryPath, fileNameIn)
    except Exception, e:
        print e

def untarData_dir(data_dirTarFile, diskDriveLetter = None, removeTarFile = True):
    '''
    '''
    if not diskDriveLetter:
        diskDriveLetter = os.path.splitdrive(data_dirTarFile)[0]
    try:
        print "Untaring %s..." % data_dirTarFile
        if os.path.exists(data_dirTarFile) and tarfile.is_tarfile(data_dirTarFile):
            with tarfile.open(data_dirTarFile, 'r', encoding='iso-8859-1') as tarFile:
                updated = []
                for m in tarFile.getmembers():
                    m.name = unicode(m.name, 'iso-8859-1')
                    updated.append(m)
                #print "before untaring"
                tarFile.extractall(diskDriveLetter,members=updated)
                #print "after untaring"
            if removeTarFile:
                os.remove(data_dirTarFile)
        else:
            print "%s is not a tar file or does not exists" % data_dirTarFile
            time.sleep(15)
        print "Untar finished."
    except Exception, e:
        print e

def deployData_dir(newData_dirPath, oldData_dirPath, gwcDirName, gwcBlobDirName, dataName, dataContentToKeep = [], dataDirMigrationScriptName = None):
    '''
    '''
    # Migration of data_dir if present
    if os.path.isdir(newData_dirPath):
        if os.path.isdir(oldData_dirPath):
            # creation of a backup of the existing data_dir if existing
            bkpName = oldData_dirPath + "_old_%4i%02i%02i_%02i_%02i_%02i" % (datetime.date.today().year,
                                                                            datetime.date.today().month,
                                                                            datetime.date.today().day,
                                                                            datetime.datetime.now().hour,
                                                                            datetime.datetime.now().minute,
                                                                            datetime.datetime.now().second)
            print "Backup of old %s as %s" % (oldData_dirPath, bkpName)
            # On va créer le dossier de backup, et copier dedans dossier par dossier,
            # sauf le geowebcache, en ne chmodant que ce que l'on copie
            os.mkdir(bkpName)
            currentDataDirPath = oldData_dirPath
            currentDataDirContent = os.listdir(oldData_dirPath)
            currentDataDirContent.remove(gwcDirName)
            currentDataDirContent.remove(gwcBlobDirName)
            for each in currentDataDirContent:
                elementToCopy = os.path.join(oldData_dirPath,each)
                #print "in for for %s" % elementToCopy
                if os.path.isdir(elementToCopy):
                    #print "in if for %s" % elementToCopy
                    chmodAll(elementToCopy)
                else:
                    #print "in else for %s" %  elementToCopy
                    os.chmod(os.path.join(elementToCopy), 0o666)
                #time.sleep(2)
                #print "before remane for %s" % elementToCopy
                shutil.move(elementToCopy, os.path.join(bkpName, each))
                #print "after remane for %s" % os.path.join(bkpName,each)
            #gwcContent = os.listdir(os.path.join(bkpName,gwcDirName))
        else:
            #TODO create a new data_dir empty?
            print ''

        # copy of the new data_dir from the ftp repository to its place
        chmodAll(newData_dirPath)
        print "Moving new %s into %s" % (newData_dirPath, oldData_dirPath)
        newDataDirContent = os.listdir(newData_dirPath)
        for each in newDataDirContent:
            elementToCopy       = os.path.join(newData_dirPath,each)
            elementToCopyNew    = os.path.join(oldData_dirPath,each)
            if not each in os.listdir(oldData_dirPath):
                shutil.move(elementToCopy, elementToCopyNew)
            else:
                print "Already there: %s" % each
                # print "gwcDirName: %s" % gwcDirName
                # print each == gwcDirName
                # special case for gwc folder that still need to have stuff copied in
                if each == gwcDirName:
                    gwcElementsToCopy  = os.listdir(elementToCopy)
                    gwcElementsPresent = os.listdir(elementToCopyNew)
                    for each2 in gwcElementsToCopy:
                        if os.path.isfile(os.path.join(elementToCopy, each2)):
                            if each2 in gwcElementsPresent:
                                print "overwriting %s" % each2
                                os.remove(os.path.join(elementToCopyNew, each2))
                            else:
                                print "writing %s" % each2
                            shutil.move(os.path.join(elementToCopy, each2), os.path.join(elementToCopyNew, each2))

        for each in dataContentToKeep:
            print "keeping %s from backup..." % each
            eachInBackupPath     = os.path.join(os.path.join(bkpName, dataName), each)
            eachInDataDirPath    = os.path.join(os.path.join(oldData_dirPath, dataName), each)
            if os.path.exists(eachInBackupPath) and not os.path.exists(eachInDataDirPath):
                shutil.copytree(eachInBackupPath, eachInDataDirPath)

        # Cleaning of the FTP_root/MyBruGIS transfer/data_dir directory
        print "removing %s" % newData_dirPath
        shutil.rmtree(newData_dirPath)
        # migrate and adapt the content of the data_dir to the different environments( dev, staging or production)
        # DOCG TODO:
        # to suppress and add in this library the content of the python script and call this method from de main Deploy script
        if dataDirMigrationScriptName:
            print "Migrating the data_dir..."
            execfile(dataDirMigrationScriptName)
            print "Migration finished."
    else:
        print '%s is not a directory' % newData_dirPath

def deleteOldData_dirBackups(data_dirDirectoryPath, numberOfData_dirBackupsToKeep):
    '''
    '''
    #print data_dirDirectoryPath
    #print numberOfData_dirBackupsToKeep
    oldData_dirBackupsFolders = []
    for dir in os.listdir(data_dirDirectoryPath):
        if 'data_dir_old' in dir:
            oldData_dirBackupsFolders.append(dir)
    oldData_dirBackupsFolders.sort()
    print oldData_dirBackupsFolders
    #print 80*"*"
    for each in oldData_dirBackupsFolders[:-numberOfData_dirBackupsToKeep]:
        print "Removing directory %s" % each
        shutil.rmtree(os.path.join(data_dirDirectoryPath, each))

################################################################################
def modifyGWCDiskQuotaJDBCXml(diskQuotaFilePath, gwcJdbcCOnfig):
    '''
        Modify JdbcDiskQuota depending the environnement and server
    '''
    DBHOST = gwcJdbcCOnfig["DBHOST"]
    DBPORT = gwcJdbcCOnfig["DBPORT"]
    DBNAME = gwcJdbcCOnfig["DBNAME"]
    #print "diskQuotaFilePath:", diskQuotaFilePath
    if os.path.isfile(diskQuotaFilePath):
        tree=ElementTree.parse(diskQuotaFilePath)
        root = tree.getroot()
        ip = getIP()
        for url in root.iter('url'):
            #Sample Connection String jdbc:postgresql://192.168.13.132:5432/gs_gwc_tiles
            conStr = "jdbc:postgresql://{host}:{port}/{database}_{ipLastPart}".format(host=DBHOST, port=DBPORT, database=DBNAME, ipLastPart=ip.split('.')[3])
            #print conStr
            url.text = conStr
        tree.write(diskQuotaFilePath)
    else:
        print "%s does not exist" % diskQuotaFilePath

def modifyGWCBlobPathInXml(gwc_blobFilePath, gwc_blobPath):
    '''
        Modify gwc_blob path in xml file
    '''
    
    print "gwc_blobFilePath: ", gwc_blobFilePath
    print "gwc_blobPath: ", gwc_blobPath
    if os.path.isfile(gwc_blobFilePath):
        print "gwc_blobFilePath isfile"
        ElementTree.register_namespace('', "http://geowebcache.org/schema/1.13.0")
        tree=ElementTree.parse(gwc_blobFilePath)
        print 'ok 0'
        root = tree.getroot()
        print root.tag
        print 'ok 1'
        for baseDirectory in root.iter('{http://geowebcache.org/schema/1.13.0}baseDirectory'):
            print 'ok 1.0'
            conStr = gwc_blobPath
            print conStr
            baseDirectory.text = conStr
            print 'ok 1.1'
        tree.write(gwc_blobFilePath)
    else:
        print "%s does not exist" % gwc_blobFilePath


def getIP():
    import socket
    if os.name !="nt":
        import fcntl
        import struct
        def get_interface_ip(ifname):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915, #SIOCGIFADDR
                struct.pack('256s', ifname[:15])
            )[20:24])
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = ["eth0", "eth1", "eth2", "wlan0", "wlan1", "wifi0", "ath0", "ath1", "ppp0"]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break;
            except IOError:
                pass
    return ip

        
def clean_gwc_db(host,user):
    try:
        print("Start reset gwc db process")
        print("Get local IP")
        the_ip = getIP()
        last_part = the_ip.split('.')[3]
        db_name = "gs_gwc_tiles_%s" % (last_part)
        conn_s = "dbname='%s' user='%s' host='%s' password='%s'" % (db_name, user,host, user)
        with psycopg2.connect(conn_s) as conn:
            cur = conn.cursor()
            cur.execute("""TRUNCATE tilepage CASCADE""")
        print("SUCCEED")
        return True
    except:
        print("FAILED", sys.exc_info())
        return False

################################################################################




