import dataset
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

total_iterations = 0


def init():
    # ВХОДНЫЕ ДАННЫЕ
    # ----------
    # Подготавливаем входные данные
    # Классы и их количество, которые хотим в дальнейшмем будем распознавать (пример: 'Цветок', 'Машина')
    classes = os.listdir(config.train_path)
    num_classes = len(classes)

    # Подгружаем входные данные для тренировки сети
    data = dataset.read_train_sets(
        config.train_path,
        config.image_size,
        classes,
        validation_size=config.validation_size
    )

    print("Завершили считывание входнных данных")
    print("Количество тренировочных данных:\t\t{}".format(len(data.train.labels)))
    print("Количество проверочных данных:\t{}".format(len(data.valid.labels)))

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
    y_pred, final_layer = cnn.create_cnn(input=x,
                                         num_channels=config.num_channels,
                                         num_classes=num_classes)

    # session.run(tf.global_variables_initializer())

    # ОБУЧЕНИЕ
    # ----------
    # -----------------------
    # Получаем cross entropy (перекрестную энропию)
    # Необходима для того, чтобы при обучении охаратеризовать насколько система
    # была права или нет при классификации того или иного обьекта
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=final_layer,
                                                            labels=y)
    # Разность между полученным и ожидаемым значениями
    cost = tf.reduce_mean(cross_entropy)
    # Оптимизатор
    optimizer = tf.train.AdamOptimizer(
        learning_rate=config.learning_rate).minimize(cost)
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

    global total_iterations
    for i in range(total_iterations, total_iterations + config.num_iteration):
        x_batch, y_batch, _, _ = data.train.next_batch(
            config.batch_size)
        feed_dict_tr = {x: x_batch, y: y_batch}

        session.run(optimizer, feed_dict=feed_dict_tr)

        
        if i % int(data.train.num_examples/config.batch_size) == 0:
            x_valid_batch, y_valid_batch, _, _ = data.valid.next_batch(
                config.batch_size)
            feed_dict_val = {x: x_valid_batch, y: y_valid_batch}

            val_loss = session.run(cost, feed_dict=feed_dict_val)
            epoch = int(i / int(data.train.num_examples/config.batch_size))

            acc = session.run(accuracy, feed_dict=feed_dict_tr)
            val_acc = session.run(accuracy, feed_dict=feed_dict_val)
            msg = "Training Epoch {0} --- Training Accuracy: {1:>6.1%}, Validation Accuracy: {2:>6.1%},  Validation Loss: {3:.3f}"
            print(msg.format(epoch + 1, acc, val_acc, val_loss))

            saver.save(session, config.model_dir + config.model_name)
    total_iterations += config.num_iteration


if __name__ == '__main__':
    init()
