import MyBruGISDeployConf as MDC
################################################################################

localServerName             = MDC.localServerName

rootDiskLetter              = MDC.rootDiskLetter

geoserverServiceName        = MDC.geoserverServiceName

tomcatServerFilePath        = MDC.tomcatServerFilePath

ftpRepositoryDirectoryPath  = rootDiskLetter + "/srv/ftp_root"
warDirectoryPath            = tomcatServerFilePath + "/webapps"
backupDirectoryPath         = rootDiskLetter + "/srv/MyBruGIS_backups"
docxTemplateDirectoryPath   = rootDiskLetter + "/srv/reperage/DocxTemplate"

webRepWarName                     = "WebReperage.war"
templateTarName                   = "UrbanalysisTemplates.tar"

################################################################################
loggingFileName = "logging.xml"

################################################################################
