#-*- coding: latin_1 -*-
# Python script for Urbanalysis deploy

import os
import datetime
import time

import UrbanalysisDeployConf as UDC
import UrbanalysisDeployLibrary as UDL
from printAndLog import printAndLog
import sendmail

################################################################################

LOCALDIRN   = UDC.ftpRepositoryDirectoryPath
LOGFILE     = os.path.basename(__file__).replace('py','log')
SENDMAIL    = False

################################################################################

with open(os.path.join(LOCALDIRN, LOGFILE),'w') as logFile:
    printAndLog("%s - %s - log - %s" % (UDC.localServerName, os.path.basename(__file__), str(datetime.datetime.today())), logFile)
    tarFileName = os.path.join(LOCALDIRN, UDC.templateTarName)
    warFileName = os.path.join(LOCALDIRN, UDC.webRepWarName)

    printAndLog("*** Deploy Urbanalysis ***", logFile)
    # on v�rifie si on a re�u un fichier tar contenant les templates
    if os.path.exists(tarFileName):
        # si oui,
        # on le d�tare en local
        UDL.untarDocxTemplate(tarFileName, diskDriveLetter = UDC.rootDiskLetter + "\\")
        # on backupe le dossier de templates
        # on d�place le dossier d�tar� � sa position d�finitive
        UDL.deployDocxTemplate(tarFileName.replace(".tar",""),
                               UDC.docxTemplateDirectoryPath,
                               "",
                               "")
    
    # on v�rifie si on a re�u un fichier war de webreperage
    if os.path.exists(warFileName):
        # si oui,
        SENDMAIL = True
        # on stoppe tomcat
        tomcatStopped = UDL.stopWinService(UDC.geoserverServiceName)
        if tomcatStopped:
            printAndLog("*** Service %s stopped. Deploying..." % UDC.geoserverServiceName, logFile)
            # on jette le dossier webreperage dans tomcat/webapp
            # on d�place le fichier webreperage re�u dans tomcat/webapps/
            # on backupe le war actuellement dans tomcat
            UDL.deployFile(UDC.ftpRepositoryDirectoryPath, UDC.webRepWarName, UDC.webRepWarName, UDC.warDirectoryPath, UDC.backupDirectoryPath)
            # on red�marre tomcat
            tomcatStarted = UDL.startWinService(UDC.geoserverServiceName)
        else:
            printAndLog("*** Impossible to stop service %s, no deploy done" % UDC.geoserverServiceName, logFile)
    else:
        printAndLog("*** No templates to deploy", logFile)
    printAndLog("*** Deploy finished", logFile)

with open(os.path.join(LOCALDIRN,LOGFILE), 'r') as logFile:
    if SENDMAIL:
        sendmail.send_mail('%s - %s - log - %s' % (UDC.localServerName, os.path.basename(__file__), str(datetime.datetime.today())), logFile.read())
    
################################################################################
    

    