from Matrix_multiplication import matrix_multiply
import pytest


# Test that two compatible matrices are multiplied correctly.
def test_matrix_multiply():
    A = [[1, 2], [3, 4]]
    B = [[2, 0], [1, 2]]
    expected = [[4, 4], [10, 8]]
    assert matrix_multiply(A, B) == expected


# Test that attempting to multiply incompatible matrices raises a ValueError.
def test_incompatible_matrices():
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[1, 2], [3, 4]]
    with pytest.raises(ValueError):
        matrix_multiply(A, B)


# Test that multiplying a matrix by the identity matrix returns the original matrix.
def test_multiply_by_identity_matrix():
    A = [[1, 2], [3, 4]]
    identity_matrix = [[1, 0], [0, 1]]
    assert matrix_multiply(A, identity_matrix) == A


# Test that multiplying any matrix by a zero matrix results in a zero matrix.
def test_multiply_by_zero_matrix():
    A = [[2, 3], [4, 5]]
    zero_matrix = [[0, 0], [0, 0]]
    expected_result = [[0, 0], [0, 0]]
    assert matrix_multiply(A, zero_matrix) == expected_result


# Test that larger matrices are multiplied correctly.
def test_with_larger_matrices():
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8], [9, 10], [11, 12]]
    expected = [[58, 64], [139, 154]]
    assert matrix_multiply(A, B) == expected


# Test that matrices containing negative numbers are multiplied correctly.
def test_with_negative_numbers():
    A = [[-1, -2], [3, 4]]
    B = [[2, 0], [-1, -2]]
    expected = [[0, 4], [2, -8]]
    assert matrix_multiply(A, B) == expected


# Test that attempting to multiply a matrix by an empty matrix raises a ValueError.
def test_multiply_with_empty_matrix():
    A = [[1, 2], [3, 4]]
    empty_matrix = []
    with pytest.raises(ValueError):
        matrix_multiply(A, empty_matrix)
