import numpy as np


# At aparam init he -> dvivide by sqrt of layer size as weights for complexity
# L2 reg -> Check it!!
#  Why initialise backprop with that term??

def sigmoid(Z):
    A = 1 / (1 + np.exp(-Z))
    mem = Z

    assert (A.shape == Z.shape)

    return A, mem


def relu(Z):
    A = np.maximum(0, Z)
    mem = Z

    assert (A.shape == Z.shape)

    return A, mem


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


def lin_forw(A, W, b):
    Z = np.dot(W, A) + b
    mem = (Z, A, b)

    assert (Z.shape == (W.shape[0], A.shape[1]))

    return Z, mem


def lin_act_forw(A_prev, W, b, act):
    Z, lin_mem = lin_forw(A_prev, W, b)

    if act == 'sigmoid':
        A, act_mem = sigmoid(Z)
    elif act == 'relu':
        A, act_mem = relu(Z)

    mem = (lin_mem, act_mem)

    assert (A.shape == (W.shape[0], A_prev.shape[1]))

    return A, mem


def model_forw(X, param, output_type):
    mem = []
    A = X

    depth = len(param) // 2
    for i in range(1, depth):
        A_prev = A
        A, temp_mem = lin_act_forw(A_prev, param['W' + str(i)], param['b' + str(i)], act='relu')

        mem.append(temp_mem)

    if output_type == 'regression':
        Af, temp_mem = lin_act_forw(A, param['W' + str(depth)], param['b' + str(depth)], act='relu')
    elif output_type == 'classification':
        Af, temp_mem = lin_act_forw(A, param['W' + str(depth)], param['b' + str(depth)], act='sigmoid')
        mem.append(temp_mem)

    assert (Af.shape == (1, X.shape[1]))

    return Af, mem


def entropy_cost(Af, Y):
    m = Y.shape[1]

    cost = 1 / m * (- np.dot(Y, np.log(Af).T) - np.dot(1 - Y, np.log(1 - Af).T))

    cost = np.squeeze(cost)  # [[cost]] -> cost
    assert (cost.shape == ())

    return cost


def mean_sq_error(Af, Y):
    m = Y.shape[1]

    cost = 1 / m * np.sum(np.sqrt(Y - Af))

    cost = np.squeeze(cost)  # [[cost]] -> cost
    assert (cost.shape == ())

    return cost


def cost_L2_reg(Af, Y, param, lambd, output_type):
    m = Y.shape[1]

    depth = len(param)
    reg_term = 0

    for i in range(1, depth):
        W = param["W" + str(i)]
        reg_term += np.sum(np.sqrt(W))

    L2_regularization_cost = lambd / (2 * m) * reg_term

    if output_type == 'regression':
        loss = mean_sq_error(Af, Y)
    elif output_type == 'classification':
        loss = entropy_cost(Af, Y)
    cost = loss + L2_regularization_cost

    assert (cost.shape == ())

    return cost


def sigmoid_backprop(dA, mem):
    Z = mem

    a = 1 / (1 + np.exp(-Z))
    dZ = dA * a * (1 - a)

    assert (dZ.shape == dA.shape)

    return dZ


def relu_backprop(dA, mem):
    Z = mem

    dZ = dA
    print(Z.shape)
    print(dZ.shape)
    dZ[Z <= 0] = 0

    assert (dZ == dA)

    return dZ


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


def lin_act_back(dA, mem, act):
    lin_mem, act_mem = mem

    if act == 'sigmoid':
        dZ = sigmoid_backprop(dA, act_mem)
    elif act == 'relu':
        dZ = relu_backprop(dA, act_mem)

    dA_prev, dW, db = lin_back(dZ, lin_mem)

    return dA_prev, dW, db


def model_back(Af, Y, mem, output_type):
    grads = {}
    depth = len(mem)
    m = Af.shape[1]
    Y = Y.reshape(Af.shape)

    # Initializing the backpropagation
    dAf = - (np.divide(Y, Af) - np.divide(1 - Y, 1 - Af))

    cur_mem = mem[depth - 1]

    if output_type == 'regression':
        grads["dA" + str(depth - 1)], grads["dW" + str(depth)], grads["db" + str(depth)] = lin_act_back(dAf, cur_mem,
                                                                                                        act="relu")
    elif output_type == 'classification':
        grads["dA" + str(depth - 1)], grads["dW" + str(depth)], grads["db" + str(depth)] = lin_act_back(dAf, cur_mem,
                                                                                                        act="sigmoid")
    for i in reversed(range(depth - 1)):
        cur_mem = mem[i]
        dA_prev_temp, dW_temp, db_temp = lin_act_back(grads["dA" + str(i + 1)], cur_mem, act="relu")

        grads["dA" + str(i)] = dA_prev_temp
        grads["dW" + str(i + 1)] = dW_temp
        grads["db" + str(i + 1)] = db_temp

    return grads


def update_param(param, grads, learning_rate):
    depth = len(param) // 2

    for i in range(depth):
        param["W" + str(i + 1)] = param["W" + str(i + 1)] - learning_rate * grads["dW" + str(i + 1)]
        param["b" + str(i + 1)] = param["b" + str(i + 1)] - learning_rate * grads["db" + str(i + 1)]

    return param


"""
def dictionary_to_vector(parameters):
    keys = []
    count = 0
    for key in ["W1", "b1", "W2", "b2", "W3", "b3"]:

        # flatten parameter
        new_vector = np.reshape(parameters[key], (-1, 1))
        keys = keys + [key] * new_vector.shape[0]

        if count == 0:
            theta = new_vector
        else:
            theta = np.concatenate((theta, new_vector), axis=0)
        count = count + 1

    return theta, keys


def vector_to_dictionary(theta):
    parameters = {}
    parameters["W1"] = theta[:20].reshape((5, 4))
    parameters["b1"] = theta[20:25].reshape((5, 1))
    parameters["W2"] = theta[25:40].reshape((3, 5))
    parameters["b2"] = theta[40:43].reshape((3, 1))
    parameters["W3"] = theta[43:46].reshape((1, 3))
    parameters["b3"] = theta[46:47].reshape((1, 1))

    return parameters


def gradients_to_vector(gradients):
    count = 0
    for key in ["dW1", "db1", "dW2", "db2", "dW3", "db3"]:
        # flatten parameter
        new_vector = np.reshape(gradients[key], (-1, 1))

        if count == 0:
            theta = new_vector
        else:"""
