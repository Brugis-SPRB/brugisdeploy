import MyBruGISDeployConf as MDC
import MyBruGISDeployLibrary as MDL
import os

MDL.modifyLoggingXml(os.path.join(MDC.dataDirPath, MDC.loggingFileName))