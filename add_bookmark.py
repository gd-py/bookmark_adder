import re
from PyPDF4 import PdfFileWriter, PdfFileReader
import sys

file_writer = PdfFileWriter()
pdf_file = PdfFileReader('old_file.pdf')
for i in range(pdf_file.getNumPages()-1):
    file_writer.addPage(pdf_file.getPage(i))

with open(input("Enter contents file name: ")+'.txt', 'r') as fh:
    contents = fh.read()
lines = contents.strip().split('\n')
page_offset = int(input("Enter page offset: "))
tree_nav = {}
for line in lines:
    n_tabs = len(re.findall('\\t', line))
    line = line.strip()
    _x = line[::-1].split(' ', 1)
    try:
        page = int(_x[0][::-1]) + page_offset
    except:
        print(_x[::-1])
        sys.exit()
    bookmark_name = _x[1].lstrip()[::-1]
    if n_tabs == 0:
        bookmark = file_writer.addBookmark(bookmark_name, page)
        tree_nav[n_tabs] = bookmark
    else:
        bookmark = file_writer.addBookmark(bookmark_name, pagenum=page, parent=tree_nav[n_tabs-1])
        tree_nav[n_tabs] = bookmark

with open('new_file.pdf', 'wb') as fh:
    file_writer.write(fh)
