'''
Module to check if depended module is already installed, and if not install it
uses pip list and ppip install
Author Siggi Bjarnason Copyright 2022


Uses the following packages, which CheckDependency will try to install if missing
pip install pymysql
pip install pyodbc
pip install psycopg2

'''
import subprocess
import sys

def CheckDependency(Module):
  """
  Function that installs missing depedencies
  Parameters:
    Module : The name of the module that should be installed
  Returns:
    dictionary object without output from the installation.
      if the module needed to be installed
        code: Return code from the installation
        stdout: output from the installation
        stderr: errors from the installation
        args: list object with the arguments used during installation
        success: true/false boolean indicating success.
      if module was already installed so no action was taken
        code: -5
        stdout: Simple String: {module} version {x.y.z} already installed
        stderr: Nonetype
        args: module name as passed in
        success: True as a boolean
  """
  dictComponents = {}
  dictReturn = {}
  strModule = Module
  lstOutput = subprocess.run(
      [sys.executable, "-m", "pip", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  lstLines = lstOutput.stdout.decode("utf-8").splitlines()
  for strLine in lstLines:
    lstParts = strLine.split()
    dictComponents[lstParts[0].lower()] = lstParts[1]
  if strModule.lower() not in dictComponents:
    lstOutput = subprocess.run(
        [sys.executable, "-m", "pip", "install", strModule], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    dictReturn["code"] = lstOutput.returncode
    dictReturn["stdout"] = lstOutput.stdout.decode("utf-8")
    dictReturn["stderr"] = lstOutput.stderr.decode("utf-8")
    dictReturn["args"] = lstOutput.args
    if lstOutput.returncode == 0:
      dictReturn["success"] = True
    else:
      dictReturn["success"] = False
    return dictReturn
  else:
    dictReturn["code"] = -5
    dictReturn["stdout"] = "{} version {} already installed".format(
        strModule, dictComponents[strModule.lower()])
    dictReturn["stderr"] = None
    dictReturn["args"] = strModule
    dictReturn["success"] = True
    return dictReturn
