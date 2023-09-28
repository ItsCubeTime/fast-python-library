"Tools for packaging & distributing your projects"
import sys
import os
from .. import files
from ..data import data
from .. import string


import pathlib
def setupPackage(projectRootDir = pathlib.Path(sys.argv[0]).parent, genProjectToml = True, genReadme = True, genLicenseFile = True):
    projectRootDir = files.Folder(projectRootDir)


    if genProjectToml:
        authorsStr = ""
        for dev in data.developers:
            authorsStr += f'{{ name="{dev.name}", email="{dev.contactInformation["email"] if "email" in dev.contactInformation.keys() else "N/A"}" }},\n'

        projectUrlStr = ""
        for linkName,link in data.appLinks:
            projectUrlStr += f'"{linkName}" = "{link}"\n'

        pyproj = f"""[project]
name = "{string.PascalCaseTo_snake_case(string.capitalizeLetterAfterEachSpace(data.appName).replace(' ', '')).lower()}"
version = "{data.appVersion}"
authors = [
    {authorsStr}
]
description = "{data.appDescriptionShort}"
readme = "README.md"

{"[project.urls]" if len(projectUrlStr) > 0 else ""}
{projectUrlStr}

[tool.setuptools]
py-modules = []
"""
        files.File(projectRootDir + "pyproject.toml").setContent(pyproj)

    if genReadme:
        files.File(projectRootDir + "README.md").setContent(f"""# {data.appName}
{data.appReadme}""")
    if genLicenseFile:
        files.File(projectRootDir + "LICENSE").setContent(f"""{data.license}""")
    

def buildForPypi(projectRootDir = pathlib.Path(sys.argv[0]).parent):
    projectRootDir = files.Folder(projectRootDir)
    os.system(f"{sys.executable} -m pip install --upgrade build")
    os.system(f"cd {projectRootDir} & {sys.executable} -m build")

def uploadPrebuiltWheelToPypi(projectRootDir = pathlib.Path(sys.argv[0]).parent, testPypi=False):
    projectRootDir = files.Folder(projectRootDir)
    os.system(f"{sys.executable} -m pip install --upgrade twine")
    os.system(f"cd {projectRootDir} & {sys.executable} -m twine upload --repository {'testpypi' if testPypi else 'pypi'} dist/*")
