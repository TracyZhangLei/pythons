import tinify
import os


#===============tinypng python scripts for android=================== 
# step 1: run "pip install --upgrade tinify"
# step 2: change your tinypng key
# step 3: copy this file to your project res dir, run "python tinyPics.py"
#
#
# tips 1: image files will be add to compressed_file_list.txt automatically
# tips 2: (optional)image files(absolute paths) in white_list.txt will be ignored if you do not want to compress them
#
#
#===============tinypng python scripts for android=================== 


tinify.key = 'your key'

def get_picpaths(directory):
    file_paths = []  # List which will store all of the full filepaths.

    for root, directories, files in os.walk(directory):
	for filename in files:
	    # Join the two strings in order to form the full filepath.
	    filepath = os.path.join(root, filename)
            if not in_compressed_list(filepath) and not in_white_list(filepath) and 'intermediates' not in filepath and '.9' not in filepath:
	      file_paths.append(filepath)
   
    return file_paths

#ignore all files in white_list.txt
def in_white_list(filepath):
    if not os.path.isfile("white_list.txt"):
        return False
    if filepath in open("white_list.txt").read():
	print "******* "+filepath+" ******* in white_list , ignore"
        return True
    else:
        return False

#ignore all files had been compressed
def in_compressed_list(filepath):
    if not os.path.isfile("compressed_file_list.txt"):
        return False
    if filepath in open("compressed_file_list.txt").read():
	print "====== "+filepath+" ====== in compressed_file_list , ignore"
        return True
    else:
        return False

#record file to compressed_file_list.txt
def append_compressed_file(filepath):
    fp = open("compressed_file_list.txt","a+")
    fp.write(filepath+"\n")
    fp.flush()
    fp.close()


full_pic_paths = get_picpaths(os.getcwd())

types=['.png','.jpg']

for f in full_pic_paths:
    for i in types:
      if i in f:
        print "tinypng "+f
        tinify.from_file(f).to_file(f)
        append_compressed_file(f)
