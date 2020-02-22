import numpy as np

""" Verify if adam is ok!!! """


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


def sigmoid(Z):
    A = 1 / (1 + np.exp(-Z))
    mem = Z

    assert (A.shape == Z.shape)

    return A, mem


def sigmoid_backprop(dA, mem):
    Z = mem

    a = 1 / (1 + np.exp(-Z))
    dZ = dA * a * (1 - a)

    assert (dZ.shape == Z.shape)

    return dZ


def relu(Z):
    A = np.maximum(0, Z)
    mem = Z

    assert (A.shape == Z.shape)

    return A, mem


def relu_backprop(dA, mem):
    Z = mem

    dZ = np.array(dA, copy=True)

    print(dZ.shape)
    print(Z.shape)
    dZ[Z <= 0] = 0

    assert (dZ == dA)

    return dZ


def lin_forw(A, W, b):
    Z = np.dot(W, A) + b
    mem = (Z, A, b)

    assert (Z.shape == (W.shape[0], A.shape[1]))

    return Z, mem


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


def lin_act_forw(A_prev, W, b, act):
    Z, lin_mem = lin_forw(A_prev, W, b)

    if act == 'sigmoid':
        A, act_mem = sigmoid(Z)
    elif act == 'relu':
        A, act_mem = relu(Z)

    mem = (lin_mem, act_mem)

    assert (A.shape == (W.shape[0], A_prev.shape[1]))

    return A, mem


def lin_act_back(dA, mem, act):
    lin_mem, act_mem = mem

    if act == 'sigmoid':
        dZ = sigmoid_backprop(dA, act_mem)
    elif act == 'relu':
        dZ = relu_backprop(dA, act_mem)

    dA_prev, dW, db = lin_back(dZ, lin_mem)

    return dA_prev, dW, db


def cross_entropy(Y, Ypr):
    m = Y.shape[1]

    cost = 1 / m * (- np.dot(Y, np.log(Ypr).T) - np.dot(1 - Y, np.log(1 - Ypr).T))

    cost = np.squeeze(cost)  # [[cost]] -> cost
    assert (cost.shape == ())

    return cost


def cross_entropy_back(Y, Ypr):
    dY = - (np.divide(Y, Ypr) - np.divide(1 - Y, 1 - Ypr))

    assert (dY.shape == Y.shape)

    return dY


def mse(Y, Ypr):
    m = Y.shape[1]

    cost = 1 / m * np.sum(np.sqrt(Y - Ypr))

    cost = np.squeeze(cost)  # [[cost]] -> cost
    assert (cost.shape == ())

    return cost


def mse_back(Y, Ypr):
    dY = Ypr - Y

    assert (dY.shape == Y.shape)

    return dY


def cost_L2(Y, Ypr, param, lambd, output_type):
    m = Y.shape[1]

    depth = len(param)
    reg_term = 0

    for i in range(1, depth):
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


def model_forw(X, param, output_type):
    mem = []
    A = X

    depth = len(param) // 2
    for i in range(1, depth):
        A_prev = A
        A, temp_mem = lin_act_forw(A_prev, param['W' + str(i)], param['b' + str(i)], act='relu')

        mem.append(temp_mem)

    if output_type == 'regression':
        Ypr, temp_mem = lin_act_forw(A, param['W' + str(depth)], param['b' + str(depth)], act='sigmoid')
    elif output_type == 'classification':
        Ypr, temp_mem = lin_act_forw(A, param['W' + str(depth)], param['b' + str(depth)], act='relu')
        mem.append(temp_mem)

    assert (Ypr.shape == (param['W' + str(depth)].shape[0], X.shape[1]))

    return Ypr, mem


def model_back(Y, Ypr, mem, output_type):
    grads = {}
    depth = len(mem)
    Y = Y.reshape(Ypr.shape)

    # Initializing the backpropagation
    cur_mem = mem[depth - 1]

    if output_type == 'classification':
        dY = mse_back(Y, Ypr)
        dA_prev_temp, dW_temp, db_temp = lin_act_back(dY, cur_mem, act="relu")

        grads["dA" + str(depth - 1)] = dA_prev_temp
        grads["dW" + str(depth)] = dW_temp
        grads["db" + str(depth)] = db_temp

    elif output_type == 'regression':
        dY = cross_entropy_back(Y, Ypr)
        dA_prev_temp, dW_temp, db_temp = lin_act_back(dY, cur_mem, act="sigmoid")

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


def adam(it, dW, V, S, beta1, beta2, epsilon):

    V = beta1 * V + (1 - beta1) * dW
    S = beta2 * S + (1 - beta2) * np.square(dW)

    V_corr = V / np.power(1 - beta1, it)
    S_corr = S / np.power(1 - beta2, it)

    dW = V_corr / np.sqrt(S_corr + epsilon)

    return dW, V, S


def update_param(param, grads, learning_rate, lambd, it,
                 weight_decay=False, adam=True, beta1=0.9, beta2=0.999, epsilon=0.00000001):

    depth = len(param) // 2

    if not weight_decay:
        reg = (1 - lambd)  # weight decay opt term
    else:
        reg = (1 - 2 * lambd)  # L2 opt term

    for i in range(1, depth):
        dW = grads["dW" + str(i)]

        if adam:
            if it == 0:
                V = 0
                S = 0
            else:
                V = param["V" + str(i)]
                S = param["S" + str(i)]

            dW, V, S = adam(it, dW, V, S, beta1, beta2, epsilon)

            param["V" + str(i)] = V
            param["S" + str(i)] = S

        param["W" + str(i)] = param["W" + str(i)] * reg - learning_rate * dW
        param["b" + str(i)] = param["b" + str(i)] * reg - learning_rate * dW

    return param
