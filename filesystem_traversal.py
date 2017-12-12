#import os
#
#rootDir = '/'
# for dirName, subdirList, fileList in os.walk(rootDir):
#    print('Found directory: %s' % dirName)
#    for fname in fileList:
#        print('\t%s' % fname)

import os
import magic

img = ['.jpg', '.jpeg', '.png', '.tiff', '.gif']
mov = ['.m4v', '.mp4', '.mov']
text = ['.doc', '.txt', '.docx', '.pdf', '.input', '.output', '.in', '.pptx']
dev = ['.html', '.xml', '.css', '.js', '.py', '.c', '.h', '.java', '.rb', '.ml', '.m', '.csh']

file_types = []
file_extensions = []

rootDir = '/Users/zach/Documents/QFS'

parent = "new"

visited = []

for dirName, subdirList, fileList in os.walk(rootDir):
    print(dirName)

    c = 0
    for fname in fileList:
        dagr_name = dirName.split("/")[-1]
        #print(dirName + '/' + fname)

            # print(dirName)
        #print(dirName + "/" + fname)
        # ft = magic.from_file(dirName + '/' + fname)
        # if ft not in file_types and ft != 'empty':
        #     file_types.append(ft)
        # fn,fe = os.path.splitext(dirName + '/' + fname)
        # if fe not in file_extensions and fe != '':
        #     file_extensions.append(fe)

# for f in file_extensions:
#     print(f)
