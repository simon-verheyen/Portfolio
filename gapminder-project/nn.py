import nn_tools
import numpy as np


# This script combines all the tools from nn_tools.py to train a neural network and get predictions
def train_network(layer_dims, data, Y, iterations, optimizer, learning_rate=0.01, lambd=0.001, problem_type='regression',
                  beta1=0.9, beta2=0.999, epsilon=1e-8, L2=True):

    param = nn_tools.init_param_he(layer_dims)

    if optimizer == 'adam':
        V, S = nn_tools.initialize_adam(param)

    Y = np.array(Y).reshape(-1, 1)
    cost = []

    for i in range(1, iterations + 1):
        if i % 10 == 0:
            print(f"iteration: {i}")

        Ypr_iter = []
        for j in range(data.shape[0]):
            X = np.array([data.values[j]]).T
            Ypr, mem = nn_tools.model_forw(X, param, problem_type)
            Ypr_iter.append(Ypr)

            grads = nn_tools.model_back(Y[j], Ypr, mem, problem_type)

            if optimizer == 'adam':
                param, V, S = nn_tools.update_adam(param, grads, V, S, i, learning_rate, L2, lambd, beta1, beta2, epsilon)
            elif optimizer == 'gd':
                param = nn_tools.update_gd(param, grads, learning_rate, lambd, L2)

        pred = np.array([Ypr_iter]).reshape(-1, 1)

        if problem_type == 'regression':
            cost_itr = nn_tools.mse(Y, pred)

        else:
            cost_itr = nn_tools.cross_entropy(Y, pred)

        cost_itr = np.squeeze(cost_itr)
        cost.append(cost_itr)

    return param, cost


def predict(param, data, output_type='regression'):
    pred = np.array([])

    for ind, row in data.iterrows():
        X = np.array([row]).T
        Af, mem = nn_tools.model_forw(X, param, output_type)

        pred = np.append(pred, np.squeeze(Af))

    return pred.reshape(-1, 1)


def check_grads(layers_dim, data, Y, problem_type='regression'):
    param = nn_tools.init_param_he(layers_dim)
    Y = np.array(Y).reshape(-1, 1)

    for i in range(len(Y)):
        X = np.array([data.values[i]]).T
        Ypr, mem = nn_tools.model_forw(X, param, problem_type)

        grads = nn_tools.model_back(Y[i], Ypr, mem, problem_type)
        nn_tools.grad_checking(layers_dim, param, grads, X, Y[i])

