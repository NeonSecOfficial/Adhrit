# !/usr/bin/python

import os
import re
from sys import exit


def smali_de(apk_name):
    print "\n--------------------------------------------------"
    print "[+] SOURCE EXTRATION IN SMALI"
    print "----------------------------------------------------"
    snamesplit = apk_name.split('.')[0]
    SmaliCmd = 'java -jar tools/apktool.jar d -f ' + apk_name
    os.system(SmaliCmd)
    if os.path.isdir(snamesplit):
        print "\n\t[+] Extraction complete."


def smali_re(apk_name):
    print "\n--------------------------------------------------"
    print "[+] RECOMPILING SMALI"
    print "----------------------------------------------------"
    snamesplit = apk_name.split('.')[0]
    if os.path.isdir(snamesplit):
        SmaliCmd = 'java -jar tools/apktool.jar b -f ' + snamesplit
        os.system(SmaliCmd)
        print "\n\t[+] Recompiling complete."
        print "\n\t[+] The recompiled apk in " + snamesplit + "/dist\n"
    else:
        print "\n\t[!] smali source not found"


def inj_check(apk_name):
    snamesplit = apk_name.split('.')[0]
    if os.path.isdir(snamesplit) == 0:
        print "\n\t[!] bytecode not found. Extracting"
        smali_de(apk_name)
    print "\n--------------------------------------------------"
    print "[+] CHECKING FOR BYTECODE INJECTIONS"
    print "----------------------------------------------------"
    inj_points = 0
    smali_dir = 'smali'
    if os.path.isdir('smali_copy'):
        os.system('rm -r smali_copy')
    os.system('cp -R ' + snamesplit + '/' + smali_dir + ' smali_copy')
    if os.path.isdir('smali_copy'):
        os.chdir('smali_copy')
        ignore_dirs = ['android', 'org', 'google', 'localytics']
        for dirList, subdirList, subfiles in os.walk(os.getcwd()):
            for subfiles in ignore_dirs:
                os.system('rm -r ' + subfiles + ' 2> /dev/null')
            for subdirList in ignore_dirs:
                os.system('rm -r ' + subdirList + ' 2> /dev/null')
            for dirList in ignore_dirs:
                os.system('rm -r ' + dirList + ' 2> /dev/null')

    for dirList, subdirList, subfiles in os.walk(os.getcwd()):
        for files in subfiles:
            with open(os.path.abspath(os.path.join(dirList, files))) as f:
                for lines in f:
                    pattern1 = 'const-string'
                    if pattern1 in lines:
                        inj_points = inj_points + 1
                        print "\n\t" + os.path.basename(f.name)
                        print lines
    print "\n\t[+] " + str(inj_points) + "simple injection points found\n"
