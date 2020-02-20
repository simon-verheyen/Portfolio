import tools_nn
import numpy as np


def train_network(layer_dims, entries, output, iterations, learning_rate, output_type):
    param = tools_nn.init_param_he(layer_dims)
    Y = np.array(output)

    for i in range(iterations):
        for j in range(entries.shape[1]):
            entry = np.array([entries.values[j]]).T
            Af, mem = tools_nn.model_forw(entry, param, output_type)
            grads = tools_nn.model_back(Af, Y[j], mem, output_type)

            param = tools_nn.update_param(param, grads, learning_rate)

    return param


def predict(param, A, output_type):
    Af, mem = tools_nn.model_forw(A, param, output_type)

    return Af
