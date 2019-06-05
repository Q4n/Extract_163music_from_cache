#coding=utf-8
import os

def crackfile(infile,outfile):
    """
    infile: 输入的.uc文件
    outfile: 输出的.mp3文件
    """
    res=""
    with open(infile,"rb") as fp:
        tmp=fp.read()
        for i in tmp:
            res+=chr(ord(i)^163) 
    with open(outfile,"wb") as f:
        f.write(res)    
    # print "Done!"

def travel(path):
    resfiles=[]
    for filename in os.listdir(path):
        pathname=os.path.join(path,filename)
        if filename.endswith(".uc"):
            resfiles.append(pathname)
    return resfiles

def mkdir(dirname):
    if not os.path.exists(dirname):
        os.mkdir(dirname)

def main_single(cache_path=''):
    userbase=os.environ['USERPROFILE']
    CACHEPATH=userbase+"\AppData\Local\Netease\CloudMusic\Cache\Cache"
    if cache_path!='':
        CACHEPATH=cache_path
    mkdir("./out")
    count=0
    filepaths=travel(CACHEPATH)
    print "[*] "+str(len(filepaths))+" in all"
    for filepath in filepaths:
        count+=1
        crackfile(filepath,"./out/"+str(count)+".mp3")
        print "[+] "+str(count)+" done!"

import threading

class power_crack(threading.Thread):
    def __init__(self,filename,count):
        threading.Thread.__init__(self)
        self.count=count
        self.filename=filename
        self.outname="./out/"+str(count)+".mp3"
    
    def run(self):
        crackfile(self.filename,self.outname)
        print "[+] "+str(self.count)+" done!"

def main_threads(cache_path=''): 
    userbase=os.environ['USERPROFILE']
    CACHEPATH=userbase+"\AppData\Local\Netease\CloudMusic\Cache\Cache"
    if cache_path!='':
        CACHEPATH=cache_path
    mkdir("./out")
    count=0
    filepaths=travel(CACHEPATH)
    threads=[]
    for filepath in filepaths:
        count+=1
        tmp=power_crack(filepath,count)
        threads.append(tmp)
    print "[+] thread init ok!"
    print "[*] "+str(count)+" in all"
    for thread in threads:
        thread.start()
        while True:
            if len(threading.enumerate())<3:
                break

import multiprocessing
def crackfile_limit(infile,outfile,limit):
    limit.acquire()
    crackfile(infile,outfile)
    limit.release()

def main_multi(cache_path=''):
    MAX_PROCESSES=4
    userbase=os.environ['USERPROFILE']
    CACHEPATH=userbase+"\AppData\Local\Netease\CloudMusic\Cache\Cache"
    if cache_path!='':
        CACHEPATH=cache_path
    mkdir("./out")
    count=0
    filepaths=travel(CACHEPATH)
    print "[*] "+str(len(filepaths))+" in all"
    limit=multiprocessing.Semaphore(MAX_PROCESSES)
    for filepath in filepaths:
        count+=1
        process=multiprocessing.Process(target=crackfile_limit,args=(filepath,"./out/"+str(count)+".mp3",limit))
        process.start()

if __name__ == "__main__":
    import time
    start=time.clock()
    main_multi()
    end=time.clock()
    print "[*] Runtime is: "+str(end-start)
    # main_threads()10: 1077.16438377
    # main_single(): 473.753408343
    # main_multi()
    pass
