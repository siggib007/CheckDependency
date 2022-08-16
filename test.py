'''
Script to test the MultiSQL module

Author Siggi Bjarnason Copyright 2022


'''
# Import libraries
import CheckDepend
import os
import time
import sys
import platform

# End imports


def GetFileHandle(strFileName, strperm):
  """
  This wraps error handling around standard file open function 
  Parameters:
    strFileName: Simple string with filename to be opened
    strperm: single character string, usually w or r to indicate read vs write. other options such as "a" are valid too.
  Returns:
    File Handle object
  """
  dictModes = {}
  dictModes["w"] = "writing"
  dictModes["r"] = "reading"
  dictModes["a"] = "appending"
  dictModes["x"] = "opening"

  cMode = strperm[0].lower()

  try:
    objFileOut = open(strFileName, strperm, encoding='utf8')
    return objFileOut
  except PermissionError:
    print("unable to open output file {} for {}, "
          "permission denied.".format(strFileName, dictModes[cMode]))
    return("Permission denied")
  except FileNotFoundError:
    print("unable to open output file {} for {}, "
          "Issue with the path".format(strFileName, dictModes[cMode]))
    return("key not found")

def FetchEnv(strVarName):
  """
  Function that fetches the specified content of specified environment variable, 
  converting nonetype to empty string.
  Parameters:
    strVarName: The name of the environment variable to be fetched
  Returns:
    The content of the environment or empty string
  """

  if os.getenv(strVarName) != "" and os.getenv(strVarName) is not None:
    return os.getenv(strVarName)
  else:
    return ""

def LogEntry(strMsg, bAbort=False):
  print(strMsg)
  if bAbort:
    print("{} is exiting abnormally on {}".format(
        strScriptName, strScriptHost))
    if not isinstance (dbConn,str):
      dbConn.close()
    sys.exit(9)

def main():
  global strScriptName
  global strScriptHost
  global dbConn
  
  lstSysArg = sys.argv
  strScriptName = os.path.basename(sys.argv[0])
  strRealPath = os.path.realpath(sys.argv[0])
  strVersion = "{0}.{1}.{2}".format(
      sys.version_info[0], sys.version_info[1], sys.version_info[2])

  strScriptHost = platform.node().upper()

  print("This is a script to test if modules are installed. This is running under Python Version {}".format(strVersion))
  print("Running from: {}".format(strRealPath))
  now = time.asctime()
  print("The time now is {}".format(now))

  #strVault = FetchEnv("VAULT")
  if len(lstSysArg) > 1:
    strCommand = lstSysArg[1]
  else:
    strCommand = input("Please provide module name: ")

  dictResult = CheckDepend.CheckDependency(strCommand)
  print("Dependency for {} good:{}".format(strCommand, dictResult["success"]))
  objFileOut = GetFileHandle("DependencyOut.txt","w")
  for strKey in dictResult:
    objFileOut.write ("{}: {}\n".format(strKey,dictResult[strKey]))

  objFileOut.close()
  now = time.asctime()
  LogEntry("Completed at {}".format(now))
  print("{} completed successfully on {}".format(
      strScriptName, strScriptHost))





if __name__ == '__main__':
    main()
