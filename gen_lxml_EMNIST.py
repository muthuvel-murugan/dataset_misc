import lxml.etree
import lxml.builder
import argparse
import os
from PIL import Image

def gn_annot(fo_n, fl_n, pt, s_w, s_h, s_d, name, xmin, xmax, ymin, ymax, op_fname=None):

    E = lxml.builder.ElementMaker()
    ANOT = E.annotation
    FOLD = E.folder
    FNAME = E.filename
    PATH = E.path
    SRC = E.source
    DB = E.database
    SIZE = E.size
    WD = E.width
    HT = E.height
    DP = E.depth
    SEG = E.segmented
    OBJ = E.object
    NAME = E.name
    POSE = E.pose
    TRUNC = E.truncated
    DIFF = E.difficult
    BND = E.bndbox
    XMIN = E.xmin
    XMAX = E.xmax
    YMIN = E.ymin
    YMAX = E.ymax
    
    the_doc = \
        ANOT(
            FOLD(fo_n),
            FNAME(fl_n),
            PATH(pt),
            SRC(
                DB('EMNIST')
                ),
            SIZE(
                WD(s_w),
                HT(s_h),
                DP(s_d)
                ),
            SEG('0'),
            OBJ(
                NAME(name),
                POSE('Unspecified'),
                TRUNC('1'),
                DIFF('0'),
                BND(
                    XMIN(xmin),
                    XMAX(xmax),
                    YMIN(ymin),
                    YMAX(ymax)),
                )
            )

    #print lxml.etree.tostring(the_doc, pretty_print=True)
    if op_fname != None:
        with open(op_fname, 'w') as f:
            f.write(lxml.etree.tostring(the_doc, pretty_print=True))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip_folder_name', type=str, required=True, 
        help='Top level folder name')
    parser.add_argument('--op_folder_name', type=str, required=True,
        help='The output folder name, where the xmls will be stored.')

    args = parser.parse_args()

    print args
    
    # for each png file in the folder(recursively) call
    for root, subdirs, files in os.walk(args.ip_folder_name):
        print root, '- Started .... ',
        for fl_n in files:
            if fl_n[-3:] == 'png':
                file_path = os.path.join(root, fl_n)
                #im = Image.open(file_path)
                xml_fname = os.path.join(args.op_folder_name , file_path.split('/')[-1][:-3] + 'xml')
                s_w, s_h = map(str, (28, 28))  #map(str, im.size)
                s_d = 1  #3 if im.mode == 'YCbCr' else len(im.mode)
                s_d = str(s_d)
        
                name = fl_n.split('_')[1]

                xmin, ymin, xmax, ymax =  map(str, (0, 0, 28, 28))  #map(str, im.getbbox())

                abs_path = os.path.join(os.path.abspath(root), root)

                gn_annot(abs_path, fl_n, abs_path, s_w, s_h, s_d, name, xmin, xmax, ymin, ymax, xml_fname)
        print 'Done'
