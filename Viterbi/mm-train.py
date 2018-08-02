#! /usr/bin/env python3

import viterbi as vb



def trainOn(model, path):
    dr, fname = os.path.split(path)
    
    # transcription
    with open(path + ".gt.txt") as f:
        line = f.read()[:-1]
    if len(line) == 0:
        return

    # image
    _,_,img = vb.openImg(path + ".bin.png")
        
    m.train(line, img)    
    m.store("Results/" + path + ".csv")
    





# TODO 
# sort dirs
# test
# sort codec creation

if __name__ == "__main__":
    # training input should be a list of image files
    # it should be assumed that the truth versions exist
    m = Model( "c")

    if len(sys.argv) > 1:
        # fit for argv
        os.chdir("Training")
        file = sys.argv[1][9:]
        trainOn(m, file)
    else:
        os.chdir("Training")
        for i in range(1,7):
            files = glob.glob("000{0}/0001/*.txt".format(i))
            files.sort()
            for file in files:
                trainOn(m, file.split(".")[0])
