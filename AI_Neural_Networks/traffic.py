import cv2
import numpy as np
from numpy import expand_dims
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data()

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    im = cv2.imread(r'C:\Users\AliDo\PycharmProjects\AI_Neural_Networks\gtsrb\42\00000_00000.ppm')
    a = cv2.resize(im, (IMG_WIDTH, IMG_HEIGHT))
    a = a/255.0
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )
    x_train = x_train / 255.0

    x_test = x_test / 255.0

    # Get a compiled neural network
    model = get_model()

    model.summary()
    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)
    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    L = np.expand_dims(a, axis=0)
    predictions = model.predict(L)
    print(predictions[0])
    print(np.argmax(predictions[0]))

    # Save model to file
    #model.save(r'C:\Users\AliDo\PycharmProjects\AI_Neural_Networks\Save')
    '''if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")'''


def load_data():
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = []
    labels = []
    for i in range(NUM_CATEGORIES):
        for image_path in os.listdir('gtsrb' + os.sep + f'{i}'):
            url = 'gtsrb' + os.sep + f'{i}' + os.sep + image_path
            im = cv2.imread(url)
            new_image = cv2.resize(im, (IMG_WIDTH, IMG_HEIGHT))
            images.append(new_image)
            labels.append(i)
    return((images,labels))


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = tf.keras.models.Sequential([
        #Convolutional Layer
        tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),

        #Max-pooling layer, 2*2 poolsize

        tf.keras.layers.MaxPooling2D(pool_size=(2,2)),

        # another time

        tf.keras.layers.Conv2D(32, (3, 3), activation=None, input_shape=(14, 14, 32)),
        tf.keras.layers.MaxPooling2D(pool_size=(3, 3)),




        # Flatten units

        tf.keras.layers.Flatten(),

        #Add hidden layer with dropout
        #tf.keras.layers.Dense(8, activation="relu"),
        tf.keras.layers.Dense(128, activation="sigmoid"),
        #tf.keras.layers.Dense(128, activation=None),

        tf.keras.layers.Dropout(0.4),

        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")


    ])

    model.compile(
        optimizer='adam',
        loss = 'categorical_crossentropy',
        metrics = ['accuracy']
    )

    return model
    raise NotImplementedError


if __name__ == "__main__":
    main()
