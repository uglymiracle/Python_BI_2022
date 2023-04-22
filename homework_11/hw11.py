from sklearn.base import BaseEstimator
from sklearn.datasets import make_classification
import numpy as np #использовала в дз по мл, воть и оставила
from sklearn.tree import DecisionTreeClassifier
from concurrent.futures import ThreadPoolExecutor


class RandomForestClassifierCustom(BaseEstimator):
    
    def __init__(
        self, n_estimators=10, max_depth=None, max_features=None, random_state=100
    ):
        
    """
    Random Forest Classifier implementation.
    
    Parameters:
    -----------
    n_estimators : int, default=10
        The number of trees in the forest.
    max_depth : int or None, default=None
        The maximum depth of the tree. 
    max_features : int or None, default=None
        The number of features to consider when looking for the best split.
        None indicates that all features will be used.
    random_state : int, default=100
        Seed of the random number generator.
    """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = max_features
        self.random_state = random_state

        self.trees = []
        self.feat_ids_by_tree = []

    def fit(self, X, y, n_jobs):
        
        """
        Build a forest of decision trees from the training set.

        Parameters:
        -----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The training input samples.
        y : array-like of shape (n_samples,)
            The target values.
        n_jobs : int or None, default=None
            The number of threads to use for parallel processing.
            None indicates that all available CPUs will be used.
            
        Returns:
        --------
        self : The fitted estimator.
        """
            
        with ThreadPoolExecutor(n_jobs) as pool:
            
            self.classes_ = sorted(np.unique(y)) 
            works = []
            
            for i in range(self.n_estimators):

                np.random.seed(self.random_state + i)

                features_ids = np.random.choice(X.shape[1], self.max_features, replace=False)
                self.feat_ids_by_tree.append(features_ids)

                bootstrap_ids = np.random.choice(X.shape[0], X.shape[0], replace=True)
                X_bootstrap = X[bootstrap_ids, :][:, features_ids]
                y_bootstrap = y[bootstrap_ids]

                tree = DecisionTreeClassifier(
                    max_depth=self.max_depth,
                    max_features=self.max_features,
                    random_state=self.random_state,
                )
                works.append(pool.submit(tree.fit, X_bootstrap, y_bootstrap))
                self.trees.append(tree)

        return self  
    
    def predict_proba(self, X, n_jobs):
        
        """
        Predict class probabilities for X.

        Parameters:
        -----------
        X : {array-like, sparse matrix} of shape (n_samples, n_features)
            The training input samples.
        n_jobs : int or None, default=None
            The number of threads to use for parallel processing.
            None indicates that all available CPUs will be used.
            
        Returns:
        --------
        probas : array-like of shape (n_samples, n_classes)
            The class probabilities of the input samples.
        """
        
        probas = np.zeros((X.shape[0], len(self.classes_)))
        
        with ThreadPoolExecutor(n_jobs) as pool:
            
            works = [pool.submit(tree.predict_proba, X[:, self.feat_ids_by_tree[i]])
                        for i, tree in enumerate(self.trees)]
            for w in works:
                probas += w.result()
                 
        return probas / len(self.trees)
    
    def predict(self, X, n_jobs):
        
        """
        Predict class labels for samples in X.
        
        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.
            
        n_jobs : int, default=None
            The number of jobs to run in parallel for predicting probabilities. 
            If None, then the number of jobs is set to the number of CPU cores.
        
        Returns
        -------
        y_pred : ndarray of shape (n_samples,)
            The predicted class labels for X.
        """
        
        probas = self.predict_proba(X, n_jobs)
        predictions = np.argmax(probas, axis=1)
        
        return predictions


import multiprocessing
multiprocessing.set_start_method('fork')
import os
import psutil
import time
import warnings


def get_memory_usage(pid):    
    
    """
    Returns the current memory usage (in bytes) of a given process.

    Args:
    pid (int): The process ID for which to retrieve memory usage.

    Returns:
    int: The current memory usage (in bytes) of the process.
    """
    
    process = psutil.Process(pid)
    mem_info = process.memory_info()
    return mem_info.rss


def bytes_to_human_readable(n_bytes):
    
    """
    Converts a number of bytes into a human-readable format (e.g. 1.25GB).

    Args:
    n_bytes (int): The number of bytes to convert.

    Returns:
    str: The human-readable representation of the number of bytes.
    """
    
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for idx, s in enumerate(symbols):
        prefix[s] = 1 << (idx + 1) * 10
    for s in reversed(symbols):
        if n_bytes >= prefix[s]:
            value = float(n_bytes) / prefix[s]
            return f"{value:.2f}{s}"
    return f"{n_bytes}B"

def human_readable_to_bytes(size):
    
    """
    Converts a human-readable representation of a file size (e.g. '1.25GB') to its
    equivalent number of bytes.

    Args:
    size (str): The human-readable size string to convert.

    Returns:
    int: The number of bytes equivalent to the given size string.
    """

    num = float(size[:-1])
    factor = {'B': 1, 'K': 1024, 'M': 1024**2, 'G': 1024**3, 'T': 1024**4,
             'P': 1024**5, 'E': 1024**6, 'Z': 1024**7, 'Y': 1024**8}[size[-1]]
    
    return num * factor

def memory_limit(soft_limit=None, hard_limit=None, poll_interval=1):
    
    """
    A decorator that limits the memory usage of a decorated function.

    Args:
    soft_limit (str, optional): A string indicating the soft memory limit (e.g. '1.25GB').
        When the memory usage exceeds this limit, a warning will be raised.
    hard_limit (str, optional): A string indicating the hard memory limit (e.g. '2GB').
        When the memory usage exceeds this limit, a MemoryError will be raised.
    poll_interval (int, optional): The interval (in seconds) at which to poll the memory usage.

    Returns:
    function: A wrapper function that limits the memory usage of the decorated function.
    """
        
    def decorator(func):
        def wrapper(*args, **kwargs):
            
            if soft_limit is not None:
                soft_limit_bytes = human_readable_to_bytes(soft_limit)
            if hard_limit is not None:
                hard_limit_bytes = human_readable_to_bytes(hard_limit)
                
            memory_info_soft_limit = 0
            
            
            proc = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
            proc.start()
            pid = proc.pid
                
            while proc.is_alive():
                
                memory_usage = get_memory_usage(pid)
                
                if hard_limit is not None:
                    if memory_usage > hard_limit_bytes:
                        message = f"Memory usage exceeds hard limit of {hard_limit}. \
                        \n Current usage: {bytes_to_human_readable(memory_usage)}. \
                        \n Limit exceeded by {bytes_to_human_readable(memory_usage-hard_limit_bytes)}"
                        
                        raise MemoryError(message)
                    
                if soft_limit is not None:
                    if memory_usage > soft_limit_bytes:
                        if memory_usage > memory_info_soft_limit:
                            memory_info_soft_limit = memory_usage
                    
                time.sleep(poll_interval)
                
            proc.join()
            
            if soft_limit is not None:
                if memory_info_soft_limit != 0:
                    message = f"Memory usage exceeds soft limit of {soft_limit}. \
                            \n Peak usage: {bytes_to_human_readable(memory_info_soft_limit)}. \
                            \n Limit exceeded by {bytes_to_human_readable(memory_info_soft_limit-soft_limit_bytes)}"
                    warnings.warn(message, UserWarning)
            
            #return все не могу разобраться как сделать, чтобы возвращать с функции ее ретерн(( хелп 
            #я нашла, что можно с помощью queue, но тогда надо менять фукцию саму, ну ретерн, как я поняла
            #а вот без этого как
            
        return wrapper
    return decorator

from concurrent.futures import ThreadPoolExecutor

def parallel_map(target_func,
                 args_container=None,
                 kwargs_container=None,
                 n_jobs=None):
    
    """
    Apply a function to multiple arguments in parallel.

    Args:
        target_func: A function to apply to the arguments.
        args_container: A container of arguments for the function. Default is None.
        kwargs_container: A container of keyword arguments for the function. Default is None.
        n_jobs: The number of threads to use. If None, the number of threads is set to the number of CPUs
            on the machine. Default is None.

    Raises:
        ValueError: If `args_container` and `kwargs_container` have different lengths.

    Returns:
        A list of the results of applying the function to the arguments.
    """
    
    if args_container is None:
        args_len = 0
    else:
        args_len = len(args_container)
    
    if kwargs_container is None:
        kwargs_len = 0
    else:
        kwargs_len = len(kwargs_container)
        
    if args_len != 0 and kwargs_len != 0:
        
        if args_len != kwargs_len:
            raise ValueError("args_container and kwargs_container should have same lengths")    
        
    if n_jobs is None:
        n_jobs = multiprocessing.cpu_count()

    if n_jobs > max(args_len, kwargs_len) and max(args_len, kwargs_len) != 0:
        n_jobs = max(args_len, kwargs_len)

    with ThreadPoolExecutor(n_jobs) as pool:
        
        results = []
        
        for i in range(max(args_len, kwargs_len)):
            if args_len == 0:
                args = []
            else:
                args = args_container[i]
                
            if kwargs_len == 0:
                kwargs = {}
            else:
                kwargs = kwargs_container[i]
                
            if isinstance(args, tuple) or args == []:
                result = pool.submit(target_func, *args, **kwargs)
                results.append(result)
                
            else:
                result = pool.submit(target_func, args, **kwargs)
                results.append(result)
            
        if args_len == 0 and kwargs_len == 0:
            for i in range(n_jobs):
                result = pool.submit(target_func)
                results.append(result)

    results_sum = []
    for result in results:
        results_sum.append(result.result())

    return results_sum
