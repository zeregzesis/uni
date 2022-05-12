from numpy import ones, vstack
from numpy.linalg import lstsq
from pickle import dump, load
import math

##############################################################################################################################

def saveToFile(x, y, args, funcName, filename):
    dump((x, y, funcName, args), open(filename, 'wb'))

def loadFromFile(filename):
    return load(open(filename, 'rb'))

##############################################################################################################################

def roundPartial (value, resolution):
    return round (value / resolution) * resolution

def linFunc(p1 ,p2):
    points = [p1,p2]
    x_coords, y_coords = zip(*points)
    A = vstack([x_coords,ones(len(x_coords))]).T
    a, b = lstsq(A, y_coords, rcond=None)[0]
    return lambda x: a*x + b

##############################################################################################################################

def MSE(y, y_hat):
    """
    Mean Squared Error
    """
    return sum([(y[i] - y_hat[i])**2 for i in range(len(y))]) / len(y)

def SNR(y, y_hat):
    """
    Signal to Noise Ratio
    """
    try:
        return 10 * math.log10(sum([y[i]**2 for i in range(len(y))]) / MSE(y, y_hat))
    except:
        return 100

def PSNR(y, y_hat):
    """
    Peak Signal to Noise Ratio
    """
    try:
        return 10 * math.log10(max(y)**2 / MSE(y, y_hat))
    except:
        return 100

def MD(y, y_hat):
    """
    Maximum Difference
    """
    return max([abs(y[i] - y_hat[i]) for i in range(len(y))])

def getAllMetrics(y, y_hat):
    """
    Returns all metrics
    """
    return {
        'MSE': MSE(y, y_hat),
        'SNR': SNR(y, y_hat),
        'PSNR': PSNR(y, y_hat),
        'MD': MD(y, y_hat)
    }