import numpy as np 


def matrix_multiplication(ar1, ar2):
    
    return np.matmul(ar1, ar2)


def multiplication_check(mat_list):
    
    for i in range(1, len(mat_list)):
        
        #check the number of columns in matrix1
        #is equal to the number of rows in matrix2.
        if mat_list[i-1].shape[1] != mat_list[i].shape[0]:
            return False
    
    return True


def multiply_matrices(mat_list):

    #check possibility of multiplication
    if mat_list[0].shape[1] != mat_list[1].shape[0]:
        return None
    
    #multiplying
    else:
        res = np.matmul(mat_list[0], mat_list[1])
    
    if len(mat_list) > 2:
        for i in range(2, len(mat_list)):
            if res.shape[1] != mat_list[i].shape[0]:
                return None
            else:
                res = np.matmul(res, mat_list[i])
    return res

def compute_2d_distance(ar1, ar2):
    
    return np.linalg.norm(ar1 - ar2)


def compute_multidimensional_distance(ar1, ar2):
    
    return np.linalg.norm(ar1 - ar2)


def compute_pair_distances(ar):
    
    return np.linalg.norm(ar[:, None, :] - ar[None, :, :], axis=-1)


if __name__ == '__main__':
    
    #create 3 arrays
    ar1 = np.arange(15)
    ar2 = np.eye(5)
    ar3 = np.diag([1, 2, 3])
    
    main()
