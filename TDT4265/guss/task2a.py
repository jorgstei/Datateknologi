from math import sqrt
import numpy as np
import utils
import typing
import math
import time
np.random.seed(1)


def pre_process_images(X: np.ndarray):
    """
    Args:
        X: images of shape [batch size, 784] in the range (0, 255)
    Returns:
        X: images of shape [batch size, 785] normalized as described in task2a
    """
    assert X.shape[1] == 784,\
        f"X.shape[1]: {X.shape[1]}, should be 784"
    # TODO implement this function (Task 2a)
    X = X.astype(float)
    temp = np.zeros((X.shape[0], 785), dtype=float)

    avg = np.average(X)
    std = np.std(X)

    for i in range(len(X)):
        for j in range(len(X[0])):
            temp[i][j] = ((X[i][j]-avg)/std)
        temp[:, -1] = 1.0 # Bias trick
    X = temp
    return X


def cross_entropy_loss(targets: np.ndarray, outputs: np.ndarray):
    """
    Args:
        targets: labels/targets of each image of shape: [batch size, num_classes]
        outputs: outputs of model of shape: [batch size, num_classes]
    Returns:
        Cross entropy error (float)
    """


    assert targets.shape == outputs.shape,\
        f"Targets shape: {targets.shape}, outputs: {outputs.shape}"
    # TODO: Implement this function (copy from last assignment)
    
    N = len(targets)
    loss = float(-np.sum(targets*np.log(outputs)))/N

    return loss


class SoftmaxModel:

    def __init__(self,
                 # Number of neurons per layer
                 neurons_per_layer: typing.List[int],
                 use_improved_sigmoid: bool,  # Task 3a hyperparameter
                 use_improved_weight_init: bool  # Task 3c hyperparameter
                 ):
        # Always reset random seed before weight init to get comparable results.
        np.random.seed(1)
        # Define number of input nodes
        self.I = 785
        self.use_improved_sigmoid = use_improved_sigmoid

        # Define number of output nodes
        # neurons_per_layer = [64, 10] indicates that we will have two layers:
        # A hidden layer with 64 neurons and a output layer with 10 neurons.
        self.neurons_per_layer = neurons_per_layer

        print("Using improved sigmoid:", self.use_improved_sigmoid)
        # Initialize the weights
        self.ws = []
        prev = self.I
        if use_improved_weight_init:
            for size in self.neurons_per_layer:
                w_shape = (prev, size)
                print("Initializing weight to shape using improved w:", w_shape)
                fan_in = 1/sqrt(prev)
                w = np.random.normal(0, fan_in, w_shape)
                self.ws.append(w)
                prev = size
        else:
            for size in self.neurons_per_layer:
                w_shape = (prev, size)
                print("Initializing weight to shape:", w_shape)
                w = np.zeros(w_shape)
                for i in range(len(w)):
                    w[i] = np.random.rand() * 2 - 1
                self.ws.append(w)
                prev = size
                
        self.grads = [None] * len(self.neurons_per_layer)
        print("Made grads", self.grads, "with len", len(self.neurons_per_layer))

        self.a = []
        self.z = []


    def forward(self, X: np.ndarray) -> np.ndarray:
        # 
        # Args:
        #     X: images of shape [batch size, 785]
        # Returns:
        #     y: output of model with shape [batch size, num_outputs]
        #
        # TODO implement this function (Task 2b)
        # HINT: For performing the backward pass, you can save intermediate activations in variables in the forward pass.
        # such as self.hidden_layer_output = ...

        # self.z_1 = X@w_1
        # if self.use_improved_sigmoid:
        #     self.a_1 = np.dot(1.7159, np.tanh((2*self.z_1/3)))
        # else:
        #     self.a_1 = 1 / (1 + np.exp(-self.z_1))
        # self.z_2 = self.a_1@w_2

        self.a.append(X)
        input = X
        for i in range(len(self.neurons_per_layer)):
            w = self.ws[i]
            z = input@w
            self.z.append(z)
            if(i != len(self.neurons_per_layer) - 1):
                if(self.use_improved_sigmoid):
                    input = np.dot(1.7159, np.tanh((2*z/3)))
                    self.a.append(input)
                else:
                    input = 1 / (1 + np.exp(-z))
                    self.a.append(input)

        y = (np.exp(self.z[len(self.z) - 1]) / np.sum(np.exp(self.z[len(self.z) - 1]), keepdims=True, axis=1))
        # print("Y\n", y)
        # time.sleep(5)
        return y

    def backward(self, X: np.ndarray, outputs: np.ndarray,
                 targets: np.ndarray) -> None:
        """
        Computes the gradient and saves it to the variable self.grad

        Args:
            X: images of shape [batch size, 785]
            outputs: outputs of model of shape: [batch size, num_outputs]
            targets: labels/targets of each image of shape: [batch size, num_classes]
        """
        # TODO implement this function (Task 2b)
        assert targets.shape == outputs.shape,\
            f"Output shape: {outputs.shape}, targets: {targets.shape}"
        # A list of gradients.
        # For example, self.grads[0] will be the gradient for the first hidden layer
        
        
        grad_k = (self.a[-1].T@(outputs-targets))/X.shape[0]
        self.grads[-1] = grad_k
        
        # Initialize prev delta to delta_k
        prev_delta = (outputs-targets).T
        sig_derivative = None
        # Exclude last layer because we've already calculated its grad
        for i, el in reversed(list(enumerate(self.neurons_per_layer[:-1]))):
            #print(i)
            if self.use_improved_sigmoid:
                sig_derivative = np.dot(1.14393, 1 - np.power(np.tanh((2*self.z[i]/3)), 2))
            else:

                sig_derivative = 1/(1+np.exp(-self.z[i])) * (1-1/(1+np.exp(-self.z[i])))

            w = self.ws[i+1]

            delta_j = sig_derivative.T * (w@prev_delta)
            prev_delta = delta_j
            grad_j = (delta_j @ self.a[i]).T/X.shape[0]
            self.grads[i] = grad_j

        print("Grad\n", self.grads)
        time.sleep(5)

        #print(len(self.ws), len(self.grads), len(self.ws[0]), len(self.grads[0]))
        for grad, w in zip(self.grads, self.ws):
            #print(grad.shape, "vs", w.shape)
            assert grad.shape == w.shape,\
                f"Expected the same shape. Grad shape: {grad.shape}, w: {w.shape}."
            

    def zero_grad(self) -> None:
        self.grads = [None for i in range(len(self.ws))]
 

def one_hot_encode(Y: np.ndarray, num_classes: int):
    """
    Args:
        Y: shape [Num examples, 1]
        num_classes: Number of classes to use for one-hot encoding
    Returns:
        Y: shape [Num examples, num classes]
    """
    # TODO: Implement this function (copy from last assignment)
    arr = np.zeros((Y.shape[0], num_classes))
    for i in range(len(arr)):
        arr[i][Y[i]] = 1

    return arr


def gradient_approximation_test(
        model: SoftmaxModel, X: np.ndarray, Y: np.ndarray):
    """
        Numerical approximation for gradients. Should not be edited. 
        Details about this test is given in the appendix in the assignment.
    """
    epsilon = 1e-3
    for layer_idx, w in enumerate(model.ws):
        for i in range(w.shape[0]):
            for j in range(w.shape[1]):
                orig = model.ws[layer_idx][i, j].copy()
                model.ws[layer_idx][i, j] = orig + epsilon
                logits = model.forward(X)
                cost1 = cross_entropy_loss(Y, logits)
                model.ws[layer_idx][i, j] = orig - epsilon
                logits = model.forward(X)
                cost2 = cross_entropy_loss(Y, logits)
                gradient_approximation = (cost1 - cost2) / (2 * epsilon)
                model.ws[layer_idx][i, j] = orig
                # Actual gradient
                logits = model.forward(X)
                model.backward(X, logits, Y)
                #print(model.grads[i])
                difference = gradient_approximation - \
                    model.grads[layer_idx][i, j]
                assert abs(difference) <= epsilon**2,\
                    f"Calculated gradient is incorrect. " \
                    f"Layer IDX = {layer_idx}, i={i}, j={j}.\n" \
                    f"Approximation: {gradient_approximation}, actual gradient: {model.grads[layer_idx][i, j]}\n" \
                    f"If this test fails there could be errors in your cross entropy loss function, " \
                    f"forward function or backward function"


if __name__ == "__main__":
    # Simple test on one-hot encoding
    Y = np.zeros((1, 1), dtype=int)
    Y[0, 0] = 3
    Y = one_hot_encode(Y, 10)
    assert Y[0, 3] == 1 and Y.sum() == 1, \
        f"Expected the vector to be [0,0,0,1,0,0,0,0,0,0], but got {Y}"

    X_train, Y_train, *_ = utils.load_full_mnist()
    # print("Mean:", np.mean(X_train))
    # print("STD:", np.std(X_train))
    X_train = pre_process_images(X_train)
    Y_train = one_hot_encode(Y_train, 10)
    assert X_train.shape[1] == 785,\
        f"Expected X_train to have 785 elements per image. Shape was: {X_train.shape}"

    neurons_per_layer = [64, 10]
    use_improved_sigmoid = False
    use_improved_weight_init = False
    model = SoftmaxModel(
        neurons_per_layer, use_improved_sigmoid, use_improved_weight_init)

    # Gradient approximation check for 100 images
    X_train = X_train[:100]
    Y_train = Y_train[:100]
    for layer_idx, w in enumerate(model.ws):
        model.ws[layer_idx] = np.random.uniform(-1, 1, size=w.shape)

    gradient_approximation_test(model, X_train, Y_train)