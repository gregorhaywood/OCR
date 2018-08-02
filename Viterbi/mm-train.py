#! /usr/bin/env python3

import viterbi as vb

_INTERVAL = 5

def main(model, out, files):
    """
    model is a vb Model 
    out is a path to a directory
    files is a list of paths to bin.imgs
    """
    for i in range(1, len(files)+1):
        train(model, files[i-1])
        if i%_INTERVAL == 0:
            fname = "{0}/{1:04d}.csv".format(out, i)
            model.store(fname)
            print("Saved: {0}".format(fname))

def train(model, imgPath):
    
    # validate path
    if imgPath[-8:] != ".bin.png":
        print("Invalid Path: {0}".format(imgPath))
        return
    path = imgPath[:-8]
    
    # transcription
    with open(path + ".gt.txt") as f:
        line = f.read()[:-1]
    if len(line) == 0:
        print("No text: {0}".format(imgPath))        
        return

    # image
    _,_,img = vb.openImg(path + ".bin.png")
    model.train(line, img)
    print("Trained on {0}".format(imgPath))
    print("\t\"{0}\"".format(line))
    
    
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="""
            Train a model, or reate a new one.""")
        
    # 1 or more image file names
    parser.add_argument("files", type=str, nargs="+", metavar="FILE",
                        help="""A list of .bin.png files to train the model on. 
                        FILE.bin.png FILE.gt.txt must both exist""")
    # 1 model filename, optional
    parser.add_argument("-m", "--model", dest="model", action="store",
                        type=str, required=True,
                        help="A model to train further.")
    # 1 model filename, requierd
    parser.add_argument("-o", dest="out", action="store",
                        type=str, required=True,
                        help="The output directory")

    args = parser.parse_args()
    model = vb.Model("o", args.model)
    main(model, args.out, args.files)
    
    
    
