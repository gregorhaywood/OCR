#! /usr/bin/env python3

import xml.etree.ElementTree as xml
import os

import viterbi as vb


def main(model, files):    
    model = vb.Model("o", model)
    for imgPath in files:        
        # validate path
        if imgPath[-8:] != ".bin.png":
            print("Invalid Path: {0}".format(imgPath))
            continue
        path = imgPath[:-8]        
        fitLine(model, path)

def fitLine(model, path):
    
    outroot = xml.Element('top')
    outtree = xml.ElementTree(outroot)   

    # get trans and img
    line = readLine(path)
    if len(line) == 0:         
        outtree.write("{0}.xml".format(path), encoding='UTF-8')
        return
    words = line.split(" ")
    words.reverse()
    
    offset,_, img = vb.openImg(path + ".bin.png")
    
    ymin, ymax, xmin = readXML(path)
    xmin += offset
    
    # results
    results, p = model.fit(line, img)
    
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
        
        
def readLine(path): 
    """Read transcript line"""   
    try:
        with open(path + ".txt") as f:
            print("Using {0}".format(path + ".txt"))      
            return f.read()[:-1]      
    except FileNotFoundError:
        with open(path + ".gt.txt") as f:
            print("Using {0}".format(path + ".gt.txt")) 
            return f.read()[:-1]
            

def readXML(path):
    """Read bounds from boxed.xml"""
    data_dir, hex_fn = os.path.split(path)
    bin_dir, _ = os.path.split(data_dir)
    tree = xml.parse(bin_dir + "/boxed.xml")
    entry = tree.getroot()[int(hex_fn[2:],16)]
    bounds = entry.attrib
    return int(bounds["ymin"]), int(bounds["ymax"]), int(bounds["xmin"])
    
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
    main(args.model, args.files)