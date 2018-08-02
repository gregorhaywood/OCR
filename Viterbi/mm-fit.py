#! /usr/bin/env python3

import xml.etree.ElementTree as xml
import os

import viterbi as vb


def main(model, out, files):
    
    m = vb.Model("o", model)
    for imgPath in files:
        
        # validate path
        if imgPath[-8:] != ".bin.png":
            print("Invalid Path: {0}".format(imgPath))
            continue
        path = imgPath[:-8]
        
        # open boxed.xml and get the boundries for this section
        data_dir, hex_fn = os.path.split(path)
        bin_dir, _ = os.path.split(data_dir)
        tree = xml.parse(bin_dir + "/boxed.xml")
        entry = tree.getroot()[int(hex_fn[2:],16)]
        bounds = entry.attrib
    
        # get trans and img
        # TODO change order
        try:
            with open(path + ".gt.txt") as f:
                line = f.read()[:-1]
                print("Using {0}".format(path + ".gt.txt"))
        except FileNotFoundError:
            with open(path + ".txt") as f:
                line = f.read()[:-1]      
                print("Using {0}".format(path + ".txt"))      
        if len(line) == 0:
            outroot = xml.Element('top')
            outtree = xml.ElementTree(outroot)            
            outtree.write("{0}.xml".format(path), encoding='UTF-8')
            continue
        offset,_, img = vb.openImg(imgPath)
        
        # results
        results, p = m.fit(line, img)
        
        ymin = int(bounds["ymin"])
        ymax = int(bounds["ymax"])
        # include ignored whitespace at start of line
        xmin = int(bounds["xmin"]) + offset
        
        outroot = xml.Element('top')
        outtree = xml.ElementTree(outroot)
        words = line.split(" ")
        words.reverse()
        
        def addWord(first, last):
            child = xml.SubElement(outroot, 'word')
            child.text = words.pop()
            child.set('xmin', str(xmin+first))
            child.set('ymin', str(ymin))
            child.set('xmax', str(xmin+last))
            child.set('ymax', str(ymax))
        
        first = 0
        space = False
        for col in range(len(results)):
            if space:
                if  str(results[col])[0] == " ":
                    continue
                else:
                    space = False
                    first = col
            if str(results[col])[0] == " ":
                addWord(first, col)
                space = True
                
        addWord(first,len(results)-1)
        
        outtree.write("{0}.xml".format(path), encoding='UTF-8')
         
    
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="""
            Use an mm model to find spaces on a transcription line. The resulting
            xml file is saved next to the image.""")
        
    # 1 or more image file names
    parser.add_argument("files", type=str, nargs="+", metavar="FILE",
                        help="""A .bin.png file to fit the model to. FILE.bin.png 
                        and FILE.txt or FILE.gt.txt must both exist""")
    # 1 model filename, requierd
    parser.add_argument("-m", "--model", dest="model", action="store",
                        type=str, required=True,
                        help="Specify the model to use (required)")

    args = parser.parse_args()
    main(args.model, args.out, args.files)