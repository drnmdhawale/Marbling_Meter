# This code was written by Nandkshor Motiram Dhawale, PhD On June 22nd 2016.
# This code is written Capture image and analyse food object using pi camera on raspberry pi platform
# The problem statement was given by the my Post doctoral advisor Dr. M. Ngadi from Department of
# Bioresource Engineering at McGill University, Macdonalds Campus. Ste-Anne-de-Bellevue, QC. Canada

"Compute tcsRatio"
import numpy as np

def test_tcsRatio (g, contourP, C2, distratio):
    Xsp = contourP[0,:] - distratio * (contourP[0,:] - C2[0])
    Ysp = contourP[1,:] - distratio * (contourP[1,:] - C2[1])
    contourSP = np.array([np.around(Xsp), np.around(Ysp)]).astype(np.float64)

    return contourSP
