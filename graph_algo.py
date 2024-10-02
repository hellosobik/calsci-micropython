from math import *
def fun(x):
    return sin(x)
resolution=7
x_range=2*resolution
y_range=1*resolution
x_dots=64
y_dots=32

for i in range(x_dots):
    x_value=i*x_range/x_dots
    j=y_dots*fun(x_value)/y_range
    print("x_dot = ",i," y_dot = ",int(j), " x_value = ",x_value, " y_value = ",fun(x_value))
print("")
for i in range(x_dots):
    x_value=-i*x_range/x_dots
    j=y_dots*fun(x_value)/y_range
    print("x_dot = ",-i," y_dot = ",int(j), " x_value = ",x_value, " y_value = ",fun(x_value))
