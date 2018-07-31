



"""

Should take in a model and list of files to process

Initially, also take an output directory

Do more to fit with ocropus framework

"""



DIVIDE = 30

def main(model, out, files):
    m = Model( "o", model)
    for f in files:
    
        # get trans and img
        try:
            with open(path + ".txt") as f:
                line = f.read()[:-1]
        except FileNotFoundError:
            with open(path + ".txt") as f:
                line = f.read()[:-1]            
        if len(line) == 0:
            return
        s, e, img = openImg(file + ".bin.png")
        
        # results
        results, p = m.fit(line, img)
    

def openImg(path):
    """
    Open an image, and return an array of counts of black 
    pixels in each column. Also trims white space and noise 
    at then begining and and end of the line.
    """
    img = np.array(imread(path))
    counts = list(map(lambda x: len(img)-x.sum(), img.transpose()))
    
    # trim start and end
    start = 0
    while (counts[start] == 0): start += 1
    buf = start
    while (counts[buf] != 0): buf += 1
    white = buf
    while (counts[white] == 0): white += 1
    if white-buf > DIVIDE:
        start = white

    end = len(counts)
    while (counts[end-1] == 0): end -= 1
    buf = end
    while (counts[buf-1] != 0): buf -= 1
    white = buf
    while (counts[white-1] == 0): white -= 1
    if buf-white > DIVIDE:
        end = white
        
        
    return start, end, counts[start:end]
    



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="""
            Use an mm model to find spaces on a transcription line.
        """)
        
    # 1 or more image file names
    parser.add_argument("files", type=str, nargs="+", metavar="FILE",
                        help="""A file to fit the model to. FILE.bin.png and FILE.txt 
                        or FILE.gt.txt must both exist""")
    # 1 model filename, requierd
    parser.add_argument("-m", "--model", dest="model", action="store",
                        type=str, required=True,
                        help="Specify the model to use (required)")
    # 1 optional output directory    
    parser.add_argument("-o", dest="out", action="store",
                        type=str, default="./",
                        help="Output directory (optional)")

    args = parser.parse_args()
    print(args.files)
    print(args.model)
    print(args.out)
    # TODO add args here
    # main(args.model, arfs.out, args.files)