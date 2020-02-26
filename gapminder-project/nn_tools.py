import numpy as np

""" Verify if adam is ok!!! """


# Initialize parameters with regularization to combat high weights in deep network for faster gradient descent
def init_param_he(layer_dims):
    np.random.seed()
    param = {}

    depth = len(layer_dims)
    for i in range(1, depth):
        param['W' + str(i)] = np.random.randn(layer_dims[i], layer_dims[i - 1]) * np.sqrt(2 / layer_dims[i - 1])
        param['b' + str(i)] = np.zeros((layer_dims[i], 1))

        assert (param['W' + str(i)].shape == (layer_dims[i], layer_dims[i - 1]))
        assert (param['b' + str(i)].shape == (layer_dims[i], 1))

    return param


# Sigmoid is used as the activation function for classification problems
def sigmoid(Z):
    A = 1 / (1 + np.exp(-Z))
    mem = Z

    assert (A.shape == Z.shape)

    return A, mem


# Derivative of the sigmoid function used during backpropagation to get the nn parameter gradients
def sigmoid_backprop(dA, mem):
    Z = mem

    a = 1 / (1 + np.exp(-Z))
    dZ = dA * a * (1 - a)

    assert (dZ.shape == Z.shape)

    return dZ


# Relu is used as the activation function for hidden layers, as well as for regression problems
def relu(Z):
    A = np.maximum(0, Z)
    mem = Z

    assert (A.shape == Z.shape)

    return A, mem


# Derivative of the sigmoid function used during backpropagation to get the nn parameter gradients
def relu_backprop(dA, mem):
    Z = mem

    dZ = np.array(dA, copy=True)
    dZ[Z <= 0] = 0

    assert (dZ.shape == dA.shape)

    return dZ


# Linear forward step to aply the weights of a layer
def lin_forw(A, W, b):
    Z = np.dot(W, A) + b
    mem = A, W, b

    assert (Z.shape == (W.shape[0], A.shape[1]))

    return Z, mem


# Dirivitve to get the gradients fr the nn parameters
def lin_back(dZ, mem):
    A_prev, W, b = mem

    m = A_prev.shape[0]

    dW = 1. / m * np.dot(dZ, A_prev.T)
    db = 1. / m * np.sum(dZ, axis=1, keepdims=True)
    dA_prev = np.dot(W.T, dZ)

    assert (dW.shape == W.shape)
    assert (db.shape == b.shape)
    assert (dA_prev.shape == A_prev.shape)

    return dA_prev, dW, db


# Full step forward, combining the linear forward step with the activation function to create an output per layer
def lin_act_forw(A_prev, W, b, act):
    Z, lin_mem = lin_forw(A_prev, W, b)

    if act == 'sigmoid':
        A, act_mem = sigmoid(Z)
    elif act == 'relu':
        A, act_mem = relu(Z)

    mem = (lin_mem, act_mem)

    assert (A.shape == (W.shape[0], A_prev.shape[1]))

    return A, mem


# Full step backwards, combining the dirivative of lin forward step and activation function
# to get the gradients of per layer
def lin_act_back(dA, mem, act):
    lin_mem, act_mem = mem

    if act == 'sigmoid':
        dZ = sigmoid_backprop(dA, act_mem)
    elif act == 'relu':
        dZ = relu_backprop(dA, act_mem)

    dA_prev, dW, db = lin_back(dZ, lin_mem)

    return dA_prev, dW, db


# Cost function used in classification problems
def cross_entropy(Y, Ypr):
    m = Y.shape[1]

    cost = 1 / m * (- np.dot(Y, np.log(Ypr).T) - np.dot(1 - Y, np.log(1 - Ypr).T))

    cost = np.squeeze(cost)  # [[cost]] -> cost
    assert (cost.shape == ())

    return cost


# Derivative of cost function to get nn parameter gradients
def cross_entropy_back(Y, Ypr):
    dY = - (np.divide(Y, Ypr) - np.divide(1 - Y, 1 - Ypr))

    assert (dY.shape == Y.shape)

    return dY


# Cost function used for regression problems
def mse(Y, Ypr):
    m = Y.shape[1]

    cost = 1 / m * np.sum(np.square(Y - Ypr))

    cost = np.squeeze(cost)  # [[cost]] -> cost
    assert (cost.shape == ())

    return cost


# Derivative of cost function used to get nn parameter gradients
def mse_back(Y, Ypr):
    dY = Ypr - Y

    assert (dY.shape == Y.shape)

    return dY


# L2 regularization on cost function to push weights to lower values for faster gradient descent
def cost_L2(Y, Ypr, param, lambd, output_type):
    m = Y.shape[1]

    depth = len(param) // 2
    reg_term = 0

    for i in range(1, depth + 1):
        W = param["W" + str(i)]
        reg_term += np.sum(np.square(W))

    L2_regularization_cost = lambd / (2 * m) * reg_term

    if output_type == 'regression':
        loss = mse(Ypr, Y)
    elif output_type == 'classification':
        loss = cross_entropy(Ypr, Y)
    cost = loss + L2_regularization_cost

    assert (cost.shape == ())

    return cost


# Full combination of function to produce an output for an input/entry
def model_forw(X, param, output_type):
    mem = []
    A = X

    depth = len(param) // 2
    for i in range(1, depth):
        A_prev = A
        A, temp_mem = lin_act_forw(A_prev, param['W' + str(i)], param['b' + str(i)], act='relu')

        mem.append(temp_mem)

    if output_type == 'regression':
        Ypr, temp_mem = lin_act_forw(A, param['W' + str(depth)], param['b' + str(depth)], act='relu')
        mem.append(temp_mem)

    elif output_type == 'classification':
        Ypr, temp_mem = lin_act_forw(A, param['W' + str(depth)], param['b' + str(depth)], act='sigmoid')
        mem.append(temp_mem)

    assert (Ypr.shape == (param['W' + str(depth)].shape[0], X.shape[1]))

    return Ypr, mem


# Full combination of function to do back propagation, providing the gradients of parameters
# for a single training example
def model_back(Y, Ypr, mem, output_type):
    grads = {}
    depth = len(mem)
    Y = Y.reshape(Ypr.shape)

    # Initializing the backpropagation
    cur_mem = mem[depth - 1]

    if output_type == 'classification':
        dY = cross_entropy_back(Y, Ypr)
        dA_prev_temp, dW_temp, db_temp = lin_act_back(dY, cur_mem, act="sigmoid")

        grads["dA" + str(depth - 1)] = dA_prev_temp
        grads["dW" + str(depth)] = dW_temp
        grads["db" + str(depth)] = db_temp

    elif output_type == 'regression':
        dY = mse_back(Y, Ypr)
        dA_prev_temp, dW_temp, db_temp = lin_act_back(dY, cur_mem, act="relu")

        grads["dA" + str(depth - 1)] = dA_prev_temp
        grads["dW" + str(depth)] = dW_temp
        grads["db" + str(depth)] = db_temp

    for i in reversed(range(depth - 1)):
        cur_mem = mem[i]
        dA_prev_temp, dW_temp, db_temp = lin_act_back(grads["dA" + str(i + 1)], cur_mem, act="relu")

        grads["dA" + str(i)] = dA_prev_temp
        grads["dW" + str(i + 1)] = dW_temp
        grads["db" + str(i + 1)] = db_temp

    return grads


# Implementation of adam optimisation.
def adam_update(it, dW, V, S, beta1, beta2, epsilon):

    V = beta1 * V + (1 - beta1) * dW
    S = beta2 * S + (1 - beta2) * np.square(dW)

    V_corr = V / np.power(1 - beta1, it)
    S_corr = S / np.power(1 - beta2, it)

    dW = V_corr / np.sqrt(S_corr + epsilon)

    return dW, V, S


# Function to update nn parameters given gradients and the wanted optimizations.
# Weighted decay can be activated though by default the system uses L2 regularization.
def update_param(param, grads, learning_rate, lambd, it, adam_param,
                 weight_decay=False, adam=True, beta1=0.9, beta2=0.999, epsilon=0.00000001):

    depth = len(param) // 2

    if not weight_decay:
        reg = (1 - lambd)  # weight decay opt term
    else:
        reg = (1 - 2 * lambd)  # L2 opt term

    for i in range(1, depth + 1):
        dW = grads["dW" + str(i)]
        db = grads["db" + str(i)]

        if adam:
            if it == 0:
                V = 0
                S = 0
            else:
                V = adam_param["V" + str(i)]
                S = adam_param["S" + str(i)]

            dW, V, S = adam_update(it, dW, V, S, beta1, beta2, epsilon)

            adam_param["V" + str(i)] = V
            adam_param["S" + str(i)] = S

        param["W" + str(i)] = param["W" + str(i)] * reg - learning_rate * dW
        param["b" + str(i)] = param["b" + str(i)] * reg - learning_rate * db

    return param, adam_param
