
class MatrixMixin():
    def get_2d_matrix(self):
        """ Returns two-dimensional matrix"""
        two_d_matrix = []
        for i in range(3):
            next = []
            for j in range(3):
                next.append(getattr(self, "matrix_%s_%s" % (i, j)))
            two_d_matrix.append(next)

        translation_vector = []
        for i in range(3):
            translation_vector.append(getattr(self, "vector_%s" % i))

        two_d_matrix.append(translation_vector)
        return two_d_matrix