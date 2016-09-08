import tinify
from tinify import AccountError, ClientError, ConnectionError, ServerError
import linecache
import os
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

def get_account_count():
    count=0
    with open ('tinypng/accounts.txt','r') as f:
        count = sum(1 for line in f)
    return count

def get_account(line):
    line = int(line)
    print "get account from line " , line
    account = linecache.getline("tinypng/accounts.txt", line)
    account = account.replace("\r\n", "")
    account = account.replace("\r", "")
    account = account.replace("\n", "")
    print "try to use "+account
    return account

def get_picpaths(directory):
    file_paths = []  # List which will store all of the full filepaths.

    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to from the full filepath.
            filepath = os.path.join(root, filename)
            if not in_compressed_list(filepath,directory) and not in_white_list(filepath,directory) and 'intermediates' not in filepath and '.9' not in filepath:
                file_paths.append(filepath)

    return file_paths

# ignore all files in tinypng/white_list.txt


def in_white_list(filepath,cwd):
    if not os.path.isfile("tinypng/white_list.txt"):
        return False
    filepath=filepath.replace(cwd,'')
    if filepath in open("tinypng/white_list.txt").read():
        print "*******"+ filepath + "******* in white_list , ignore"
        return True
    else:
        return False

# ignore all files had been compressed


def in_compressed_list(filepath,cwd):
    if not os.path.isfile("tinypng/compressed_file_list.txt"):
        return False
    filepath=filepath.replace(cwd,'')
    if filepath in open("tinypng/compressed_file_list.txt").read():
        print "====== " + filepath + " ====== in compressed_file_list , ignore"
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
    
def tiny(f,cwd):
    try:
        tinify.from_file(f).to_file(f)
        append_compressed_file(f,cwd)
        print "tinypng " + f
    except AccountError,e:
        print "AccountError .. "+e.message
        global line
        global account_sum
        if(line > account_sum):
            print "All counts tried , finish"
            return False
        else:
            tinify.key = get_account(line)
            line = line + 1
            tiny(f,cwd)
    except ClientError:
        print "ClientError .."
        return False
    except ServerError:
        print "ServerError .."
        return False
    except ConnectionError:
        print "ConnectionError .."
        return False
    
    return True


#cd to projectDir(tinypng parentDir)
os.chdir('..')

line = 1
account_sum = get_account_count()
tinify.key = get_account(line)
print "key:"+tinify.key
line = line+1
cwd=os.getcwd()
full_pic_paths = get_picpaths(cwd)

types = ['.png', '.jpg']
finish = False
for f in full_pic_paths:
    if finish:
        break
    for i in types:
        if i in f:
            if(not tiny(f,cwd)):
                finish = True
                break
            
