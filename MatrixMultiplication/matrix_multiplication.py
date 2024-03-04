import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def matrix_multiply(A, B):
    """Multiply matrix A by matrix B."""
    if len(A[0]) != len(B):
        raise ValueError(
            "The number of columns in A must equal the number of rows in B"
        )

    result = [
        [0 for _ in range(len(B[0]))] for _ in range(len(A))
    ]

    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result
