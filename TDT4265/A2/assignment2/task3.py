from string import digits
import numpy as np
import utils
import matplotlib.pyplot as plt
from task2a import pre_process_images
from trainer import BaseTrainer
from task3a import cross_entropy_loss, SoftmaxModel, one_hot_encode
np.random.seed(0)


def calculate_accuracy(X: np.ndarray, targets: np.ndarray, model: SoftmaxModel) -> float:
    """
    Args:
        X: images of shape [batch size, 785]
        targets: labels/targets of each image of shape: [batch size, 10]
        model: model of class SoftmaxModel
    Returns:
        Accuracy (float)
    """
    # TODO: Implement this function (task 3c)
    counter = 0
    # Get evaluations
    predictions = model.forward(X)
    for i, ev in enumerate(predictions):
        max_val = max(ev)
        idx = np.where(ev == max_val)[0][0]
        idy = np.where(targets[i] == 1.0)[0][0]
        if idx == idy:
            counter += 1

    return counter / float(len(targets))


class SoftmaxTrainer(BaseTrainer):

    def train_step(self, X_batch: np.ndarray, Y_batch: np.ndarray):
        """
        Perform forward, backward and gradient descent step here.
        The function is called once for every batch (see trainer.py) to perform the train step.
        The function returns the mean loss value which is then automatically logged in our variable self.train_history.

        Args:
            X: one batch of images
            Y: one batch of labels
        Returns:
            loss value (float) on batch
        """
        # TODO: Implement this function (task 3b)
        loss = 0
        predictions = self.model.forward(X_batch)
        self.model.backward(X_batch, predictions, Y_batch)
        self.model.w -= self.model.grad * learning_rate
        loss = cross_entropy_loss(Y_batch, predictions)
        return loss

    def validation_step(self):
        """
        Perform a validation step to evaluate the model at the current step for the validation set.
        Also calculates the current accuracy of the model on the train set.
        Returns:
            loss (float): cross entropy loss over the whole dataset
            accuracy_ (float): accuracy over the whole dataset
        Returns:
            loss value (float) on batch
            accuracy_train (float): Accuracy on train dataset
            accuracy_val (float): Accuracy on the validation dataset
        """
        # NO NEED TO CHANGE THIS FUNCTION
        logits = self.model.forward(self.X_val)
        loss = cross_entropy_loss(Y_val, logits)

        accuracy_train = calculate_accuracy(
            X_train, Y_train, self.model)
        accuracy_val = calculate_accuracy(
            X_val, Y_val, self.model)
        return loss, accuracy_train, accuracy_val


if __name__ == "__main__":
    # hyperparameters DO NOT CHANGE IF NOT SPECIFIED IN ASSIGNMENT TEXT
    num_epochs = 50
    learning_rate = 0.01
    batch_size = 128
    l2_reg_lambda = 0
    shuffle_dataset = True

    # Load dataset
    X_train, Y_train, X_val, Y_val = utils.load_full_mnist()
    X_train = pre_process_images(X_train)
    X_val = pre_process_images(X_val)
    Y_train = one_hot_encode(Y_train, 10)
    Y_val = one_hot_encode(Y_val, 10)

    # ANY PARTS OF THE CODE BELOW THIS CAN BE CHANGED.

    # Intialize model
    model = SoftmaxModel(l2_reg_lambda)
    # Train model
    trainer = SoftmaxTrainer(
        model, learning_rate, batch_size, shuffle_dataset,
        X_train, Y_train, X_val, Y_val,
    )
    train_history, val_history = trainer.train(num_epochs)

    print("Final Train Cross Entropy Loss:",
          cross_entropy_loss(Y_train, model.forward(X_train)))
    print("Final Validation Cross Entropy Loss:",
          cross_entropy_loss(Y_val, model.forward(X_val)))
    print("Final Train accuracy:", calculate_accuracy(X_train, Y_train, model))
    print("Final Validation accuracy:", calculate_accuracy(X_val, Y_val, model))

    # plt.ylim([0.2, .6])
    # utils.plot_loss(train_history["loss"],
    #                 "Training Loss", npoints_to_average=10)
    # utils.plot_loss(val_history["loss"], "Validation Loss")
    # plt.legend()
    # plt.xlabel("Number of Training Steps")
    # plt.ylabel("Cross Entropy Loss - Average")
    # plt.savefig("task3b_softmax_train_loss.png")
    # plt.show()

    # # Plot accuracy
    # plt.ylim([0.89, .93])
    # utils.plot_loss(train_history["accuracy"], "Training Accuracy")
    # utils.plot_loss(val_history["accuracy"], "Validation Accuracy")
    # plt.xlabel("Number of Training Steps")
    # plt.ylabel("Accuracy")
    # plt.legend()
    # plt.savefig("task3b_softmax_train_accuracy.png")
    # plt.show()

    # Train a model with L2 regularization (task 4b)

    X_train, Y_train, X_val, Y_val = utils.load_full_mnist()
    X_train = pre_process_images(X_train)
    X_val = pre_process_images(X_val)
    Y_train = one_hot_encode(Y_train, 10)
    Y_val = one_hot_encode(Y_val, 10)

    model1 = SoftmaxModel(l2_reg_lambda=2.0)
    trainer2 = SoftmaxTrainer(
        model1, learning_rate, batch_size, shuffle_dataset,
        X_train, Y_train, X_val, Y_val,
    )
    train_history_reg01, val_history_reg01 = trainer2.train(num_epochs)

    X_train, Y_train, X_val, Y_val = utils.load_full_mnist()
    X_train = pre_process_images(X_train)
    X_val = pre_process_images(X_val)
    Y_train = one_hot_encode(Y_train, 10)
    Y_val = one_hot_encode(Y_val, 10)

    model2 = SoftmaxModel(l2_reg_lambda=0.2)
    trainer3 = SoftmaxTrainer(
        model2, learning_rate, batch_size, shuffle_dataset,
        X_train, Y_train, X_val, Y_val,
    )
    train_history_reg02, val_history_reg02 = trainer3.train(num_epochs)

    X_train, Y_train, X_val, Y_val = utils.load_full_mnist()
    X_train = pre_process_images(X_train)
    X_val = pre_process_images(X_val)
    Y_train = one_hot_encode(Y_train, 10)
    Y_val = one_hot_encode(Y_val, 10)

    model3 = SoftmaxModel(l2_reg_lambda=0.02)
    trainer4 = SoftmaxTrainer(
        model3, learning_rate, batch_size, shuffle_dataset,
        X_train, Y_train, X_val, Y_val,
    )
    train_history_reg03, val_history_reg03 = trainer4.train(num_epochs)

    X_train, Y_train, X_val, Y_val = utils.load_full_mnist()
    X_train = pre_process_images(X_train)
    X_val = pre_process_images(X_val)
    Y_train = one_hot_encode(Y_train, 10)
    Y_val = one_hot_encode(Y_val, 10)

    model4 = SoftmaxModel(l2_reg_lambda=0.002)
    trainer5 = SoftmaxTrainer(
        model4, learning_rate, batch_size, shuffle_dataset,
        X_train, Y_train, X_val, Y_val,
    )
    train_history_reg04, val_history_reg04 = trainer5.train(num_epochs)
    
    plt.ylim([0.2, .6])
    utils.plot_loss(train_history_reg01["loss"],
                    "Training Loss L = 2.0", npoints_to_average=10)
    utils.plot_loss(val_history_reg01["loss"], "Validation Loss")
    utils.plot_loss(train_history_reg02["loss"],
                    "Training Loss L = 0.2", npoints_to_average=10)
    utils.plot_loss(val_history_reg02["loss"], "Validation Loss")
    utils.plot_loss(train_history_reg03["loss"],
                    "Training Loss L = 0.02", npoints_to_average=10)
    utils.plot_loss(val_history_reg03["loss"], "Validation Loss")
    utils.plot_loss(train_history_reg04["loss"],
                    "Training Loss L = 0.002", npoints_to_average=10)
    utils.plot_loss(val_history_reg04["loss"], "Validation Loss")
    plt.legend()
    plt.xlabel("Number of Training Steps")
    plt.ylabel("Cross Entropy Loss - Average")
    plt.savefig("task4c_l2_reg_norms.png")
    plt.show()

    # Plot accuracy
    plt.ylim([0.89, .93])
    utils.plot_loss(train_history_reg01["accuracy"], "Training Accuracy L = 2.0")
    utils.plot_loss(val_history_reg01["accuracy"], "Validation Accuracy L = 2.0")
    utils.plot_loss(train_history_reg02["accuracy"], "Training Accuracy L = 0.2")
    utils.plot_loss(val_history_reg02["accuracy"], "Validation Accuracy L = 0.2")
    utils.plot_loss(train_history_reg03["accuracy"], "Training Accuracy L = 0.02")
    utils.plot_loss(val_history_reg03["accuracy"], "Validation Accuracy L = 0.02")
    utils.plot_loss(train_history_reg04["accuracy"], "Training Accuracy L = 0.002")
    utils.plot_loss(val_history_reg04["accuracy"], "Validation Accuracy L = 0.002")
    plt.legend()
    plt.xlabel("Number of Training Steps")
    plt.ylabel("Accuracy")
    # This fig did not get saved correctly, but you can find it in the report at task 4c, graph number 2.
    plt.savefig("task4c_l2_reg_accuracy.png")
    plt.show()

    # Plotting of softmax weights (Task 4b)
    weights = trainer.model.w[:-1].T
    # Print weights of each digit
    fig = plt.figure(figsize=(10, 2))
    for digit in range(1, 10):
        plt.title(f"Digit: {digit}")

        # Reshape to 28x28
        img = np.reshape(weights[digit], (28, 28))
        fig.add_subplot(2, 10, digit)
        plt.imshow(img, cmap="gray")
    plt.savefig("task4b_l2_weights_no_lambda.png")
    plt.show()

    weights2 = trainer2.model.w[:-1].T
    # Print weights of each digit
    fig2 = plt.figure(figsize=(10, 2))
    for digit in range(1, 10):
        plt.title(f"Digit: {digit}")

        # Reshape to 28x28
        img = np.reshape(weights2[digit], (28, 28))
        fig2.add_subplot(2, 10, digit)
        plt.imshow(img, cmap="gray")
    plt.savefig("task4b_l2_weights_with_lambda.png")
    plt.show()

    plt.savefig("task4c_l2_reg_accuracy.png")

    # Plotting of accuracy for difference values of lambdas (task 4c)
    l2_lambdas = [2, .2, .02, .002]

    # Task 4e
