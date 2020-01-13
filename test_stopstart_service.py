import MyBruGISDeployConf as MDC
import MyBruGISDeployLibrary as MDL
import time


geoserverStopped = MDL.stopWinService(MDC.geoserverServiceName)

print geoserverStopped

time.sleep(10)

geoserverStarted = MDL.startWinService(MDC.geoserverServiceName)

print geoserverStarted