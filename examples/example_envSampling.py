import numpy as np
import WDRT.ESSC as ESSC
import copy
import matplotlib.pyplot as plt

# Create buoy object, in this case for Station #46022
buoy46022 = ESSC.Buoy('46022','NDBC')

# Read data from ndbc.noaa.gov
buoy46022.fetchFromWeb()
#buoy46022.loadFromH5('./data/NDBC46022.h5')
buoy46022.saveAsTxt(savePath = ".\Data")
buoy46022.saveAsH5()

# Load data from .txt file if avilable
#buoy46022.loadFromTxt()

# Load data from .h5 file if available
# buoy46022.loadFromH5('./data/NDBC46022.h5')

# Declare required parameters
Time_SS = 1.  # Sea state duration (hrs)
Time_R = 100  # Return periods (yrs) of interest

# Create PCA EA object for the buoy
pca46022 = ESSC.PCA(buoy46022)

# Calculate contour using PCA method
pca_Hs_Return, pca_T_Return = pca46022.getContours(Time_SS, Time_R)

# Show a plot of the data
pca46022.plotData()

# Save data in h5 file
pca46022.saveContour('./data/NDBC%s' % (pca46022.buoy.buoyNum))

# Create EA objects for remaining contour methods
Gauss46022 = ESSC.GaussianCopula(buoy46022)
Gumbel46022 = ESSC.GumbelCopula(buoy46022)
Clayton46022 = ESSC.ClaytonCopula(buoy46022)
rosen46022 = ESSC.Rosenblatt(buoy46022)
NonParaGauss46022 = ESSC.NonParaGaussianCopula(buoy46022)
NonParaClay46022 = ESSC.NonParaClaytonCopula(buoy46022)
NonParaGum46022 = ESSC.NonParaGumbelCopula(buoy46022)

# Calculate contours for all remaining contour methods
Gauss_Hs_Return, Gauss_T_Return = Gauss46022.getContours(Time_SS, Time_R)
Gumbel_Hs_Return, Gumbel_T_Return = Gumbel46022.getContours(Time_SS, Time_R)
Clayton_Hs_Return, Clayton_T_Return = Clayton46022.getContours(Time_SS, Time_R)
rosen_Hs_Return, rosen_T_Return = rosen46022.getContours(Time_SS, Time_R)
NonParaGau_Hs_Return, NonParaGau_T_Return = NonParaGauss46022.getContours(Time_SS, Time_R)
NonParaClay_Hs_Return, NonParaClay_T_Return = NonParaClay46022.getContours(Time_SS, Time_R)
NonParaGum_Hs_Return, NonParaGum_T_Return = NonParaGum46022.getContours(Time_SS, Time_R)

# Plot all contour results for comparison 
f = plt.figure()
f.canvas.set_window_title('NDBC%s, %i-year contours' % (buoy46022.buoyNum, Time_R))
plt.plot(buoy46022.T, buoy46022.Hs, 'bo', alpha=0.1, label='Data')
plt.plot(pca_T_Return, pca_Hs_Return, '-', label='PCA')
plt.plot(Gauss_T_Return, Gauss_Hs_Return, '-', label='Gaussian')
plt.plot(Gumbel_T_Return, Gumbel_Hs_Return, '-', label='Gumbel')
plt.plot(Clayton_T_Return, Clayton_Hs_Return, '-', label='Clayton')
plt.plot(rosen_T_Return, rosen_Hs_Return, '-', label='Rosenblatt')
plt.plot(NonParaGau_T_Return, NonParaGau_Hs_Return, 'g--', label='Non-Parametric Gaussian')
plt.plot(NonParaGum_T_Return, NonParaGum_Hs_Return, 'r--', label='Non-Parametric Gumbel')
plt.plot(NonParaClay_T_Return, NonParaClay_Hs_Return, 'c--', label='Non-Parametric Clayton')
plt.xlabel('Energy period, $T_e$ [s]')
plt.ylabel('Sig. wave height, $H_s$ [m]')
plt.grid(True)
plt.legend(loc='center right', bbox_to_anchor=(1.4,0.5),fontsize=10, fancybox=True)
plt.show()

# Sample Generation Example
num_contour_points = 20  # Number of points to be sampled for each
# contour interval.
contour_returns = np.array([0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50, 100])
# Probabilities defining sampling contour bounds.
random_seed = 2  # Random seed for sample generation

# Get samples for a full sea state long term analysis
Hs_sampleFSS, T_sampleFSS, Weight_sampleFSS = pca46022.getSamples(num_contour_points,
                                                     contour_returns, random_seed)
# Get samples for a contour approach long term analysis
T_sampleCA = np.arange(12, 26, 2)
Hs_sampleCA = pca46022.getContourPoints(T_sampleCA)

# Modify contour by steepness curve if they intersect
# Declare required parameters
depth = 391.4  # Depth at measurement point (m)
SteepMax = 0.07  # Optional: enter estimate of breaking steepness
T_vals = np.arange(0.1, np.amax(buoy46022.T), 0.1)

#Note, if depth is not inputted manually, it will automatically be retrieved from NDBC's website
SteepH = pca46022.steepness(SteepMax, T_vals,depth = depth)
SteepH_Return = pca46022.steepness(SteepMax, pca46022.T_ReturnContours, depth = depth)

Steep_correction = np.where(SteepH_Return < pca46022.Hs_ReturnContours)
Hs_Return_Steep = copy.deepcopy(pca46022.Hs_ReturnContours)
Hs_Return_Steep[Steep_correction] = SteepH_Return[Steep_correction]

pca46022.plotSampleData()

# Calculate bootstrap confidence intervals, commented out due to long run time
# Note that stable bootstrap confidence intervals require large sample sizes
# pca46022.bootStrap(boot_size=10)
# Gauss46022.bootStrap(boot_size=10)
# Gumbel46022.bootStrap(boot_size=10)
# cc46022.bootStrap(boot_size=10)
# rosen46022.bootStrap(boot_size=10)
# NonParaGauss46022.bootStrap(boot_size=10)
# NonParaGauss46022.bootStrap(boot_size=10)
# NonParaGauss46022.bootStrap(boot_size=10)


