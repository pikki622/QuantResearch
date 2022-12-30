import numpy as np
from scipy.stats import norm
import xlwings as xw

# https://en.wikipedia.org/wiki/Greeks_(finance)
@xw.func
def bsm(S, K, T = 1.0, r = 0.0, q = 0.0, sigma = 0.16, CP='call'):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    result = 0.0
    if CP.lower() == 'call':
        result = (S * np.exp(-q * T) * norm.cdf(d1, 0.0, 1.0) - K * np.exp(-r * T) * norm.cdf(d2, 0.0, 1.0))
    if CP.lower() == 'put':
        result = (K * np.exp(-r * T) * norm.cdf(-d2, 0.0, 1.0) - S * np.exp(-q * T) * norm.cdf(-d1, 0.0, 1.0))

    return result

@xw.func
def bsm_delta(S, K, T = 1.0, r = 0.0, q = 0.0, sigma = 0.16, CP='call'):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    result = 0.0
    if CP.lower() == 'call':
        result = np.exp(-q * T) * norm.cdf(d1, 0.0, 1.0)
    if CP.lower() == 'put':
        result = - np.exp(-q * T) * norm.cdf(-d1, 0.0, 1.0)

    return result

@xw.func
def bsm_vega(S, K, T = 1.0, r = 0.0, q = 0.0, sigma = 0.16):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    return S * np.exp(-q * T) * norm.pdf(d1, 0.0, 1.0) * np.sqrt(T)

@xw.func
def bsm_theta(S, K, T = 1.0, r = 0.0, q = 0.0, sigma = 0.16, CP='call'):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    result = 0.0
    if CP.lower() == 'call':
        result = - np.exp(-q * T) * S * norm.pdf(d1, 0.0, 1.0) * sigma / 2 / np.sqrt(T) \
                 - r * K * np.exp(-r * T) * norm.cdf(d2, 0.0, 1.0) \
                 + q * S * np.exp(-q * T) * norm.cdf(d1, 0.0, 1.0)
    if CP.lower() == 'put':
        result = - np.exp(-q * T) * S * norm.pdf(-d1, 0.0, 1.0) * sigma / 2 / np.sqrt(T) \
                 + r * K * np.exp(-r * T) * norm.cdf(-d2, 0.0, 1.0) \
                 - q * S * np.exp(-q * T) * norm.cdf(-d1, 0.0, 1.0)

    return result

@xw.func
def bsm_rho(S, K, T = 1.0, r = 0.0, q = 0.0, sigma = 0.16, CP='call'):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    result = 0.0
    if CP.lower() == 'call':
        result = K * T * np.exp(-r*T) * norm.cdf(d2, 0.0, 1.0)
    if CP.lower() == 'put':
        result = -K * T * np.exp(-r*T) * norm.cdf(-d2, 0.0, 1.0)

    return result


@xw.func
def bsm_gamma(S, K, T = 1.0, r = 0.0, q = 0.0, sigma = 0.16):
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    return np.exp(-q*T) * norm.pdf(d1) / S / sigma / np.sqrt(T)

@xw.func
def bsm_vanna(S, K, T = 1.0, r = 0.0, q = 0.0, sigma = 0.16):
    """d^2V/dS/dsigma"""
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    return -np.exp(-q*T) * norm.pdf(d1) * d2 / sigma

@xw.func
def bsm_volga(S, K, T = 1.0, r = 0.0, q = 0.0, sigma = 0.16):
    """d^2V/dsigma^2"""
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(S / K) + (r - q - 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    return S*np.exp(-q*T) * norm.pdf(d1) * np.sqrt(T) * d1 * d2 / sigma

@xw.func
def black76(F, K, T, r, sigma, CP='call'):
    d1 = (np.log(F / K) + (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(F / K) - (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    result = 0.0
    return (
        np.exp(-r * T) * (F * norm.cdf(d1) - K * norm.cdf(d2))
        if CP.lower() == 'call'
        else np.exp(-r * T) * (K * norm.cdf(-d2) - F * norm.cdf(-d1))
    )

@xw.func
def black76_delta(F, K, T, r, sigma, CP='call'):
    d1 = (np.log(F / K) + (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(F / K) - (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    result = 0.0
    return (
        np.exp(-r * T) * norm.cdf(d1)
        if CP.lower() == 'call'
        else -np.exp(-r * T) * norm.cdf(-d1)
    )

@xw.func
def black76_vega(F, K, T, r, sigma):
    d1 = (np.log(F / K) + (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(F / K) - (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    return F * np.exp(-r * T) * norm.pdf(d1) * np.sqrt(T)

@xw.func
def black76_theta(F, K, T, r, sigma, CP='call'):
    d1 = (np.log(F / K) + (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(F / K) - (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    result = 0.0
    return (
        -F * np.exp(-r * T) * norm.pdf(d1) * sigma / 2 / np.sqrt(T)
        - r * K * np.exp(-r * T) * norm.cdf(d2)
        + r * F * np.exp(-r * T) * norm.cdf(d1)
        if CP.lower() == 'call'
        else -F * np.exp(-r * T) * norm.pdf(-d1) * sigma / 2 / np.sqrt(T)
        + r * K * np.exp(-r * T) * norm.cdf(-d2)
        - r * F * np.exp(-r * T) * norm.cdf(-d1)
    )


@xw.func
def black76_rho(F, K, T, r, sigma, CP='call'):
    d1 = (np.log(F / K) + (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(F / K) - (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    result = 0.0
    return (
        K * T * np.exp(-r * T) * norm.cdf(d2)
        if CP.lower() == 'call'
        else -K * T * np.exp(-r * T) * norm.cdf(-d2)
    )


@xw.func
def black76_gamma(F, K, T, r, sigma):
    d1 = (np.log(F / K) + (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(F / K) - (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    return np.exp(-r*T)*norm.pdf(d1)/F/sigma/np.sqrt(T)

@xw.func
def black76_vanna(F, K, T, r, sigma):
    d1 = (np.log(F / K) + (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(F / K) - (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    return -np.exp(-r*T)*norm.pdf(d1)*d2/sigma

@xw.func
def black76_volga(F, K, T, r, sigma):
    d1 = (np.log(F / K) + (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = (np.log(F / K) - (0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    return F*np.exp(-r*T)*norm.pdf(d1)*np.sqrt(T)*d1*d2/sigma