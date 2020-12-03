import platform
class systemUtils:


    SYSTEM_TYPE_LINUX="Linux"

    SYSTEM_TYPE_WINDOWS="Windows"

    SYSTEM_TYPE_MACOS="Darwin"

    @staticmethod
    def getSystemType():

        return platform.system()