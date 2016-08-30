import tinify
import os


#===============tinypng python scripts for android=================== 
# step 1: run "pip install --upgrade tinify"
# step 2: change your tinypng key
# step 3: copy this file to your project res dir, run "python tinyPics.py"
#===============tinypng python scripts for android=================== 


#tinify.key = 'your key'

def get_picpaths(directory):
    file_paths = []  # List which will store all of the full filepaths.

    for root, directories, files in os.walk(directory):
	for filename in files:
	    # Join the two strings in order to form the full filepath.
	    filepath = os.path.join(root, filename)
            if 'drawable' in filepath and not in_compressed_list(filepath) and 'intermediates' not in filepath and '.9.png' not in filepath:
	      file_paths.append(filepath)
   
    return file_paths

def in_compressed_list(filePath):
    re = filePath in open('compressed_file_list.txt').read()
    if re:
	print filepath+" in compressed_file_list"
    return re

def append_compressed_file(filePath):
    fp = open("compressed_file_list.txt","a+")
    fp.write(filePath+"\n")
    fp.flush()
    fp.close()


full_pic_paths = get_picpaths(os.getcwd())

types=['.png','.jpg']

for f in full_pic_paths:
    for i in types:
      if i in f:
        print "tinypng "+f
#        tinify.from_file(f).to_file(f)
        append_compressed_file(f)
