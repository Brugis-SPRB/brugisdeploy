#-*- coding: latin_1 -*-
# Python script for Brugis deploy

import os
import datetime
import time

import MyBruGISDeployConf as MDC
import MyBruGISDeployLibrary as MDL
from printAndLog import printAndLog
import sendmail

################################################################################

LOCALDIRN   = MDC.ftpRepositoryDirectoryPath
LOGFILE     = os.path.basename(__file__).replace('py','log')
SENDMAIL    = False
migrationTo = "sta"

################################################################################

with open(os.path.join(LOCALDIRN, LOGFILE),'w') as logFile:
    printAndLog("%s - %s - log - %s" % (MDC.localServerName, os.path.basename(__file__), str(datetime.datetime.today())), logFile)
    tarFileName = os.path.join(MDC.ftpRepositoryDirectoryPath, MDC.data_dirName) + ".tar"
    waxFileName = os.path.join(MDC.ftpRepositoryDirectoryPath, MDC.waxName)
    brugisWarFileName = os.path.join(MDC.brugisFtpRepositoryDirectoryPath, MDC.brugisWarName)
    dbFileName  = os.path.join(MDC.ftpRepositoryDirectoryPath, MDC.dbName)

    if os.path.exists(tarFileName) or os.path.exists(waxFileName) or os.path.exists(dbFileName) or os.path.exists(brugisWarFileName):
        SENDMAIL = True
        geoserverStopped = MDL.stopService(MDC.geoserverServiceName)
        if geoserverStopped:
            printAndLog("*** Service %s stopped. Deploying..." % MDC.geoserverServiceName, logFile)
            # Migration of MyBruGIS.war if present
            MDL.deployFile(MDC.ftpRepositoryDirectoryPath, MDC.waxName, MDC.warName, MDC.warDirectoryPath, MDC.backupDirectoryPath)
            # Migration of bruGIS.war if present
            MDL.deployFile(MDC.brugisFtpRepositoryDirectoryPath, MDC.brugisWarName, MDC.brugisWarName, MDC.warDirectoryPath, MDC.backupDirectoryPath)
            # Migration of geoexplorer.db if present
            MDL.deployFile(MDC.ftpRepositoryDirectoryPath, MDC.dbName, MDC.dbName, MDC.dbDirectoryPath, MDC.backupDirectoryPath)

            if os.path.exists(tarFileName):
                # untar of data_dir tar file
                MDL.untarData_dir(tarFileName, diskDriveLetter = MDC.ftpRepositoryDirectoryPath)
                # Migration of data_dir if present
                MDL.deployData_dir(os.path.join(MDC.ftpRepositoryDirectoryPath, MDC.data_dirName),
                                   os.path.join(MDC.data_dirDirectoryPath, MDC.data_dirName),
                                   MDC.gwc_dirName,
                                   MDC.gwc_blob_dirName,
                                   MDC.dataName)
                # Adaptation of Data_dir to local server and environment
                MDL.modifyGWCDiskQuotaJDBCXml(os.path.join(MDC.gwcDirPath, MDC.geowebcacheDiskquotaJdbcFileName), MDC.gwcJdbcConfig[migrationTo])
                MDL.modifyGWCBlobPathInXml(os.path.join(MDC.gwcDirPath, MDC.geowebcacheFileName), MDC.gwc_blobDirPath)
                printAndLog("*** Modification of %s Finished" % MDC.dataDirPath, logFile)

                # cleanup of old data_dir backup directories
                MDL.deleteOldData_dirBackups(MDC.data_dirDirectoryPath, 3)

            # Clean GWC DB
            if (MDL.clean_gwc_db(MDC.gwcJdbcConfig[migrationTo]["DBHOST"],"gsgwctiles")):
                printAndLog("*** Clean GWC DB SUCCEED", logFile)
            else:
                printAndLog("*** Clean GWC DB FAILED", logFile)
            printAndLog("*** Deploy finished.", logFile)
            # Start the geoserver service
            geoserverStarted = MDL.startService(MDC.geoserverServiceName)
        else:
            printAndLog("*** Impossible to stop service %s, no deploy done" % MDC.geoserverServiceName, logFile)
    else:
        printAndLog("*** Nothing to deploy", logFile)
    printAndLog("*** Deploy finished", logFile)

with open(os.path.join(LOCALDIRN,LOGFILE), 'r') as logFile:
    if SENDMAIL:
        sendmail.send_mail('%s - %s - log - %s' % (MDC.localServerName, os.path.basename(__file__), str(datetime.datetime.today())), logFile.read())

################################################################################
