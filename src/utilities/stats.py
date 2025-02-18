import numpy as np
from scipy import stats
from sklearn import metrics
import torch

def d_prime(auc):
    standard_normal = stats.norm()
    d_prime = standard_normal.ppf(auc) * np.sqrt(2.0)
    return d_prime

def calculate_stats(output, target):
    """Calculate regression statistics including MSE, MAE, and R².
    
    Args:
        output: array of predicted values
        target: array of true values
        
    Returns:
        stats: dictionary containing MSE, MAE, and R²
    """
    
    # Calculate MSE, MAE, and R² for regression
    mse = metrics.mean_squared_error(target, output)
    mae = metrics.mean_absolute_error(target, output)
    r2 = metrics.r2_score(target, output)
    
    stats = {
        'mse': mse,
        'mae': mae,
        'r2': r2
    }
    
    return stats