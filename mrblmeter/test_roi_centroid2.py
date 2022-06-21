"Compute tcsRatio"
import numpy as np

def test_tcsRatio (g, contourP, C2, distratio):
    Xsp = contourP[0,:] - distratio * (contourP[0,:] - C2[0])
    Ysp = contourP[1,:] - distratio * (contourP[1,:] - C2[1])
    contourSP = np.array([np.around(Xsp), np.around(Ysp)]).astype(np.float64)

    return contourSP
