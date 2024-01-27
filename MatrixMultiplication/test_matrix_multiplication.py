from matrix_multiplication import multiply_matrices

def run_test_cases():
    test_cases = [
        # Valid test cases
        ([[1, 2], [3, 4]], [[5, 6], [7, 8]], [[19, 22], [43, 50]]),
        ([[2, 4], [6, 8]], [[1, 3], [5, 7]], [[22, 34], [46, 74]]),
        # Invalid test cases (Dimension mismatch)
        ([[1, 2, 3]], [[4], [5]], "ValueError"),
        # Test with zero matrices
        ([[0, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0], [0, 0]]),
        # Test with identity matrices
        ([[1, 0], [0, 1]], [[1, 2], [3, 4]], [[1, 2], [3, 4]]),
        # Test with single row and single column
        ([[1, 2, 3]], [[4], [5], [6]], [[32]]),
        # Test with incompatible matrices (should raise ValueError)
        ([[1, 2]], [[3, 4], [5, 6], [7, 8]], "ValueError")
    ]

    passed_tests = 0
    failed_tests = 0

    for i, (A, B, expected) in enumerate(test_cases, 1):
        try:
            result, _ = multiply_matrices(A, B)
            assert result == expected, f"Test case {i} failed: {result} != {expected}"
            print(f"Test case {i} passed.")
            passed_tests += 1
        except ValueError:
            if expected == "ValueError":
                print(f"Test case {i} correctly raised ValueError.")
                passed_tests += 1
            else:
                print(f"Test case {i} failed: ValueError was not expected.")
                failed_tests += 1
        except AssertionError as e:
            print(e)
            failed_tests += 1

    print(f"Passed tests: {passed_tests}")
    print(f"Failed tests: {failed_tests}")

if __name__ == "__main__":
    run_test_cases()