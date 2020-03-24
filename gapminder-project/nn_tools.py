import numpy as np

""" Complet the implimentation for L2 reg and weighted decay, use in forw & back prop at same time!!! """
""" Grad descent inconsistent, sometimes work fine, sometimes has bad gradients"""


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


# Relu is used as the activation function for hidden layers, as well as for regression problems
def relu(Z):
    A = np.maximum(0, Z)
    mem = Z

    assert (A.shape == Z.shape)

    return A, mem


def linear(Z):
    A = Z
    mem = Z

    return A, mem


# Linear forward step to aply the weights of a layer
def forward_prop(A, W, b):
    Z = np.dot(W, A) + b
    mem = (A, W, b)

    assert (Z.shape == (W.shape[0], A.shape[1]))

    return Z, mem


# Full step forward, combining the linear forward step with the activation function to create an output per layer
def lin_act_forw(A_prev, W, b, act):
    Z, lin_mem = forward_prop(A_prev, W, b)

    if act == 'sigmoid':
        A, act_mem = sigmoid(Z)
    elif act == 'relu':
        A, act_mem = relu(Z)
    elif act == 'linear':
        A, act_mem = linear(Z)

    mem = (lin_mem, act_mem)

    assert (A.shape == (W.shape[0], A_prev.shape[1]))

    return A, mem


# Cost function used in classification problems
def cross_entropy(Y, Ypr):
    m = Y.shape[1]

    cost = 1 / m * (- np.dot(Y, np.log(Ypr).T) - np.dot(1 - Y, np.log(1 - Ypr).T))

    cost = np.squeeze(cost)  # [[cost]] -> cost
    assert (cost.shape == ())

    return cost


# Cost function used for regression problems
def mse(Y, Ypr):
    m = Y.shape[1]

    cost = 1 / m * np.sum(np.square(Y - Ypr))

    cost = np.squeeze(cost)  # [[cost]] -> cost
    assert (cost.shape == ())

    return cost


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
        loss = mse(Y, Ypr)
    elif output_type == 'classification':
        loss = cross_entropy(Y, Ypr)
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
        Ypr, temp_mem = lin_act_forw(A, param['W' + str(depth)], param['b' + str(depth)], act='linear')

    elif output_type == 'classification':
        Ypr, temp_mem = lin_act_forw(A, param['W' + str(depth)], param['b' + str(depth)], act='sigmoid')

    mem.append(temp_mem)

    assert (Ypr.shape == (1, X.shape[1]))

    return Ypr, mem


# Derivative of the sigmoid function used during backpropagation to get the nn parameter gradients
def sigmoid_backprop(dA, mem):
    Z = mem

    a = 1 / (1 + np.exp(-Z))
    dZ = dA * a * (1 - a)

    assert (dZ.shape == Z.shape)

    return dZ


# Derivative of the sigmoid function used during backpropagation to get the nn parameter gradients
def relu_backprop(dA, mem):
    Z = mem

    dZ = np.array(dA, copy=True)
    dZ[Z <= 0] = 0

    assert (dZ.shape == dA.shape)

    return dZ


def linear_back(dA):
    dZ = np.array(dA, copy=True)

    assert (dZ.shape == dA.shape)

    return dZ


# Derivative to get the gradients fr the nn parameters
def back_prop(dZ, mem):
    A_prev, W, b = mem
    m = A_prev.shape[1]

    dW = 1. / m * np.dot(dZ, A_prev.T)
    db = 1. / m * np.sum(dZ, axis=1, keepdims=True)
    dA_prev = np.dot(W.T, dZ)

    assert (dW.shape == W.shape)
    assert (db.shape == b.shape)
    assert (dA_prev.shape == A_prev.shape)

    return dA_prev, dW, db


# Full step backwards, combining the dirivative of lin forward step and activation function
# to get the gradients of per layer
def lin_act_back(dA, mem, act):
    lin_mem, act_mem = mem

    if act == 'sigmoid':
        dZ = sigmoid_backprop(dA, act_mem)
    elif act == 'relu':
        dZ = relu_backprop(dA, act_mem)
    elif act == 'linear':
        dZ = linear_back(dA)

    dA_prev, dW, db = back_prop(dZ, lin_mem)

    return dA_prev, dW, db


# Derivative of cost function to get nn parameter gradients
def cross_entropy_back(Y, Ypr):
    dY = - (np.divide(Y, Ypr) + np.divide(1 - Y, 1 - Ypr))

    assert (dY.shape == Y.shape)

    return dY


# Derivative of cost function used to get nn parameter gradients
def mse_back(Y, Ypr):
    dY = 2 * (Ypr - Y)

    assert (dY.shape == Y.shape)

    return dY


def cost_weighted_back(Y, Ypr, param, lambd, output_type):
    m = Y.shape[1]

    depth = len(param) // 2
    reg_term = 0

    for i in range(1, depth + 1):
        W = param["W" + str(i)]
        reg_term += np.sum(np.square(W))

    L2_regularization_cost = lambd / m * reg_term

    if output_type == 'regression':
        loss = mse_back(Y, Ypr)
    elif output_type == 'classification':
        loss = cross_entropy(Y, Ypr)
    cost = loss + L2_regularization_cost

    assert (cost.shape == ())

    return cost


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

    elif output_type == 'regression':
        dY = mse_back(Y, Ypr)
        dA_prev_temp, dW_temp, db_temp = lin_act_back(dY, cur_mem, act="linear")

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


def initialize_adam(param):
    depth = len(param) // 2
    V = {}
    S = {}

    for i in range(1, depth + 1):
        V["dW" + str(i)] = np.zeros(param["W" + str(i)].shape)
        V["db" + str(i)] = np.zeros(param["b" + str(i)].shape)

        S["dW" + str(i)] = np.zeros(param["W" + str(i)].shape)
        S["db" + str(i)] = np.zeros(param["b" + str(i)].shape)

    return V, S


# Implementation of adam optimisation.
def update_adam(param, grads, V, S, it, learning_rate, lambd, L2, beta1=0.9, beta2=0.999, epsilon=1e-8):
    depth = len(param) // 2
    V_corr = {}
    S_corr = {}
    reg = 1

    if L2:
        reg = (1 - 2 * lambd)

    for i in range(depth):
        V["dW" + str(i + 1)] = beta1 * V["dW" + str(i + 1)] + (1 - beta1) * grads['dW' + str(i + 1)]
        V["db" + str(i + 1)] = beta1 * V["db" + str(i + 1)] + (1 - beta1) * grads['db' + str(i + 1)]

        V_corr["dW" + str(i + 1)] = V["dW" + str(i + 1)] / (1 - np.power(beta1, it))
        V_corr["db" + str(i + 1)] = V["db" + str(i + 1)] / (1 - np.power(beta1, it))

        S["dW" + str(i + 1)] = beta2 * S["dW" + str(i + 1)] + (1 - beta2) * np.power(grads['dW' + str(i + 1)], 2)
        S["db" + str(i + 1)] = beta2 * S["db" + str(i + 1)] + (1 - beta2) * np.power(grads['db' + str(i + 1)], 2)

        S_corr["dW" + str(i + 1)] = S["dW" + str(i + 1)] / (1 - np.power(beta2, it))
        S_corr["db" + str(i + 1)] = S["db" + str(i + 1)] / (1 - np.power(beta2, it))

        param["W" + str(i + 1)] = param["W" + str(i + 1)] * reg - learning_rate * V_corr["dW" + str(i + 1)] / (
                np.sqrt(S_corr["dW" + str(i + 1)]) + epsilon)
        param["b" + str(i + 1)] = param["b" + str(i + 1)] * reg - learning_rate * V_corr["db" + str(i + 1)] / (
                np.sqrt(S_corr["db" + str(i + 1)]) + epsilon)

    return param, V, S


# Function to update nn parameters given gradients and the wanted optimizations.
# Weighted decay can be activated though by default the system uses L2 regularization.
def update_gd(param, grads, learning_rate, lambd, L2=True):
    depth = len(param) // 2
    reg = 1

    if L2:
        reg = (1 - 2 * lambd)  # L2 opt term
    # elif weight_decay:
    #    reg = (1 - lambd)  # weight decay opt term

    for i in range(1, depth + 1):
        param["W" + str(i)] = param["W" + str(i)] * reg - learning_rate * grads["dW" + str(i)]
        param["b" + str(i)] = param["b" + str(i)] * reg - learning_rate * grads["db" + str(i)]

    return param


def grad_checking(layers, nn_param, grads, X, Y, epsilon=1e-7):
    param_val = dict_to_vect(nn_param, layers)
    grad_val = grad_to_vect(grads, layers)

    num_param = param_val.shape[0]

    J_plus = np.zeros((num_param, 1))
    J_minus = np.zeros((num_param, 1))
    gradapprox = np.zeros((num_param, 1))

    for i in range(num_param):
        thetaplus = np.copy(param_val)
        thetaplus[i][0] = thetaplus[i][0] + epsilon
        Y_plus, _ = model_forw(X, vect_to_dict(thetaplus, layers), 'regression')

        thetaminus = np.copy(param_val)
        thetaminus[i][0] = thetaminus[i][0] - epsilon
        Y_minus, _ = model_forw(X, vect_to_dict(thetaminus, layers), 'regression')

        J_plus[i] = np.square(Y - np.squeeze(Y_plus))
        J_minus[i] = np.square(Y - np.squeeze(Y_minus))

        gradapprox[i] = (J_plus[i] - J_minus[i]) / (2 * epsilon)

    num = np.linalg.norm(grad_val - gradapprox)
    den = np.linalg.norm(grad_val) + np.linalg.norm(gradapprox)

    diff = num / den
    if diff > epsilon:
        print(f"Bad gradients")
    else:
        print("Good gradients")
    print(f"diff: {diff}")
    return diff


def dict_to_vect(param, layers):
    count = 0

    for i in range(1, len(layers)):
        W_vector = np.reshape(param['W' + str(i)], (-1, 1))
        b_vector2 = np.reshape(param['b' + str(i)], (-1, 1))

        if count == 0:
            theta = W_vector
        else:
            theta = np.concatenate((theta, W_vector), axis=0)

        theta = np.concatenate((theta, b_vector2), axis=0)
        count += 1

    return theta


def vect_to_dict(theta, layers):
    param = {}
    prev_size = 0

    for i in range(1, len(layers)):
        size = prev_size + layers[i] * layers[i - 1]
        param["W" + str(i)] = theta[prev_size:size].reshape((layers[i], layers[i - 1]))
        prev_size = size
        size = prev_size + layers[i]
        param["b" + str(i)] = theta[prev_size:size].reshape((layers[i], 1))
        prev_size = size

    return param


def grad_to_vect(grads, layers):
    count = 0

    for i in range(1, len(layers)):
        new_vector = np.reshape(grads['dW' + str(i)], (-1, 1))
        new_vector2 = np.reshape(grads['db' + str(i)], (-1, 1))

        if count == 0:
            theta = new_vector
        else:
            theta = np.concatenate((theta, new_vector), axis=0)

        theta = np.concatenate((theta, new_vector2), axis=0)

        count += 1

    return theta
