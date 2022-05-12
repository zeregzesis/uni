import math


def MSE(y, y_hat):
    """
    Mean Squared Error
    """
    return sum([(y[i] - y_hat[i])**2 for i in range(len(y))]) / len(y)

def SNR(y, y_hat):
    """
    Signal to Noise Ratio
    """
    return 10 * math.log10(sum([y[i]**2 for i in range(len(y))]) / MSE(y, y_hat))

def PSNR(y, y_hat):
    """
    Peak Signal to Noise Ratio
    """
    return 10 * math.log10(max(y)**2 / MSE(y, y_hat))

def MD(y, y_hat):
    """
    Maximum Difference
    """
    return max([abs(y[i] - y_hat[i]) for i in range(len(y))])

def getAllMetrics(y, y_hat):
    """
    Returns all metrics
    """
    return [MSE(y, y_hat), SNR(y, y_hat), PSNR(y, y_hat), MD(y, y_hat)]