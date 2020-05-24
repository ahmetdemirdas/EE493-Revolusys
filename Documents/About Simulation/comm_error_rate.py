import random
import numpy
import matplotlib.pyplot as plt


def communication_error_rate(environment, real_distance, sd_type):
    real_distance_values = [0, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 30, 45] # cm
    measured_error_rate_mean_light = [0, 1.04, 1.11, 1.22, 1.32, 1.82, 2.17, 2.54, 2.93, 3.32, 3.69, 4.13, 6.13, 8.78,
                                      19.77] # percentage
    measured_error_rate_mean_dark = [0, 1.02, 1.10, 1.22, 1.33, 1.79, 1.63, 2.02, 2.44, 2.88, 3.62, 4.01, 5.11, 6.54,
                                     12.06] # percentage
    constant_sd = 0.01 # Constant standard deviation can be arranged here.
    exp_sd_light = []  # I couldn't find related data yet.
    exp_sd_dark = []  # I couldn't find related data yet.
    if sd_type == "constant":
        measured_sd = constant_sd * numpy.ones(len(real_distance_values))
    elif sd_type == "experimental":
        if environment == "light":
            measured_sd = exp_sd_light
        elif environment == "dark":
            measured_sd = exp_sd_light
    if environment == "light":
        measured_error_rate_mean = measured_error_rate_mean_light
    elif environment == "dark":
        measured_error_rate_mean = measured_error_rate_mean_dark
    mean_fit = numpy.polyfit(real_distance_values, measured_error_rate_mean, 3)
    sd_fit = numpy.polyfit(real_distance_values, measured_sd, 3)
    error_function = numpy.poly1d(mean_fit/100) # normalizing percentage
    sd_function = numpy.poly1d(sd_fit)
    error_rate = random.normalvariate(error_function(real_distance), sd_function(real_distance))
    # # The following 12 lines are written to observe the behaviour of the fitted functions in usage range. Optimum
    # # fitting degree is found as 3.
    # mean = numpy.zeros(451)
    # sd = numpy.zeros(451)
    # for i in range(451):
    #     mean[i] =error_function(i/10)
    #     sd[i] =sd_function(i/10)
    # x_axis = numpy.linspace(0, 45, num=451)
    # plt.figure()
    # plt.plot(x_axis, mean, "-")
    # plt.savefig("mean_comm.png")
    # plt.show()
    # plt.figure()
    # plt.plot(x_axis, sd, "-")
    # plt.savefig("sd_comm.png")
    return error_rate
