import tensorflow as tf
import numpy as np


def create_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))


def create_biases(size):
    return tf.Variable(tf.constant(0.05, shape=[size]))


def create_convolutional_layer(input,
                               num_input_channels,
                               conv_filter_size,
                               num_filters):
    """
    Создание convolutional (сверточного) слоя

    @param input
    @param num_input_channels
    @param conv_filter_size
    @param num_filters
    """

    weights = create_weights(shape=[
        conv_filter_size,
        conv_filter_size,
        num_input_channels,
        num_filters
    ])

    # Создаем сверточный слой, используя внутреннюю функцию tf
    layer = tf.nn.conv2d(input=input,
                         filter=weights,
                         strides=[1, 1, 1, 1],
                         padding='SAME')

    biases = create_biases(num_filters)

    layer += biases

    layer = tf.nn.max_pool(value=layer,
                           ksize=[1, 2, 2, 1],
                           strides=[1, 2, 2, 1],
                           padding='SAME')

    # Выход подаем в функцию активации relu (выпрямитель) - rectified linear unit
    layer = tf.nn.relu(layer)

    return layer


def create_flatten_layer(layer):
    """
    Создать flatten слой.

    @param layer
    """

    # Узнаем shape (форму) из предыдущего (то есть поданного нам на вход) слоя
    shape = layer.get_shape()

    num = shape[1:4].num_elements()

    # Данная функция позволит сделать сглаживание
    layer = tf.reshape(layer, [-1, num])

    return layer


def create_fc_layer(input,
                    num_inputs,
                    num_outputs,
                    use_relu=True):
    """
    Создать fully connected слой.

    @param input
    @param num_inputs
    @param num_outputs
    @param use_rely
    """

    weights = create_weights(shape=[num_inputs, num_outputs])
    biases = create_biases(num_outputs)

    # Fully connected слой принимает на вход x и отдает w*x + b
    # Так как мы работает с матрицами, то используем специальную для этого фукнцию
    layer = tf.matmul(input, weights) + biases

    # По необходимости используем relu
    if use_relu:
        layer = tf.nn.relu(layer)

    return layer


def create_cnn(input,
               num_channels,
               num_classes):
    """
    Создать cnn (сверточную нейронную сеть).

    @param input
    @param num_channels
    @param num_classes
    """
    # Подумать над тем, чтобы сделать сеть полностью конфигурируемой
    # Количество каждого вида слоев и параметров для них

    # Параметры сети (сделать входными данными)

    filter_size_conv1 = 3
    num_filters_conv1 = 32

    filter_size_conv2 = 3
    num_filters_conv2 = 32

    filter_size_conv3 = 3
    num_filters_conv3 = 64

    fc_layer_size = 128

    first_conv_layer = create_convolutional_layer(input=input,
                                                  num_input_channels=num_channels,
                                                  conv_filter_size=filter_size_conv1,
                                                  num_filters=num_filters_conv1)

    second_conv_layer = create_convolutional_layer(input=first_conv_layer,
                                                   num_input_channels=num_filters_conv1,
                                                   conv_filter_size=filter_size_conv2,
                                                   num_filters=num_filters_conv2)

    third_conv_layer = create_convolutional_layer(input=second_conv_layer,
                                                  num_input_channels=num_filters_conv2,
                                                  conv_filter_size=filter_size_conv3,
                                                  num_filters=num_filters_conv3)

    flat_layer = create_flatten_layer(third_conv_layer)

    first_fc_layer = create_fc_layer(input=flat_layer,
                                     num_inputs=flat_layer.get_shape()[
                                         1:4].num_elements(),
                                     num_outputs=fc_layer_size,
                                     use_relu=True)

    second_fc_layer = create_fc_layer(input=first_fc_layer,
                                      num_inputs=fc_layer_size,
                                      num_outputs=num_classes,
                                      use_relu=False)

    return {
        y: tf.nn.softmax(second_fc_layer, name='y'),
        final_layer: second_fc_layer
    }
