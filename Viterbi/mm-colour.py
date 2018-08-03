#! /usr/bin/env python3

import viterbi as vb

def main(model, out, colours, files):    
    for imgPath in files:        
        # validate path
        if imgPath[-8:] != ".bin.png":
            print("Invalid Path: {0}".format(imgPath))
            continue
        path = imgPath[:-8]        
        colourImg(model, path, out, colours)

def colourImg(model, path, out, colours):
    """Colour an image according to state"""
    
    # transcription
    with open(path + ".gt.txt") as f:
        line = f.read()[:-1]
    if len(line) == 0:
        return
    
    # img     
    start,end,img = vb.openImg(path + ".bin.png")
    results, p = model.fit(line, img)
    
    fname = path.split("/")[-1]
    vb.saveImg(results, start, path + ".bin.png", "{0}/{1}.col.png".format(out, fname), colours)
    print("{0}:  {1:.2f}".format(path, p))



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="""
            Use an mm model to find spaces on a transcription line. The resulting
            xml file is saved next to the image.""")
        
    # 1 or more image file names
    parser.add_argument("files", type=str, nargs="+", metavar="FILE",
                        help="A list of .bin.png files to colour")
    # 1 model filename, requierd
    parser.add_argument("-m", "--model", dest="model", action="store",
                        type=str, required=True,
                        help="Specify the model to use (required)")
    # 1 output directory
    parser.add_argument("-o", dest="out", action="store",
                        type=str, required=True,
                        help="The output directory")
    parser.add_argument("-c", "--coloured", dest="colour", action="store_true",
                        help="Colour all states")

    args = parser.parse_args()
    model = vb.Model("o", args.model)
    main(model, args.out, args.colour, args.files)

