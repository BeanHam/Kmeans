import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from sklearn.metrics import pairwise_distances

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class Kmeans:
    """K-Means Clustering Algorithm"""
    
    def __init__(self, k, centers=None, cost=None,iter=None, labels=None, max_iter = 1000):
        """Initialize Parameters"""
        
        self.max_iter = max_iter
        self.k = k
        self.centers = np.empty(1)
        self.cost = []
        self.iter = 1
        self.labels = np.empty(1)

    def calc_distances(self, data, centers, weights):
        """Distance Matrix"""
        
        distance = pairwise_distances(data, centers)**2
        min_distance = np.min(distance, axis = 1)
        D = min_distance*weights
        return D    
    
    def fit(self, data):
        """Clustering Process"""
        
        ## Initial centers
        if type(data) == pd.DataFrame: data = data.values
        nrow = data.shape[0]
        index = np.random.choice(range(nrow), self.k, False)
        self.centers = data[index]
        
        while (self.iter <= self.max_iter):
            distance = pairwise_distances(data, self.centers)**2
            self.cost.append(sum(np.min(distance, axis=1)))
            self.labels = np.argmin(distance, axis=1)
            centers_new = np.array([np.mean(data[self.labels == i], axis=0) for i in np.unique(self.labels)])
            
            ## sanity check
            if(np.all(self.centers == centers_new)): break 
            self.centers = centers_new
            self.iter += 1
            
        ## convergence check
        if (sum(np.min(pairwise_distances(data, self.centers)**2, axis=1)) != self.cost[-1]):
            warnings.warn("Algorithm Did Not Converge In {} Iterations".format(self.max_iter))
        return self

