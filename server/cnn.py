import tensorflow as tf
import numpy as np


def create_weights(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))


def create_biases(size):
    return tf.Variable(tf.constant(0.05, shape=[size]))


def conv_layer(input, weights, biases, strides=1):
    # Обертка над внутренними tf функциями для создания conv слоя
    layer = tf.nn.conv2d(
        input=input,
        filter=weights,
        strides=[1, strides, strides, 1],
        padding='SAME'
    )
    layer = tf.nn.bias_add(layer, biases)
    return tf.nn.relu(layer)


def create_convolutional_layer(input,
                               num_input_channels,
                               conv_filter_size,
                               num_filters):
    # Создаем сверточный слой
    weights = create_weights(shape=[
        conv_filter_size,
        conv_filter_size,
        num_input_channels,
        num_filters
    ])
    biases = create_biases(num_filters)
    return conv_layer(input, weights, biases)


def create_max_pooling_layer(input, k=2):
    # Создаем слой подвыборки
    return tf.nn.max_pool(value=input, ksize=[1, k, k, 1], strides=[1, k, k, 1], padding='SAME')


def reshape_layer(layer):
    return tf.reshape(layer, [-1, layer.get_shape()[1:4].num_elements()])


def create_fc_layer(input,
                    num_inputs,
                    num_outputs,
                    use_relu=True):
    weights = create_weights(shape=[num_inputs, num_outputs])
    biases = create_biases(num_outputs)

    # Fully connected слой принимает на вход x и отдает w*x + b
    # Так как мы работает с матрицами, то используем специальную для этого фукнцию
    layer = tf.add(tf.matmul(input, weights), biases)

    # По необходимости используем relu
    if use_relu:
        layer = tf.nn.relu(layer)

    return layer


def create_cnn(input,
               num_channels,
               num_classes):
    # Первые сверточный, подвыборки слои
    filter_size_conv1 = 3
    num_filters_conv1 = 32

    first_conv_layer = create_convolutional_layer(
        input=input,
        num_input_channels=num_channels,
        conv_filter_size=filter_size_conv1,
        num_filters=num_filters_conv1
    )

    first_conv_layer = create_max_pooling_layer(first_conv_layer)

    # Второй
    filter_size_conv2 = 3
    num_filters_conv2 = 32

    second_conv_layer = create_convolutional_layer(
        input=first_conv_layer,
        num_input_channels=num_filters_conv1,
        conv_filter_size=filter_size_conv2,
        num_filters=num_filters_conv2
    )

    second_conv_layer = create_max_pooling_layer(second_conv_layer)

    # Третий
    filter_size_conv3 = 3
    num_filters_conv3 = 64

    third_conv_layer = create_convolutional_layer(
        input=second_conv_layer,
        num_input_channels=num_filters_conv2,
        conv_filter_size=filter_size_conv3,
        num_filters=num_filters_conv3
    )

    third_conv_layer = create_max_pooling_layer(third_conv_layer)

    # Fully Connected слой
    fc_layer_size = 128

    first_fc_layer = reshape_layer(third_conv_layer)

    first_fc_layer = create_fc_layer(
        input=first_fc_layer,
        num_inputs=first_fc_layer.get_shape()[
            1:4].num_elements(),
        num_outputs=fc_layer_size,
        use_relu=True
    )

    second_fc_layer = create_fc_layer(
        input=first_fc_layer,
        num_inputs=fc_layer_size,
        num_outputs=num_classes,
        use_relu=False
    )

    y = tf.nn.softmax(second_fc_layer, name="y_pred")
    return y, second_fc_layer
