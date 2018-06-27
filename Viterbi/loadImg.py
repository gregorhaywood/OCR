from matplotlib.image import imread, imsave
import numpy as np
from hmmlearn import hmm

# Return True for black cells
def isChar(x):
    if x==0:
        return True
    else:
        return False

def makeHeatMap(fname):
    img = np.array(imread(fname))

    output =[]
    for col in img.transpose():
        val = 1-col.sum()/len(img)
        output.append(list(map(
            lambda x: [0.0,0.0,0.0,1.0] if isChar(x) else [1.0,0.0,0.0,val],
            col)))

    imsave("Data/heat.png", np.array(output).transpose(1,0,2), format="png")


def runHMM(fname):
    img = np.array(imread(fname))
    counts = list(map(lambda x: [len(img)-x.sum()], img.transpose()))

    model = hmm.GaussianHMM(n_components=6, n_iter=100, init_params="mcs")
    model.transmat_ = np.array([[0.5, 0.1, 0.1, 0.1, 0.1, 0.1],
                                [0.1, 0.5, 0.1, 0.1, 0.1, 0.1],
                                [0.1, 0.1, 0.5, 0.1, 0.1, 0.1],
                                [0.1, 0.1, 0.1, 0.5, 0.1, 0.1],
                                [0.1, 0.1, 0.1, 0.1, 0.5, 0.1],
                                [0.1, 0.1, 0.1, 0.1, 0.1, 0.5]])


    model.fit(counts[:120])
    results = model.predict(counts)

    output =[]
    trans = img.transpose()
    def c(col):
        if results[col] == 0:
            return [1.0,0.0,0.0,1.0]
        if results[col] == 1:
            return [0.0,1.0,0.0,1.0]
        if results[col] == 2:
            return [0.0,0.0,1.0,1.0]
        if results[col] == 3:
            return [1.0,1.0,0.0,1.0]
        if results[col] == 4:
            return [0.0,1.0,1.0,1.0]
        else:
            return [1.0,0.0,1.0,1.0]

    for col in range(len(trans)):
        val = 1-trans[col].sum()/len(img)
        output.append(list(map(
            lambda x: [0.0,0.0,0.0,1.0] if isChar(x) else c(col),
            trans[col])))

    imsave("Data/results.png", np.array(output).transpose(1,0,2), format="png")

# TODO
# improve GUI/integration


# Work from there

# make model (easier said)

# need to make model with correct emission probabilities (log-normal)
# initially jusst get something working, don't worry about character models

# Show predicted letter and section in gui


# makeHeatMap("Data/img.png")
runHMM("Data/img.png")
