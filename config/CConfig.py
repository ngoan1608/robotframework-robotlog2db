# **************************************************************************************************************
#
#  Copyright 2020-2022 Robert Bosch Car Multimedia GmbH
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
# **************************************************************************************************************
#
# CConfig.py
#
# XC-CT/ECA3-Queckenstedt
#
# Purpose:
# - Compute and store all repository specific information, like the repository name,
#   paths to repository subfolder, paths to interpreter and so on ...
#
# - All paths to subfolder depends on the repository root path that has to be provided to constructor of CConfig
# 
# Additional hints:
# - Variable names like SPHINXBUILD, SOURCEDIR and BUILDDIR are taken over from original output of Sphinx
#   (when documentation project files like make.bat are generated by Sphinx; for better understanding
#   no new names here).
#
# - Output in PDF format requires LaTeX compiler and depends on %ROBOTLATEXPATH%/miktex/bin/x64/pdflatex.exe
#
# - Don't be confused: We have 'doc/_build' containing the documentation builder output
#   and we have 'build' containing the build of the setup tools. These are different things.
#
# --------------------------------------------------------------------------------------------------------------
#
# 28.02.2022 / XC-CT/ECA3-Queckenstedt
# Usage of %RobotPythonPath% exchanged by sys.executable
#
# 11.10.2021 / XC-CI1/ECA3-Queckenstedt
# Fixed path within site-packages (Linux)
# 
# 06.10.2021 / XC-CI1/ECA3-Queckenstedt
# Added Linux support
# 
# 01.10.2021 / XC-CI1/ECA3-Queckenstedt
# Added environment check
# 
# 01.10.2021 / XC-CI1/ECA3-Queckenstedt
# Added wrapper for error messages
# 
# Initial version 08/2021
#
# --------------------------------------------------------------------------------------------------------------

import os, sys, platform, shlex, subprocess
import colorama as col
import pypandoc

col.init(autoreset=True)
COLBR = col.Style.BRIGHT + col.Fore.RED
COLBG = col.Style.BRIGHT + col.Fore.GREEN

# --------------------------------------------------------------------------------------------------------------

def printerror(sMsg):
    sys.stderr.write(COLBR + f"Error: {sMsg}!\n")

def printexception(sMsg):
    sys.stderr.write(COLBR + f"Exception: {sMsg}!\n")

# --------------------------------------------------------------------------------------------------------------

class CConfig():

    def __init__(self, sReferencePath="."):

        self.__dictConfig = {}

        self.__sReferencePath = os.path.normpath(os.path.abspath(sReferencePath))
        self.__dictConfig['sReferencePath'] = self.__sReferencePath # only to have the possibility to print out all values only with help of 'self.__dictConfig'

        # 1. basic setup stuff
        self.__dictConfig['sPackageName']                = "RobotResults2DB"
        self.__dictConfig['sVersion']                    = "1.0.0"
        self.__dictConfig['sAuthor']                     = "Tran Duy Ngoan"
        self.__dictConfig['sAuthorEMail']                = "Ngoan.TranDuy@vn.bosch.com"
        self.__dictConfig['sDescription']                = "Package for importing robot result(s) to TestResultWebApp database"
        self.__dictConfig['sLongDescriptionContentType'] = "text/markdown"
        self.__dictConfig['sURL']                        = "https://github.com/test-fullautomation/robotframework-testresultwebapptool"
        self.__dictConfig['sProgrammingLanguage']        = "Programming Language :: Python :: 3"
        self.__dictConfig['sLicence']                    = "License :: OSI Approved :: Apache Software License"
        self.__dictConfig['sOperatingSystem']            = "Operating System :: OS Independent"
        self.__dictConfig['sPythonRequires']             = ">=3.0"
        self.__dictConfig['sDevelopmentStatus']          = "Development Status :: 4 - Beta"
        self.__dictConfig['sIntendedAudience']           = "Intended Audience :: Developers"
        self.__dictConfig['sTopic']                      = "Topic :: Software Development"
        self.__dictConfig['arInstallRequires']            = ['sphinx','pypandoc','colorama']


        # 2. certain folder and executables (things that requires computation)
        bSuccess, sResult = self.__InitConfig()
        if bSuccess != True:
            raise Exception(sResult)
        print(COLBG + sResult)
        print()


    def __del__(self):
        del self.__dictConfig


    def __InitConfig(self):

        sOSName         = os.name
        sPlatformSystem = platform.system()
        sPythonPath     = os.path.dirname(sys.executable)
        sPython         = sys.executable
        sPythonVersion  = sys.version

        SPHINXBUILD                = None
        sLaTeXInterpreter          = None
        sInstalledPackageFolder    = None
        sInstalledPackageDocFolder = None

        try:
            self.__dictConfig['sPandoc'] = pypandoc.get_pandoc_path()
        except Exception as ex:
            bSuccess = False
            sResult  = str(ex)
            return bSuccess, sResult

        if sPlatformSystem == "Windows":
            SPHINXBUILD                = f"{sPythonPath}/Scripts/sphinx-build.exe"
            sInstalledPackageFolder    = f"{sPythonPath}/Lib/site-packages/" + self.__dictConfig['sPackageName']
            sInstalledPackageDocFolder = f"{sPythonPath}/Lib/site-packages/" + self.__dictConfig['sPackageName'] + "_doc"
            sLaTeXInterpreter          = os.path.normpath(os.path.expandvars("%ROBOTLATEXPATH%/miktex/bin/x64/pdflatex.exe"))

        elif sPlatformSystem == "Linux":
            SPHINXBUILD                = f"{sPythonPath}/sphinx-build"
            sInstalledPackageFolder    = f"{sPythonPath}/../lib/python3.9/site-packages/" + self.__dictConfig['sPackageName']
            sInstalledPackageDocFolder = f"{sPythonPath}/../lib/python3.9/site-packages/" + self.__dictConfig['sPackageName'] + "_doc"
            sLaTeXInterpreter          = os.path.normpath(os.path.expandvars("${ROBOTLATEXPATH}/miktex/bin/x64/pdflatex"))

        else:
            bSuccess = False
            sResult  = f"Operating system {sPlatformSystem} ({sOSName}) not supported"
            return bSuccess, sResult

        if os.path.isfile(sLaTeXInterpreter) is False:
            sLaTeXInterpreter = None # not an error; PDF generation is an option

        if os.path.isfile(SPHINXBUILD) is False:
            bSuccess = False
            sResult  = f"Missing Sphinx '{SPHINXBUILD}'"
            return bSuccess, sResult

        self.__dictConfig['SPHINXBUILD']                = SPHINXBUILD
        self.__dictConfig['sPython']                    = sPython
        self.__dictConfig['sLaTeXInterpreter']          = sLaTeXInterpreter
        self.__dictConfig['sInstalledPackageFolder']    = sInstalledPackageFolder
        self.__dictConfig['sInstalledPackageDocFolder'] = sInstalledPackageDocFolder


        # ---- paths relative to repository root folder (where the srcipts are located that use this module)

        # ====== 1. documentation

        # This doesn't matter in case of the documentation builder itself is using this CConfig.
        # But if the documentation builder is called by other apps like setup_ext.py, they need to know where to find.
        sDocumentationBuilder = os.path.normpath(self.__sReferencePath + "/sphinx-makeall.py")
        self.__dictConfig['sDocumentationBuilder'] = sDocumentationBuilder

        # - documentation project source dir (relative to reference path (= position of executing script)
        SOURCEDIR = os.path.normpath(self.__sReferencePath + "/doc")
        self.__dictConfig['SOURCEDIR'] = SOURCEDIR

        # - documentation project build dir
        BUILDDIR = os.path.normpath(SOURCEDIR + "/_build")
        self.__dictConfig['BUILDDIR'] = BUILDDIR

        # - documentation project html output folder
        sHTMLOutputFolder = os.path.normpath(BUILDDIR + "/html")
        self.__dictConfig['sHTMLOutputFolder'] = sHTMLOutputFolder

        # - README
        sReadMe_rst = os.path.normpath(self.__sReferencePath + "/README.rst")
        self.__dictConfig['sReadMe_rst'] = sReadMe_rst
        sReadMe_md = os.path.normpath(self.__sReferencePath + "/README.md")
        self.__dictConfig['sReadMe_md'] = sReadMe_md


        # ====== 2. setuptools

        self.__dictConfig['sSetupBuildFolder']       = os.path.normpath(self.__sReferencePath + "/build")
        self.__dictConfig['sSetupBuildLibFolder']    = os.path.normpath(self.__sReferencePath + "/build/lib")
        self.__dictConfig['sSetupBuildLibDocFolder'] = os.path.normpath(self.__sReferencePath + "/build/lib/" + self.__dictConfig['sPackageName'] + "_doc")
        self.__dictConfig['sSetupDistFolder']        = os.path.normpath(self.__sReferencePath + "/dist")
        self.__dictConfig['sEggInfoFolder']          = os.path.normpath(self.__sReferencePath + "/" + self.__dictConfig['sPackageName'] + ".egg-info")

        print()
        print(f"Running under {sPlatformSystem} ({sOSName})")
        self.PrintConfig()

        bSuccess = True
        sResult  = "Repository setup done"
        return bSuccess, sResult

    # eof def __InitConfig(self):


    def PrintConfig(self):
        # -- printing configuration to console
        nJust = 30
        print()
        for sKey in self.__dictConfig:
            print(sKey.rjust(nJust, ' ') + " : " + str(self.__dictConfig[sKey]))
        print()
    # eof def PrintConfig(self):


    def Get(self, sName=None):
        if ( (sName is None) or (sName not in self.__dictConfig) ):
            print()
            printerror(f"Error: Configuration parameter '{sName}' not existing!")
            # from here it's standard output:
            print("Use instead one of:")
            self.PrintConfig()
            return None # returning 'None' in case of key is not existing !!!
        else:
            return self.__dictConfig[sName]
    # eof def Get(self, sName=None):

# eof class CConfig():

# --------------------------------------------------------------------------------------------------------------
