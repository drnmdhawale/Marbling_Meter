"Compute the geometric centroid"
import numpy as np

def test_centroid(I, contourP):
    x = 0
    mx1 = 0
    mx2 = 0
    y = 0
    my1 = 0
    my2 = 0
    mt1 = 0
    mt2 = 0
    [m,n] = np.shape(contourP)
    gray_I= np.mean(I)
    w = np.array([]).astype(np.float64)
    iw = np.array([]).astype(np.float64)
    #print np.shape(contourP)
    for c in range(0, n):
        #print c
        x = contourP[0, c] + x
        y = contourP[1, c] + y
        #print I[contourP[1, c], contourP[0, c]]

        #w = I[contourP[1, c], contourP[0, c]].astype(np.float64)
        w = I[contourP[1, c], contourP[0, c]]
        #print w
        mx1 = w*contourP[0,c] + mx1
        my1 = w*contourP[1,c] + my1
        mt1 = w + mt1
        #print mt1

        #iw = 255 - I[contourP[1, c], contourP[0, c]].astype(np.float64)
        iw = 255 - I[contourP[1, c], contourP[0, c]]
        #print w
        mx2 = iw*contourP[0,c] + mx2
        my2 = iw*contourP[1,c] + my2
        mt2 = iw + mt2
        #print mt2
    C0 = np.array([round(x/n), round(y/n)])
    C1 = np.array([round(mx1/mt1), round(my1/mt1)])
    C2 = np.array([round(mx2/mt2), round(my2/mt2)])
    d = np.sqrt(np.power((C0[0] - C1[0]),2) + np.power((C0[1] - C1[1]),2))

    return C0, C1, C2, d
