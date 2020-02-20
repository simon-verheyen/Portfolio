import numpy as np
import random

n_x = 4
n_h = 3
n_y = 1
layers_dims = [n_x, n_h, n_y]
mutation_rate = 0.2


class Brain:
    def __init__(self):

        self.layers_dims = layers_dims
        self.parameters = initialize_parameters(layers_dims)

    def to_jump(self, distX, toTop, toBot, jumpLeft):

        X = np.array([[distX], [toTop], [toBot], [jumpLeft]])
        A1 = linear_activation_forward(X, self.parameters["W1"], "relu")
        A2 = linear_activation_forward(A1, self.parameters["W2"], "sigmoid")

        return A2 >= 0.5

    def make_baby(self, dad):

        kid = Brain()
        conc_mom = np.concatenate((self.parameters['W1'], self.parameters['W2']), axis=None)
        conc_dad = np.concatenate((dad.parameters['W1'], dad.parameters['W2']), axis=None)
        random_stop = random.randint(0, conc_mom.shape[0])
        ind = 0

        for i in range(0, len(conc_mom)):
            if i < random_stop:
                conc_mom[i] = conc_dad[i]

        for l in range(1, len(self.layers_dims)):
            for i in range(0, self.layers_dims[l]):
                for j in range(0, self.layers_dims[l - 1]):
                    kid.parameters['W' + str(l)][i, j] = conc_mom[ind]
                    ind += 1

        return kid.parameters

    def mutate(self):

        conc = np.concatenate((self.parameters['W1'], self.parameters['W2']), axis=None)
        ind = 0

        for i in range(0, len(conc)):
            if random.random() < mutation_rate:
                conc[i] = np.random.randn(1) * 0.01

        for l in range(1, len(self.layers_dims)):
            for i in range(0, self.layers_dims[l]):
                for j in range(0, self.layers_dims[l - 1]):
                    self.parameters['W' + str(l)][i, j] = conc[ind]
                    ind += 1


def initialize_parameters(layer_dims):
    parameters = {}
    L = len(layer_dims)

    for l in range(1, L):
        parameters['W' + str(l)] = np.random.randn(layer_dims[l], layer_dims[l - 1]) * 0.01

        assert (parameters['W' + str(l)].shape == (layer_dims[l], layer_dims[l - 1]))

    return parameters


def linear_activation_forward(A_prev, W, activation):
    if activation == "sigmoid":
        Z = linear_forward(A_prev, W)
        A = sigmoid(Z)

    elif activation == "relu":
        Z = linear_forward(A_prev, W)
        A = relu(Z)

    assert (A.shape == (W.shape[0], A_prev.shape[1]))

    return A


def linear_forward(A, W):
    Z = np.dot(W, A)
    assert (Z.shape == (W.shape[0], A.shape[1]))

    return Z


def sigmoid(Z):
    A = 1 / (1 + np.exp(-Z))

    return A


def relu(Z):
    A = np.maximum(0, Z)

    assert (A.shape == Z.shape)

    return A
