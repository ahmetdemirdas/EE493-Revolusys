import random
import numpy
import matplotlib.pyplot as plt


def sensor_real_distance(intended_distance, sd_type):
    real_distance_values = [3, 5, 7, 10, 15, 20, 30, 50, 100, 150] # cm
    measured_distance_mean = [3.80, 4.87, 6.82, 10.33, 16.60, 20.39, 29.56, 49.08, 97.68, 147.49] # cm
    constant_sd = 0.1 # Constant standard deviation can be arraged here.
    exp_sd = [0.04, 0.05, 0.05, 0.22, 0.12, 0.07, 0.13, 0.11, 0.41, 0.41]
    if sd_type == "constant":
        measured_sd = constant_sd * numpy.ones(len(real_distance_values))
    elif sd_type == "experimental":
        measured_sd = exp_sd
    mean_fit = numpy.polyfit(real_distance_values, measured_distance_mean, 5)
    sd_fit = numpy.polyfit(real_distance_values, measured_sd, 5)
    distance_function = numpy.poly1d(mean_fit)
    sd_function = numpy.poly1d(sd_fit)
    real_distance = random.normalvariate(distance_function(intended_distance), sd_function(intended_distance))
    # The following 12 lines are written to observe the behaviour of the fitted functions in usage range. Optimum
    # fitting degree is found as 5.
    # mean = numpy.zeros(1501)
    # sd = numpy.zeros(1501)
    # for i in range(1501):
    #     mean[i] =distance_function(i/10)
    #     sd[i] =sd_function(i/10)
    # x_axis = numpy.linspace(0, 150, num=1501)
    # plt.figure()
    # plt.plot(x_axis, mean, "-")
    # plt.savefig("mean_sensor.png")
    # plt.figure()
    # plt.plot(x_axis, sd, "-")
    # plt.savefig("sd_sensor.png")
    return real_distance
