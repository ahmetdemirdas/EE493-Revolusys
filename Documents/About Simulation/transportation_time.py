import numpy
import matplotlib.pyplot as plt


def transportation_sim(seperation_distance):
    seperation_values = [150, 100, 50]  # cm
    measured_time = [19.52 / 10, 13.95 / 10, 9.18 / 10]  # seconds
    fit_time = numpy.polyfit(seperation_values, measured_time, 2)
    measured_time_function = numpy.poly1d(fit_time)
    time = measured_time_function(seperation_distance)
    # # The following 12 lines are written to observe the behaviour of the fitted functions in usage range. Optimum
    # # fitting degree is found as 2.
    # time_array = numpy.zeros(1001)
    # for i in range(1001):
    #     time_array[i] =measured_time_function(i/10)
    # x_axis = numpy.linspace(50, 150, num=1001)
    # plt.figure()
    # plt.plot(x_axis, time_array, "-")
    # plt.savefig("transportation_time.png")
    return time, (seperation_distance - 30) / time


time, one_go_time = transportation_sim(50)
print(time, one_go_time)
