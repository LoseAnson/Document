#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys

def txt_wrap_by(start_str, end, html):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()

def getCrashFileUUID(filePath):
    f = open(filePath)             # 返回一个文件对象
    line = f.readline()             # 调用文件的 readline()方法
    uuid = ''
    while line:
        if line.startswith('Binary Images:'):
            desLine = f.readline()
            uuid = txt_wrap_by("<",">",desLine)
            break
        line = f.readline()
    f.close()
    return uuid.upper()

def getTagFileUUID(filePath):
    ines = os.popen('dwarfdump --uuid ' + filePath).readlines()
    uuids = []
    for item in ines:
        uuid = txt_wrap_by('UUID:', ' (', item)
        uuid = uuid.replace('-','').upper()
        uuids.append(uuid)
    return uuids

def getDevDir():
    return os.popen('xcode-select -p').readlines()[0].replace('\n', '')

def getSymbolicatecrashPath():
    return getDevDir().replace('Developer', '') + 'SharedFrameworks/DVTFoundation.framework/Versions/A/Resources/symbolicatecrash'



if len(sys.argv) <= 2:
    print "sorry! you must input 2 arg like this："
    print "\t python decode.py 1.crash xxxx.app.dSYM"
    exit(0)

crashFilePath = sys.argv[1]
dsymFilePath = sys.argv[2]
print "crashFilePath:" + crashFilePath
print "dsymFilePath:" + dsymFilePath


outPutFilePath = crashFilePath + ".log"

#检查uuid是否匹配
crashUUID = getCrashFileUUID(crashFilePath)
tagUUIDS = getTagFileUUID(dsymFilePath)
if crashUUID in tagUUIDS:
    print "UUID match success! " + crashUUID
else:
    print  "UUID not match"
    exit(0)

#设置环境变量
cmd = "export DEVELOPER_DIR=\"" + getDevDir()+"\"\n"

symbolicatecrashPath = getSymbolicatecrashPath()

cmd +=  symbolicatecrashPath + " " + crashFilePath + " " + dsymFilePath + ' > ' + outPutFilePath + '\n'
cmd += 'open '+outPutFilePath
print os.popen(cmd)