import time

def multiply_matrices(A, B):
    """
    Multiply two matrices A and B and return the result along with the time taken to compute.
    
    :param A: list of lists, where the inner lists represent rows of matrix A
    :param B: list of lists, where the inner lists represent rows of matrix B
    :return: list of lists representing the result of multiplying A by B, and the computation time
    """
    start_time = time.time()
    
    if not A or not B or len(A[0]) != len(B):
        raise ValueError("Matrices have incompatible dimensions for multiplication.")
    
    result = [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*B)] for A_row in A]
    
    end_time = time.time()
    computation_time = end_time - start_time
    
    return result, computation_time

if __name__ == "__main__":
    # This can be used to quickly test the function with a default case
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    result, computation_time = multiply_matrices(A, B)
    print(f"Result: {result}, Computation Time: {computation_time} seconds")