import tinify
import os

tinify.key = 'your key'

def get_filepaths(directory):
    file_paths = []  # List which will store all of the full filepaths.

    for root, directories, files in os.walk(directory):
	for filename in files:
	    # Join the two strings in order to form the full filepath.
	    filepath = os.path.join(root, filename)
	    file_paths.append(filepath) 
   
    return file_paths

full_file_paths = get_filepaths(os.getcwd())

types=['.png','.jpg']

for f in full_file_paths:
  if 'drawable' in filepath and 'intermediates' not in filepath:
    for i in types:
      if i in f and '.9.png' not in f:
        print "tinypng "+f
        tinify.from_file(f).to_file(f)
