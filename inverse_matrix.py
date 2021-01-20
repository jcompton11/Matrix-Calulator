matA = [[2, 4, 1], [-1, 1, -1], [1, 4, 0]]

# A Inverse = 1/det(A) * Adj(A), when det(A) != 0
# In a 2x2 matrix, the Adj(A) the reverse of the 1st elem in the 1st row
# with the 2nd elem in the 2nd row and a reverse sign on the 2nd diagonal.

rows = len(matA)
cols = len(matA[0])

def identity_mat(mat):
    return [[1 if i == j else 0 for j in range(cols)] for i in range(rows)]

def augmented_mat(mat):
    mat_a = [lst[:] for lst in mat]
    mat_i = identity_mat(mat)
    
    for i in range(len(mat)):
        mat_a[i].extend(mat_i[i])
    return mat_a

def row_operation(elem, lst):
    x, y = lst
    return x + -1 * x * y

def inverse_matrix(mat):
    aug_mat = augmented_mat(mat)
    
    for fd in range(cols):
        elem = aug_mat[fd][fd]
        aug_mat[fd] = list(map(lambda x: x / elem if x > 0 else -1 * (x / elem), aug_mat[fd]))
        sub_mat = aug_mat[:fd] + aug_mat[fd + 1:]
        aug_mat = [list(map(lambda l: l[0] + -1 * sub_mat[i][fd] * l[1], zip(sub_mat[i], aug_mat[fd]))) for i in range(len(sub_mat))]
    
    return None

# print(f"The Determinant of A: {determinant_helper(matA)}")
# print("The cofactor matrix:")
# print("Identity matrix of A: ")
# for row in identity_mat(matA):
#    print(*row)
print("The inverse matrix of A: ")
for row in inverse_matrix(matA):
    print(*row)