import tinify
from tinify import AccountError, ClientError, ConnectionError, ServerError
import os
import threading
import math
#import requests.packages.urllib3
#requests.packages.urllib3.disable_warnings()


#===============tinypng python scripts for android===============
# step 1: run "pip install --upgrade tinify"
# step 2: prepare your tinypng keys, write them to accounts.txt, each account one line
# step 3: copy this dir to your project root dir, cd to tinypng dir & run "python tinyPics.py"
#
#
# tips 1: image files will be add to compressed_file_list.txt automatically
# tips 2: (optional)image files(absolute paths) in white_list.txt will be ignored if you do not want to compress them
# tips 3: if SSL connections error happens , open the import of requests.packages.urllib3
#
#===============tinypng python scripts for android===============

class AccountManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.accounts = {}
        flag = False
        with open('tinypng/accounts.txt', 'r') as f:
            for line in f:
                self.accounts[line] = True
                if not flag:
                    tinify.key = line
                    flag = True

    def getAvailableAccount(self):
        self.lock.acquire()
        result = None
        try:
            for k, v in self.accounts.items():
                if v :
                    print '\ntry to use account:', k
                    result = k
        finally:
            self.lock.release()
        return result

    def setAccountUnavailable(self, accountKey):
        self.lock.acquire()
        try:
            if None != accountKey:
                self.accounts[accountKey] = False
                print '\nset account unavailable:', accountKey, self.accounts
        finally:
            self.lock.release()

class Compresser(threading.Thread):

    def __init__(self, filesToBeCompress, accountManager):
        threading.Thread.__init__(self)
        self.filesToBeCompress = filesToBeCompress
        self.accountManager = accountManager

    def run(self):
        print '\nthread start...' + threading.currentThread().name
        for f in self.filesToBeCompress:
            if (not self.tiny(f, cwd)):
                return

    def tiny(self, f, cwd):
        try:
            tinify.from_file(f).to_file(f)
            append_compressed_file(f, cwd)
            print "tinypng " , f
        except AccountError, e:
            print "\nAccountError .. " + e.message, threading.currentThread().name
            self.accountManager.setAccountUnavailable(tinify.key)
            newKey = self.accountManager.getAvailableAccount()
            if (None == newKey):
                print "\nAll counts tried , finish"
                exit(0)
                return False
            else:
                tinify.key = newKey
                self.tiny(f, cwd)
        except ClientError, e1:
            print "\nClientError ..", e1, f, threading.currentThread().name
            # tiny(f,cwd)
            # return False
        except ServerError, e2:
            print "\nServerError ..", e2, f, threading.currentThread().name
            # tiny(f,cwd)
            # return False
        except ConnectionError, e3:
            print "\nConnectionError ..", e3, f, threading.currentThread().name
            # tiny(f,cwd)
            # return False

        return True

def get_picpaths(directory):
    file_paths = []  # List which will store all of the full filepaths.

    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to from the full filepath.
            filepath = os.path.join(root, filename)
            if (filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg")) and not in_compressed_list(filepath,directory) and not in_white_list(filepath,directory) and 'intermediates' not in filepath and '.9' not in filepath:
                file_paths.append(filepath)

    return file_paths

# ignore all files in tinypng/white_list.txt


def in_white_list(filepath,cwd):
    if not os.path.isfile("tinypng/white_list.txt"):
        return False
    filepath=filepath.replace(cwd,'')
    if filepath in open("tinypng/white_list.txt").read():
        print "\n*******"+ filepath + "******* in white_list , ignore"
        return True
    else:
        return False

# ignore all files had been compressed


def in_compressed_list(filepath,cwd):
    if not os.path.isfile("tinypng/compressed_file_list.txt"):
        return False
    filepath=filepath.replace(cwd,'')
    if filepath in open("tinypng/compressed_file_list.txt").read():
        print "\n====== " + filepath + " ====== in compressed_file_list , ignore"
        return True
    else:
        return False

# record file to tinypng/compressed_file_list.txt


def append_compressed_file(filepath,cwd):
    filepath=filepath.replace(cwd,'')
    fp = open("tinypng/compressed_file_list.txt", "a+")
    fp.write(filepath + "\n")
    fp.flush()
    fp.close()

if __name__ == "__main__":
    #cd to projectDir(tinypng parentDir)
    os.chdir('..')
    cwd=os.getcwd()
    accountManager = AccountManager()
    full_pic_paths = get_picpaths(cwd)
    if len(full_pic_paths) <= 0:
        print '\n====Warning!==== there is no image, or all images have been compressed according to compressed_file_list.txt, clear compressed_file_list.txt and try again\n'
        exit(0)
    threadCount = int(math.sqrt(len(full_pic_paths)))
    groupSize = len(full_pic_paths)/threadCount
    index=0
    while index < threadCount :
        if index < threadCount - 1:
            files = full_pic_paths[index * groupSize: (index + 1) * groupSize]
        else:
            files = full_pic_paths[index * groupSize: len(full_pic_paths)]
        # print files
        index = index + 1
        Compresser(files, accountManager).start()

    print '====Done!===='