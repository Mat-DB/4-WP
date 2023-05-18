from haversine import haversine, Unit
import matplotlib.pyplot as plt
import numpy
import miniball
import math

def f_haversineCircle(straal, middelpunt, message):
    pointA = (middelpunt)
    pointB = (middelpunt[0], (middelpunt[1]+straal))
    afstand = haversine(pointA, pointB, unit=Unit.METERS)
    print("{message}: straal={distance1:1.4f}m, diameter={distance2:1.4f}m".format(message=message, distance1=afstand, distance2=2*afstand))
    print("{message}middelpunt: longitude={distance1:f}°, latitude={distance2:f}°".format(message=message, distance1=middelpunt[0], distance2=middelpunt[1]))

def f_haversinePoints(center1, center2, message):
    pointA = (center1)
    pointB = (center2)
    afstand = haversine(pointA, pointB, unit=Unit.METERS)
    print("{message}: distance={distance:1.4f}m".format(message=message, distance=afstand))

def f_removeOutliers(dataFrame):
    Q1 = dataFrame.quantile(0.25)
    Q3 = dataFrame.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5*IQR
    upper = Q3 + 1.5*IQR
    lower_lat = numpy.where(dataFrame["latitude"] <= lower["latitude"])[0]
    upper_lat = numpy.where(dataFrame["latitude"] >= upper["latitude"])[0]
    lower_long = numpy.where(dataFrame["longitude"] <= lower["longitude"])[0]
    upper_long = numpy.where(dataFrame["longitude"] >= upper["longitude"])[0]
    index_arr = numpy.concatenate((lower_lat, lower_long, upper_lat, upper_long))
    # print("index_arr")
    # print(index_arr)
    newDataFrame = dataFrame.drop(index=index_arr)
    return newDataFrame

def f_removeOutliers2(dataFrame):
    Q1 = dataFrame.quantile(0.25)
    Q3 = dataFrame.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5*IQR
    upper = Q3 + 1.5*IQR
    newDataFrame = dataFrame.drop(dataFrame[ (dataFrame["latitude"] <= lower["latitude"]) | (dataFrame["latitude"] >= upper["latitude"]) | (dataFrame["longitude"] <= lower["longitude"]) | (dataFrame["longitude"] >= upper["longitude"])  ].index)
    return newDataFrame

def f_circumscribe(dataFrame):
    bBox = [ [dataFrame["longitude"].min(), dataFrame["latitude"].min()], [dataFrame["longitude"].max(), dataFrame["latitude"].max()] ]
    arr = numpy.asarray(bBox)
    C, r2 = miniball.get_bounding_ball(arr, epsilon=1e-7)
    straal = math.sqrt(r2)
    circle = plt.Circle(tuple(C), straal, color='r', fill=False)
    return circle

def f_plotCircles(circles):
    # gca = get current axis
    plt.gca().set_aspect(1)
    box = (4.411500, 4.42, 51.177, 51.18) # map2.png
    # box = (4.4114, 4.4195, 51.1766, 51.1817) # map3.png
    plt.xlim(box[0], box[1])
    plt.ylim(box[2], box[3])
    colours = ["b", "r", "g", "y", "c", "m"]
    for i in range(len(circles)):
        circle = circles[i]
        circle.set_edgecolor(colours[i])
        plt.gca().add_patch(circle)

def f_plotCircle(circle, color):
    # gca = get current axis
    plt.gca().set_aspect(1)
    box = (4.411500, 4.42, 51.177, 51.18) # map2.png
    # box = (4.4114, 4.4195, 51.1766, 51.1817) # map3.png
    plt.xlim(box[0], box[1])
    plt.ylim(box[2], box[3])
    circle.set_edgecolor(color)
    plt.gca().add_patch(circle)

def f_plotCirclesWithCenter(circles):
    # gca = get current axis
    plt.gca().set_aspect(1)
    box = (4.411500, 4.42, 51.177, 51.18) # map2.png
    # box = (4.4114, 4.4195, 51.1766, 51.1817) # map3.png
    plt.xlim(box[0], box[1])
    plt.ylim(box[2], box[3])
    colours = ["b", "r", "g", "y", "c", "m"]
    for i in range(len(circles)):
        circle = circles[i]
        circle.set_edgecolor(colours[i])
        plt.gca().add_patch(circle)
        center = (circle.get_center())
        plt.scatter(center[0], center[1], color=colours[i], zorder=1, alpha=1, s=5)


def f_switchColumns(dataFrame):
    cols = list(dataFrame.columns)
    a, b = cols.index("latitude"), cols.index("longitude")
    cols[b], cols[a] = cols[a], cols[b]
    dataFrame = dataFrame[cols]
    return dataFrame

def f_plotMap(imageName):
    box = (4.411500, 4.42, 51.177, 51.18) # map2.png
    # box = (4.4114, 4.4195, 51.1766, 51.1817)  # map3.png
    ruh_m = plt.imread(imageName)
    aspect = 1
    #plt.imshow(ruh_m, zorder=0, extent=box, aspect=aspect)
    plt.imshow(ruh_m, zorder=0, extent=box, aspect=aspect)
