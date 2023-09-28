import pathlib
import sys
from ..classes import User

backSlash = "\\"


class Data:
    appName: str = "Template App Name"
    "Set me"

    appIcon: str = (pathlib.Path(__file__).parent.absolute().as_posix() + "/assets/readyFox32px.png").replace('//', '/')

    license: str = "All Rights Reserved."

    publishers: list[str] = ["Mr. Lorem Ipsum"]
    "Set me, list of publishers of your app. Typically the names of individuals & organizations with right to publish & distribute the app first hand"

    appVersion: str = "N/A"

    appDescriptionShort = "A software that makes the world a better place."
    "Describe your software in as few words as possible."

    appReadme = "A software that makes the world a better place."
    "Used for files in style with README.md, dont add the project title at the top, its added for you."

    appLinks: dict[str,str] = dict()
    """Eg: {"Bug Tracker"="https://github.com"}"""

    user: User = User(username="User", password="", userId="User")

    userHomeDirectory = pathlib.Path.home().absolute().as_posix()
    "Override me on app startup if desired"

    globalAppDataDirectory = (pathlib.Path.home() / ('AppData/Local' if sys.platform == 'win32' else ('.local/share' if sys.platform == 'linux' else ('Library/Application Support' if sys.platform == 'darwin' else lambda: exec('raise Exception'))))).absolute().as_posix()
    "Eg C:/users/olliv/AppData/Local on Windows. Override me on app startup if desired"

    # @note As of 6-4-2022 Im feeling unsure how/where permanent local data should be best stored.
    # Maybe should I put everything inside fast.db, and fast.db stores everything under: __main__.__file__.parent/f'__fast__/{data.appName}/lsdb'

    libraryName = "Fast Python Library"
    libraryNameShort = "Fast"

    @property
    def tempDir(self):
        "All temp files & dirs should be created in this directory. Files created here will be automatically deleted on application exit & startup."
        import tempfile
        return (tempfile.gettempdir()+f"/__{self.libraryNameShort.lower()}__/{self.appName}").replace('\\','/').replace('//','/')
    
    @property
    def appDataDirectory(self, val=None):
        "Eg C:/users/olliv/AppData/Local/appName"
        self._appDataAppDirectory = val if val else None
        if self._appDataAppDirectory:
            return self._appDataAppDirectory
        return self.globalAppDataDirectory + f'/{self.appName}'
    @property
    def localUserDataDir(self, val=None):
        return self.appDataAppDir + f'/userData/{self.user.userId}'

    class Developer:
        """contactInformation example: {"email":"olliver.aira@gmail.com"}"""
        def __init__(self, name: str, roles: list[str] = [], organizations: list[str] = [], contactInformation:dict = dict()):
            self.name = name
            self.roles = roles
            "Eg: [Software Engineer, UX Designer]"
            self.organizations = organizations
            """Organizations he've been working under whilst contributing to the project, would be: '[Open Source Contributor, ReadyFox Inc]' if he've
            spent time working on the project under ReadyFox Inc payroll & as well as his own free time contributiting."""
            self.contactInformation = contactInformation
    developers: list[Developer] = [Developer("Mr. Lorem Ipsum")]
    "Set me, list of developers of your app. Could be the individual contributors names or names of involved organizations"



    # @property
    # def dataLocation(self, value: str):
    #     "Set me if desired. Defaults to %APPDATA%/fast/"
    #     _dataLocation = value.replace('\\', '/').replace('//', '/')
    #     if _dataLocation[-1] != '/':
    #         _dataLocation = _dataLocation + '/'
    #     return _dataLocation

    # @property
    # def logLocation(self):
    #     """Readonly. defaults to f"{dataLocation}"/logs/"""
    #     return str(data.dataLocation) + "logs/"


data = Data()
"""I hold various generic data used across the entire fast library.

Im a class instance accessible directly under the fast parent module."""

# if "__fastData__" in globals():
#     print("loading data")
#     data = globals()["__fastData__"]
# else:
#     print("Creating data")
#     data = Data()
#     globals()["__fastData__"] = data
