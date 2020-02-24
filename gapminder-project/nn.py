import tools_nn
import numpy as np


# This script combines all the tools from tools_nn.py to train a neural network and get predictions
def train_network(layer_dims, data, Y, iterations, learning_rate, lambd, problem_type='regression',
                  beta1=0.9, beta2=0.999, epsilon=0.00000001, weight_decay=False, adam=True):
    param = tools_nn.init_param_he(layer_dims)
    Y = np.array(Y).reshape(-1, 1)

    adam_param = {}

    for i in range(iterations):
        for j in range(data.shape[0]):
            entry = np.array([data.values[j]]).T
            Ypr, mem = tools_nn.model_forw(entry, param, problem_type)
            grads = tools_nn.model_back(Y[j], Ypr, mem, problem_type)

            param, adam_param = tools_nn.update_param(param, grads, learning_rate, lambd, i, adam_param, weight_decay,
                                                      adam, beta1, beta2, epsilon)

    return param


def predict(param, A, output_type):
    Af, mem = tools_nn.model_forw(A, param, output_type)

    return Af
