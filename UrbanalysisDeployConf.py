import MyBruGISDeployConf as MDC
################################################################################

localServerName             = MDC.localServerName

rootDiskLetter              = MDC.rootDiskLetter

geoserverServiceName        = MDC.geoserverServiceName

tomcatServerFilePath        = MDC.tomcatServerFilePath

ftpRepositoryDirectoryPath  = rootDiskLetter + "\FTP_Root\mybrugis_transfer\\"
warDirectoryPath            = tomcatServerFilePath + "\webapps\\"
backupDirectoryPath         = rootDiskLetter + "\MyBruGIS_backups\\"
docxTemplateDirectoryPath   = rootDiskLetter + "\DocxTemplate\\"

webRepWarName                     = "WebReperage.war"
templateTarName                   = "UrbanalysisTemplates.tar"

################################################################################
loggingFileName = "logging.xml"

################################################################################
