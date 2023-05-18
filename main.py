import pandas as pd
import matplotlib.pyplot as plt
import circle_fit

import helperFunctions

def f_initData(experimentNR, locatie):
    if (locatie=="middelheim"):
        file = "Location-Middelheim_Experiment-"+ experimentNR + "-Parsed.txt"
    elif (locatie=="tussenGebouwen"):
        file = "Location-TussenGebouwen_Experiment-" + experimentNR + "-Parsed.txt"
    elif (locatie=="veld"):
        file = "Location-OpenVeld_Experiment-" + experimentNR + "-Parsed.txt"
    elif (locatie=="onderAfdak"):
        file = "Location-OnderAfdak_Experiment-" + experimentNR + "-Parsed.txt"
    else:
        print("Invalid location! Default middelheim")
        file = "Location-Middelheim_Experiment-"+ experimentNR + "-Parsed.txt"

    dataFrameArdu = pd.read_csv("arduino/" + file, sep=';')
    dataFrameSep = pd.read_csv("septentrio/" + file, sep=';')
    dataFrameGSM = pd.read_csv("gnss/" + file, sep=';')
    dataFrameArdu = helperFunctions.f_switchColumns(dataFrameArdu)
    dataFrameSep = helperFunctions.f_switchColumns(dataFrameSep)
    dataFrameGSM = helperFunctions.f_switchColumns(dataFrameGSM)
    return dataFrameSep, dataFrameGSM, dataFrameArdu

def f_plotOnMap(dataFrameArdu, dataFrameGSM, dataFrameSep):
    bBox = (dataFrameArdu["longitude"].min(), dataFrameArdu["longitude"].max(), dataFrameArdu["latitude"].min(), dataFrameArdu["latitude"].max())
    box = (4.411500, 4.42, 51.177, 51.18) # map2.png
    ruh_m = plt.imread("map2.png")
    #aspect = 734/413
    aspect = 1
    print(aspect)
    plt.imshow(ruh_m, zorder=0, extent=box, aspect=aspect)
    plt.scatter(dataFrameArdu["longitude"], dataFrameArdu["latitude"], zorder=1, alpha=0.2, c='b', s=10)
    plt.scatter(dataFrameSep["longitude"], dataFrameSep["latitude"], zorder=1, alpha=0.2, c='r', s=10)
    plt.scatter(dataFrameGSM["longitude"], dataFrameGSM["latitude"], zorder=1, alpha=0.2, c='g', s=10)
    plt.title("GPS metingen middelheim park.")
    plt.xlim(box[0], box[1])
    plt.ylim(box[2], box[3])

def f_circleFit(dataList):
    xc, yc, r, sigma = circle_fit.taubinSVD(dataList)
    circle_fit.plot_data_circle(dataList, xc, yc, r)

def main():
    mid = "middelheim"
    geb = "tussenGebouwen"
    veld = "veld"
    z = "onderAfdak"
    locatie = z
    #------------------------------------------------------------
    # Initialize dataframes
    #------------------------------------------------------------
    dataFrameSep1, dataFrameGSM1, dataFrameArdu1 = f_initData("1", locatie)
    dataFrameSep2, dataFrameGSM2, dataFrameArdu2 = f_initData("2", locatie)

    dataFrameArduTot = dataFrameArdu1.append(dataFrameArdu2)
    dataFrameGSMTot = dataFrameGSM1.append(dataFrameGSM2)
    dataFrameSepTot = dataFrameSep1.append(dataFrameSep2)
    # print(dataFrameSepTot.head(5))
    # print()

    #------------------------------------------------------------
    # Kies de gewenste dataframes
    #------------------------------------------------------------
    dataFrameArdu = dataFrameArdu2
    dataFrameSep = dataFrameSep2
    dataFrameGSM = dataFrameGSM2
    expNR="2"

    #------------------------------------------------------------
    # Make lists from dataframes for circle fit
    #------------------------------------------------------------
    # sepList = dataFrameSep1.values.tolist()
    # gsmList = dataFrameGSM1.values.tolist()
    # arduList = dataFrameArdu1.values.tolist()
    # gpsList = gsmList

    #------------------------------------------------------------
    # Circle fit
    #------------------------------------------------------------
    #f_plotOnMap(dataFrameArdu1, dataFrameGSM1, dataFrameSep1)
    #f_circleFit(gpsList)
    #f_circumscribe(dataFrameSep1)

    #------------------------------------------------------------
    # Remove outliers from dataframes
    #------------------------------------------------------------
    dfArduClean = helperFunctions.f_removeOutliers2(dataFrameArdu)
    dfSepClean = helperFunctions.f_removeOutliers2(dataFrameSep)
    dfGSMClean = helperFunctions.f_removeOutliers2(dataFrameGSM)

    #------------------------------------------------------------
    # Kies met of zonder outliers
    #------------------------------------------------------------
    cleanData=False
    if (cleanData):
        dataFrameArdu = dfArduClean
        dataFrameSep = dfSepClean
        dataFrameGSM = dfGSMClean
        print(locatie + " clean " + expNR)
    else:
        print(locatie + " std " + expNR)

    #------------------------------------------------------------
    # Make circles around points in dataframe and append to circles list
    #------------------------------------------------------------
    circles = []
    circles.append(helperFunctions.f_circumscribe(dataFrameArdu))
    circles.append(helperFunctions.f_circumscribe(dataFrameSep))
    circles.append(helperFunctions.f_circumscribe(dataFrameGSM))

    #------------------------------------------------------------
    # Plot circles and center on map or white background
    # Call haversino function to print information
    #------------------------------------------------------------
    # print("Allemaal zonder outliers.")
    text = ["Arduino", "Septentrio", "GSM"]
    # for i in range(len(circles)):
    #     helperFunctions.f_haversineCircle(circles[i].get_radius(), circles[i].get_center(), text[i])
    # helperFunctions.f_plotCirclesWithCenter(circles)
    # helperFunctions.f_plotCircles(circles)
    #helperFunctions.f_plotMap("map3.png")
    colours = ["b", "r", "g", "y", "c", "m"]
    i=2
    print(i)
    helperFunctions.f_haversineCircle(circles[i].get_radius(), circles[i].get_center(), "")
    helperFunctions.f_plotCircle(circles[i], colours[i])

    #------------------------------------------------------------
    # Call haversine function to print information
    #------------------------------------------------------------
    # helperFunctions.f_haversinePoints(circles[0].get_center(), circles[1].get_center(), "Afstand tussen ardu en sep")
    # helperFunctions.f_haversinePoints(circles[1].get_center(), circles[2].get_center(), "Afstand tussen gsm en sep")

    #------------------------------------------------------------
    # Makes scatter plot of dataframes
    # colours = ["b", "r", "g", "y", "c", "m"]
    #------------------------------------------------------------
    if (i==0):
        plt.scatter(dataFrameArdu["longitude"], dataFrameArdu["latitude"], zorder=1, alpha=0.2, c='b', s=10)
    elif (i==1):
        plt.scatter(dataFrameSep["longitude"], dataFrameSep["latitude"], zorder=1, alpha=0.2, c='r', s=10)
    elif (i==2):
        plt.scatter(dataFrameGSM["longitude"], dataFrameGSM["latitude"], zorder=1, alpha=0.2, c='g', s=10)

    plt.show()

if __name__ == '__main__':
    main()

