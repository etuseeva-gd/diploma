from myutils import read_train_sets
import tensorflow as tf
import time
import config
from datetime import timedelta
import math
import random
import numpy as np
import os
import cnn
from numpy.random import seed
from tensorflow import set_random_seed

seed(1)
set_random_seed(2)


def train(num_classes, data):
    # МОДЕЛЬ
    # ----------
    # Создаем session (сессию)
    session = tf.Session()

    # Задаем вход НС
    x = tf.placeholder(tf.float32,
                       shape=[None, config.image_height,
                              config.image_width, config.num_channels],
                       name='x')

    # Опеределяем выход НС
    y = tf.placeholder(tf.float32,
                       shape=[None, num_classes],
                       name='y')

    # Определяем сверточную НС
    # и получаем последний слой сети
    layer_params = [
        {
            'filter_size': 3,
            'num_filters': 32
        },
        {
            'filter_size': 3,
            'num_filters': 32
        },
        {
            'filter_size': 3,
            'num_filters': 64
        }
    ]
    y_pred, final_layer = cnn.create_cnn(
        input=x,
        num_channels=config.num_channels,
        num_classes=num_classes,
        layer_params=layer_params,
        image_size=config.image_size
    )

    # session.run(tf.global_variables_initializer())

    # ОБУЧЕНИЕ
    # ----------
    # -----------------------
    # Получаем cross entropy (перекрестную энропию)
    # Необходима для того, чтобы при обучении охаратеризовать насколько система
    # была права или нет при классификации того или иного обьекта
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(
        logits=final_layer,
        labels=y
    )
    # Разность между полученным и ожидаемым значениями
    cost = tf.reduce_mean(cross_entropy)
    # Оптимизатор
    optimizer = tf.train.AdamOptimizer(
        learning_rate=config.learning_rate
    ).minimize(cost)
    # -----------------------

    # Точность операции
    # -----------------------
    # Здесь вы проверяете, равен ли индекс максимального значения прогнозируемого
    # изображения фактическому помеченному изображению. Оба будут вектор-столбцом.
    correct_prediction = tf.equal(
        tf.argmax(y_pred, dimension=1),
        tf.argmax(y, dimension=1)
    )
    # Вычислить точность по всем заданным изображениям и усреднить их
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
    # -----------------------

    session.run(tf.global_variables_initializer())

    # Определяем saver. Необходим нам для того, чтобы мы в дальнейшем смогли восстановить нашу модель.
    saver = tf.train.Saver(save_relative_paths=True)

    for i in range(config.num_iteration):
        x_batch, y_batch, _, _ = data.train.next_batch(
            config.batch_size
        )
        feed_dict_train = {x: x_batch, y: y_batch}
        session.run(optimizer, feed_dict=feed_dict_train)

        num_batch = int(data.train.num_examples/config.batch_size)
        if i % num_batch == 0:
            # Номер эпохи
            epoch = int(i / num_batch)

            train_accuracy = session.run(accuracy, feed_dict=feed_dict_train)

            x_test_batch, y_test_batch, _, _ = data.test.next_batch(
                config.batch_size
            )
            feed_dict_test = {x: x_test_batch, y: y_test_batch}
            test_accuracy, test_loss = session.run(
                [accuracy, cost],
                feed_dict=feed_dict_test
            )

            print("Эпоха {0}: Точность обучения = {1:>6.1%}, Точность проверки = {2:>6.1%}, Потеря = {3:.3f}"
                  .format(epoch + 1, train_accuracy, test_accuracy, test_loss))

            # Сохраняем можель после каждой эпохи
            saver.save(session, config.model_dir + config.model_name)


def console_train():
    # ВХОДНЫЕ ДАННЫЕ
    # ----------
    # Подготавливаем входные данные
    # Классы и их количество, которые хотим в дальнейшмем будем распознавать (пример: 'Цветок', 'Машина')
    classes = os.listdir(config.train_path)
    num_classes = len(classes)

    # Подгружаем входные данные для тренировки сети
    data = read_train_sets(
        config.train_path,
        config.image_size,
        classes,
        test_size=config.test_size
    )

    print("Тренировочные данные: {}".format(len(data.train.labels)))
    print("Проверочные данные: {}".format(len(data.test.labels)))

    train(num_classes, data)


if __name__ == '__main__':
    console_train()
