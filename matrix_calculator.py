class Matrix:
    def __init__(self, num_rows=0, num_columns=0, mat=[]):
        self.rows = num_rows
        self.columns = num_columns

        self.mat = mat

    def rows_eq_cols(self, mat_inst):
        if self.columns == mat_inst.rows:
            return True
        else:
            return False

    def square_matrix(self):
        return self.rows == self.columns

    def upper_triangular_matrix(self):
        if self.square_matrix():
            truth_lst = [sum(map(lambda x: x == 0, self.mat[i][:i])) for i in range(1, self.rows)]
            for elem in truth_lst:
                if elem == 0:
                    return False
        return True

    def lower_triangular_matrix(self):
        if self.square_matrix():
            truth_lst = [sum(map(lambda x: x == 0, self.mat[i][i + 1:])) for i in range(self.rows - 1)]
            for elem in truth_lst:
                if elem == 0:
                    return False
        return True

    def add_matrices(self, mat_inst):
        # return [(self.mat[n][m] + mat_inst.mat[n][m]) for n in range(self.rows) for m in range(self.columns)]
        return [list(map(sum, zip(self.mat[i], mat_inst.mat[i]))) for i in range(self.rows)]

    @staticmethod
    def product(lst):
        x, y = lst
        res = x * y
        return res

    def mul_matrices(self, mat_inst):
        # Multiplies matrices together using a variation of the "Waterfall Method"
        # Reversing the indices "i" and "j" will calculate the column instead of the row
        # This confusion cost a lot of time :/
        mat_trans = mat_inst.transpose_main()
        return [[sum(map(self.product, zip(mat_trans[j], self.mat[i])))
                 for j in range(len(mat_trans))] for i in range(self.rows)]

    @staticmethod
    def multiply_matrix_by_scalar(mat, scalar):
        return [list(map(lambda x: x * scalar, mat[i])) for i in range(len(mat))]

    def mul_by_const(self, const):
        # return [(const * self.mat[n][m]) for n in range(self.rows) for m in range(self.columns)]
        return self.multiply_matrix_by_scalar(self.mat, const)

    def transpose_main(self):
        new_mat = list(map(list, zip(*self.mat)))
        self.columns = self.rows
        self.rows = len(new_mat)
        return new_mat

    def transpose_side(self):
        self.mat = self.transpose_h()
        self.mat = self.transpose_main()
        return self.transpose_h()

    def transpose_v(self):
        new_mat = []
        for row in self.mat:
            new_mat.append(row[::-1])
        return new_mat

    def transpose_h(self):
        return self.mat[::-1]

    def determinant_helper(self, mat):
        # calculate the minor
        if len(mat) == 2:
            return mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
        # calculate the cofactor
        else:
            det = 0
            for i in range(len(mat)):
                new_mat = mat.copy()
                del new_mat[i]
                new_mat = [lst[1:] for lst in new_mat]
                cofactor = mat[i][0] * pow(-1, i) * self.determinant_helper(new_mat)
                det += cofactor
            return det

    def determinant(self):
        det = 0
        if len(self.mat) == 1:
            return self.mat[0][0]
        elif self.upper_triangular_matrix() or self.lower_triangular_matrix():
            for i in range(len(self.mat)):
                det *= self.mat[i][i]
            return det
        else:
            return self.determinant_helper(self.mat)

    def adjoint_matrix(self, mat):
        adj_mat = [lst[:] for lst in mat]
        num_cols = len(mat)
        for j in range(num_cols):
            for i in range(num_cols):
                new_mat = [lst[:] for lst in mat]
                del new_mat[i]
                for lst in new_mat:
                    lst.remove(lst[j])

                cofactor = pow(-1, i + j) * self.determinant_helper(new_mat)
                adj_mat[i][j] = cofactor

        return list(map(list, zip(*adj_mat)))

    def inverse_matrix(self):
        det = self.determinant()
        if det != 0:
            if self.rows == 2:
                inv_mat = [lst[:] for lst in self.mat]
                a00 = inv_mat[0][0]
                a11 = inv_mat[1][1]
                inv_mat[0][0] = a11
                inv_mat[1][1] = a00
                inv_mat[0][1] = -1 * inv_mat[0][1]
                inv_mat[1][0] = -1 * inv_mat[1][0]
                return inv_mat
            else:
                adj_mat = self.adjoint_matrix(self.mat)
                return [list(map(lambda x: int((x / det) * 100) / 100, adj_mat[i])) for i in range(len(adj_mat))]
        else:
            return [[0]]


def to_int_or_float(num):
    val = 0
    try:
        val = int(num)
    except ValueError:
        try:
            val = float(num)
        except ValueError:
            Exception(f"The operation cannot be performed. Invalid input: {num}.")
    return val


def input_dim():
    return map(int, input().split())


def matrix_generator(prompt=[]):
    prompt_len = len(prompt)
    first_prompt = "Enter size of matrix: "
    second_prompt = "Enter matrix:"
    if prompt_len != 0:
        first_prompt = prompt[0]
        second_prompt = prompt[1]

    print(first_prompt, end="")
    rows, cols = input_dim()
    print(second_prompt)
    mat = input_matrix(rows)
    return Matrix(rows, cols, mat)


def input_matrix(num_rows):
    return [list(map(to_int_or_float, input().split())) for _ in range(num_rows)]


def input_const():
    return to_int_or_float(input().strip())


def print_matrix(matrix):
    for row in matrix:
        print(*row)


def run():
    print("""
1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit""")

    choice = int(input("Your choice: ").strip())

    if choice == 1:
        matrix_a = matrix_generator(["Enter size of first matrix: ", "Enter first matrix:"])

        matrix_b = matrix_generator(["Enter size of second matrix: ", "Enter second matrix:"])

        if matrix_a.square_matrix() and matrix_b.square_matrix():
            print("The result is:")
            new_mat = matrix_a.add_matrices(matrix_b)
            print_matrix(new_mat)
        else:
            print("The operation cannot be performed.")

    elif choice == 2:
        matrix_a = matrix_generator()

        print("Enter constant: ", end="")

        new_mat = matrix_a.mul_by_const(input_const())

        print("The result is:")

        print_matrix(new_mat)
    elif choice == 3:
        matrix_a = matrix_generator(["Enter size of first matrix: ", "Enter first matrix:"])

        matrix_b = matrix_generator(["Enter size of second matrix: ", "Enter second matrix:"])

        if matrix_a.rows_eq_cols(matrix_b):
            print("The result is:")
            new_mat = matrix_a.mul_matrices(matrix_b)
            print_matrix(new_mat)
        else:
            print("The operation cannot be performed.")

    elif choice == 4:
        print("""
1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line""")
        choice = int(input("Your choice: ").strip())
        matrix_a = matrix_generator()

        if choice == 1:
            new_mat = matrix_a.transpose_main()
            print_matrix(new_mat)
        if choice == 2:
            new_mat = matrix_a.transpose_side()
            print_matrix(new_mat)
        if choice == 3:
            new_mat = matrix_a.transpose_v()
            print_matrix(new_mat)
        if choice == 4:
            new_mat = matrix_a.transpose_h()
            print_matrix(new_mat)
    elif choice == 5:
        matrix_a = matrix_generator()

        if matrix_a.square_matrix():
            det = matrix_a.determinant()
            print("The result is:", '\n', det)
        else:
            print("The operation cannot be performed.")

    elif choice == 6:
        matrix_a = matrix_generator()

        if matrix_a.square_matrix():
            inverse_mat = matrix_a.inverse_matrix()
            if inverse_mat[0][0] != 0:
                print_matrix(inverse_mat)
            else:
                print("This matrix doesn't have an inverse.")
        else:
            print("The operation cannot be performed.")

    elif choice == 0:
        exit(0)


def main():
    while True:
        run()


if __name__ == "__main__":
    main()
