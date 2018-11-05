import numpy as np
import tensorflow as tf


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
               num_classes,
               nn_params,
               image_size):
    # @todo подумать о image_size

    # Conv + pool слои
    # conv/pool 1
    layer = create_convolutional_layer(
        input=input,
        num_input_channels=num_channels,
        conv_filter_size=nn_params.get_filter_size(0),
        num_filters=nn_params.get_num_filters(0)
    )
    layer = create_max_pooling_layer(layer)

    # conv/pool 2 - n
    for i in range(1, len(nn_params.layer_params)):
        layer = create_convolutional_layer(
            input=layer,
            num_input_channels=nn_params.get_num_filters(i - 1),
            conv_filter_size=nn_params.get_filter_size(i),
            num_filters=nn_params.get_num_filters(i)
        )
        layer = create_max_pooling_layer(layer)

    # Fully Connected слои (одинаковые для всех)
    layer = reshape_layer(layer)

    # fc 1
    layer = create_fc_layer(
        input=layer,
        num_inputs=layer.get_shape()[1:4].num_elements(),
        num_outputs=image_size,
        use_relu=True
    )

    # fc 2
    layer = create_fc_layer(
        input=layer,
        num_inputs=image_size,
        num_outputs=num_classes,
        use_relu=False
    )

    y = tf.nn.softmax(layer, name="y_pred")
    return y, layer
