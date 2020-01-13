################################################################################

localServerName             = "SVAPPCAVW026"
rootDiskLetter              = "E:"
data_dirName                = "data_dir"
gwc_dirName                 = "gwc"
gwc_blob_dirName            = "gwc_blob"
dataName                    = "data"
waxName                     = "MyBruGIS.wa1"
warName                     = "MyBruGISOLD.war"
brugisWarName               = "brugis.war"
dbName                      = "geoexplorer.db"
geowebcacheDiskquotaJdbcFileName = "geowebcache-diskquota-jdbc.xml"
geowebcacheFileName         = "geowebcache.xml"
geoserverServiceName        = "Tomcat8"


ftpRepositoryDirectoryPath  = rootDiskLetter + "\FTP_Root\\mybrugis_transfer\\"
brugisFtpRepositoryDirectoryPath = rootDiskLetter + "\FTP_Root\\brugis_transfer\\"
tomcatServerFilePath        = rootDiskLetter + "\Tomcat 8.0"
backupDirectoryPath         = rootDiskLetter + "\MyBruGIS_backups\\"
data_dirDirectoryPath       = rootDiskLetter + "\WWW_Brugis\\"
dbDirectoryPath             = tomcatServerFilePath + "\\"
warDirectoryPath            = tomcatServerFilePath + "\webapps\\"
dataDirPath                 = data_dirDirectoryPath + data_dirName + "\\"
gwcDirPath                  = dataDirPath + gwc_dirName + "\\"
gwc_blobDirPath             = dataDirPath + gwc_blob_dirName

gwcJdbcConfig = {
    "sta" : {
        "DBHOST" : "1.1.1.1",
        "DBPORT" : "5432",
        "DBNAME" : "gs_gwc_tiles"
        },
    "prd" : {
        "DBHOST" : "1.1.1.1",
        "DBPORT" : "5432",
        "DBNAME" : "gs_gwc_tiles"
        }
    }
