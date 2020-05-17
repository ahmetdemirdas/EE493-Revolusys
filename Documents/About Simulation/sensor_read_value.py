import random
import numpy
import pickle

def sensor_measured_distance(intended_distance):
    x_values = [3, 5, 7, 10, 15, 20, 30, 50, 100, 150]
    measured_mean = [3.80, 4.87, 6.82, 10.33, 16.60, 20.39, 29.56, 49.08, 97.68, 147.49]
    measured_sd = [0.04, 0.05, 0.05, 0.22, 0.12, 0.07, 0.13, 0.11, 0.41, 0.41]
    z_mean = numpy.polyfit(x_values, measured_mean, 9)
    z_sd = numpy.polyfit(x_values, measured_sd, 9)
    distance_function = numpy.poly1d(z_mean)
    sd_function = numpy.poly1d(z_sd)
    outputted_distance = random.normalvariate(distance_function(intended_distance), sd_function(intended_distance))
    return outputted_distance

print(sensor_measured_distance(15))