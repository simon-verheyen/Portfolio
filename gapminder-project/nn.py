import nn_tools
import numpy as np


# This script combines all the tools from nn_tools.py to train a neural network and get predictions
def train_network(layer_dims, data, Y, iterations, learning_rate=0.1, lambd=0.001, problem_type='regression',
                  beta1=0.9, beta2=0.999, epsilon=0.00000001, weight_decay=False, adam=True):

    param = nn_tools.init_param_he(layer_dims)
    Y = np.array(Y).reshape(-1, 1)
    adam_param = {}
    cost = []

    for i in range(iterations):
        if i % 10 == 1:
            print(f"iteration: {i}")

        Ypr_iter = []
        for j in range(data.shape[0]):
            X = np.array([data.values[j]]).T
            Ypr, mem = nn_tools.model_forw(X, param, problem_type)
            Ypr_iter.append(Ypr)

            grads = nn_tools.model_back(Y[j], Ypr, mem, problem_type)

            param, adam_param = nn_tools.update_param(param, grads, learning_rate, lambd, i, adam_param, weight_decay,
                                                      adam, beta1, beta2, epsilon)

            print(grads)
            pred = np.array([Ypr_iter]).reshape(-1, 1)

        if problem_type == 'regression':
            cost_itr = nn_tools.mse(Y, pred)

        else:
            cost_itr = nn_tools.cross_entropy(Y, pred)

        cost.append(cost_itr)

    return param, cost


def predict(param, data, output_type='regression'):
    pred = []

    for ind, row in data.iterrows():
        X = np.array([row]).T
        Af, mem = nn_tools.model_forw(X, param, output_type)

        pred.append(Af)

    pred.reshape(1, 1)

    return pred
