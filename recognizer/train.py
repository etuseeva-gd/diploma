import tensorflow as tf
import time
from datetime import timedelta
import math
import random
import numpy as np
import os
from numpy.random import seed
from tensorflow import set_random_seed
import sys

from models.params import Params

from utility.network import create_cnn
from utility.image import read_train_sets
from utility.constants import model_dir, model_name, train_path, report_path, end_flag
from utility.file import write_a, write_w

seed(1)
set_random_seed(2)


def train(num_classes, data, params):
    # МОДЕЛЬ
    # ----------
    # Создаем session (сессию)
    session = tf.Session()

    # Задаем вход НС
    x = tf.placeholder(tf.float32,
                       shape=[None, params.base_params.image_height,
                              params.base_params.image_width, params.base_params.num_channels],
                       name='x')

    # Опеределяем выход НС
    y = tf.placeholder(tf.float32,
                       shape=[None, num_classes],
                       name='y')

    # Определяем сверточную НС
    # и получаем последний слой сети
    y_pred, final_layer = create_cnn(
        input=x,
        num_channels=params.base_params.num_channels,
        num_classes=num_classes,
        nn_params=params.nn_params,
        image_size=params.base_params.image_size
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
        learning_rate=params.train_params.learning_rate
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

    write_w(report_path, '')
    num_batch = int(data.train.num_examples /
                    params.train_params.batch_size)

    # for i in range(params.train_params.num_iteration):
    for i in range(num_batch * 50):
        print(i)

        x_batch, y_batch, _, _ = data.train.next_batch(
            params.train_params.batch_size
        )
        feed_dict_train = {x: x_batch, y: y_batch}
        session.run(optimizer, feed_dict=feed_dict_train)

        if i % num_batch == 0:
            # Номер эпохи
            epoch = int(i / num_batch)

            train_accuracy, train_loss = session.run(
                [accuracy, cost],
                feed_dict=feed_dict_train
            )

            x_test_batch, y_test_batch, _, _ = data.test.next_batch(
                params.train_params.batch_size
            )
            feed_dict_test = {x: x_test_batch, y: y_test_batch}
            test_accuracy, test_loss = session.run(
                [accuracy, cost],
                feed_dict=feed_dict_test
            )

            print("Эпоха {0}: Точность обучения = {1:>6.1%}, Потеря обучения = {2:.3f}, Точность проверки = {3:>6.1%}, Потеря проверки = {4:.3f}"
                  .format(epoch + 1, train_accuracy, train_loss, test_accuracy, test_loss))

            # Сохраняем можель после каждой эпохи
            saver.save(session, model_dir + model_name)

            # Записываем все в файл, чтобы потом показать UI
            write_a(report_path, "{0} {1} {2} {3} {4}\n".format(
                epoch + 1, train_accuracy, train_loss, test_accuracy, test_loss))

    write_a(report_path, end_flag)


def console_train(path = train_path):
    # Инициализируем наши параметры
    params = Params()

    # ВХОДНЫЕ ДАННЫЕ
    # ----------
    # Подготавливаем входные данные
    # Классы и их количество, которые хотим в дальнейшмем будем распознавать (пример: 'Цветок', 'Машина')
    classes = next(os.walk(path))[1]
    num_classes = len(classes)

    # Подгружаем входные данные для тренировки сети
    data = read_train_sets(
        path,
        params.base_params.image_size,
        classes,
        test_size=0.2
    )

    print("Тренировочные данные: {}".format(len(data.train.labels)))
    print("Проверочные данные: {}".format(len(data.test.labels)))

    train(num_classes, data, params)


if __name__ == '__main__':
    try:
        #  Получаем данные о местоположении директории с обучающими данными
        path = train_path
        
        if len(sys.argv) > 1:
            path = sys.argv[1]

        if not os.path.exists(path):
            raise Exception('Директория содержащая обучающие данные отсутствует! ' + path)

        console_train(path)
    except IndexError as error:
        print('Поймана ошибка: ' + repr(error))
        print('Проверьте коректность входных аргументов')
    except Exception as error:
        print('Поймана ошибка: ' + repr(error))
    