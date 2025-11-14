import numpy as np
from scipy.optimize import curve_fit
from scipy.special import factorial

def poisson(x, avg):
    """Define Gaussian distribution function.
    
    Parameters
    ----------
    x : 1D array
        Domain over which the function is calculated.
    avg : 1D array or list
        Average number of occurences

    Returns
    -------
    1D array of Gaussian distribution function for the specified x domain.
    """
    return avg**x*np.exp(-x)/factorial(x)

def gaussian(x, amp, mean, sigma, c):
    """Define Gaussian distribution function.
    
    Parameters
    ----------
    p : 1D array or list
        Amplitude, mean, sigma, y-shift of the Gaussian curve.
    x : 1D array
        Domain over which the function is calculated.

    Returns
    -------
    1D array of Gaussian distribution function for the specified x domain.
    """
    return amp*np.exp(-(1/2)*((x-mean)/sigma)**2)+c

def double_gaussian(x, amp1, mean1, sigma1, amp2, mean2, sigma2, c):
    """Define Gaussian distribution function.
    
    Parameters
    ----------
    p : 1D array or list
        Amplitude, mean, sigma, y-shift of the Gaussian curve.
    x : 1D array
        Domain over which the function is calculated.

    Returns
    -------
    1D array of Gaussian distribution function for the specified x domain.
    """
    return amp1*np.exp(-(1/2)*((x-mean1)/sigma1)**2) + amp2*np.exp(-(1/2)*((x-mean2)/sigma2)**2) + c

def linear(x, p):
    """Define a linear function.
    
    Parameters
    ----------
    p : 1D array or list
        Amplitude, mean, sigma, y-shift of the Gaussian curve.
    x : 1D array
        Domain over which the function is calculated.

    Returns
    -------
    1D array of a linear function for the specified x domain.
    """
    a, b = p
    return a*x + b

def power_law(x, a, b):
    """
    Parameters
    ----------
    a : float
        Amplitude of the power curve.
    b : float
        Power of the power curve.
    x : 1D array
        Domain over which the function is calculated.

    Returns
    -------
    1D array of a linear function for the specified x domain.
    """
    return a*x**b

def residuals(f, x, y, p):
    """Define residuals for a model fit.

    Parameters
    ----------
    p : 1D array or list
        Fit parameters of the curve.
    f : func
        Curve to fit.
    x : 1D array
        Range of x-values to calculate chi^2.
    y : 1D array
        Range of y-values to calculate chi^2.
    
    Returns
    -------
    1D array of residuals function.
    """
    return (y - f(x, *p))

def fit_model(fit_func, x, y, s=None, p0=None, prints=False):
    """Find model fit for any given function and initial parameters.
    
    Parameters
    ----------
    fit_func : func
        Model of the function to fit.
    x : 1D array or list
        X-values of data to fit.
    y : 1D array or list
        Y_values of data to fit.
    s : float, optional
        Error in y-values.

    Returns
    -------
    p_fit : list
        Calculated fit parameters in the same given order of p0.
    e_fit : list
        1-Standard deviation error for each fit parameter.
    r2_val : float
        R squared value of the fit.
    r : 1-D array
        Residuals of the calculated model.
    """
    # Find parameters and their errors
    p_fit, pcov = curve_fit(fit_func, x, y, sigma=s)
    e_fit = np.sqrt(np.diag(pcov))

    # Compute Residuals
    res = residuals(fit_func, x, y, p_fit)

    # R squared
    ss_res = np.sum(res**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2_val = 1 - (ss_res / ss_tot)

    # Chi Squared
    chi2_val = ss_res / (x.size - len(p_fit))

    if prints:
        print('Fit Parameters:', p_fit)
        print('Error in Fit Parameters:', e_fit)
        print('R-squared value of the fit:', r2_val)
        print('Chi-squared value of the fit:', chi2_val)

    return p_fit, e_fit, r2_val, chi2_val, res