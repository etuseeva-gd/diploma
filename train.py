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

# ВХОДНЫЕ ДАННЫЕ
# ----------

# Подготавливаем входные данные
print('Подготовка входных данных')

classes = os.listdir(config.train_path)
num_classes = len(classes)

print('Начинаем загрузку входных данных')

# Подгружаем входные данные для тренировки сети
data = dataset.read_train_sets(
    config.train_path, config.image_size, classes, validation_size=config.validation_size)

print("Завершили считывание входнных данных")
print("Количество тренировочных данных:\t\t{}".format(len(data.train.labels)))
print("Количество проверочных данных:\t{}".format(len(data.valid.labels)))

# МОДЕЛЬ
# ----------
print('Определение модели (нейронной сети)')

# Создаем session (сессию)
session = tf.Session()

x = tf.placeholder(tf.float32,
                   shape=[None, config.image_size, config.image_size, config.num_channels],
                   name='x')

y_true = tf.placeholder(tf.float32, shape=[None, num_classes], name='y_true')
y_true_cls = tf.argmax(y_true, dimension=1)

# Получаем последний слой сети
y_pred, final_layer = cnn.create_cnn(input=x,
                                     num_channels=config.num_channels,
                                     num_classes=num_classes)
y_pred_cls = tf.argmax(y_pred, dimension=1)

session.run(tf.global_variables_initializer())

# ОБУЧЕНИЕ
# ----------
print('Подговка перед обучением')

# Получаем cross entropy (перекрестную энропию)
# Необходима для того, чтобы при обучении охаратеризовать насколько система
# была права или нет при классификации того или иного обьекта
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=final_layer,
                                                        labels=y_true)
# Разность между полученным и ожидаемым значениями
cost = tf.reduce_mean(cross_entropy)

# Оптимизатор
optimizer = tf.train.AdamOptimizer(learning_rate=config.learning_rate).minimize(cost)

# Точность операции
correct_prediction = tf.equal(y_pred_cls, y_true_cls)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

session.run(tf.global_variables_initializer())

# Определяем saver. Необходим нам для того, чтобы мы в дальнейшем смогли восстановить нашу модель.
saver = tf.train.Saver(save_relative_paths=True)


def show_progress(epoch, feed_dict_train, feed_dict_validate, val_loss):
    """
        Вывести прогресс обучения.

        @param epoch - эпоха
        @param feed_dict_train
        @param feed_dict_validate
        @param val_loss
    """

    acc = session.run(accuracy, feed_dict=feed_dict_train)
    val_acc = session.run(accuracy, feed_dict=feed_dict_validate)
    msg = "Эпоха {0} --- Точность обучения: {1:>6.1%}, Точность проверки: {2:>6.1%},  Потеря: {3:.3f}"
    print(msg.format(epoch + 1, acc, val_acc, val_loss))


def train(num_iteration):
    total_iterations = 0

    for i in range(total_iterations,
                   total_iterations + num_iteration):
        x_batch, y_true_batch, _, cls_batch = data.train.next_batch(config.batch_size)
        feed_dict_tr = {x: x_batch,
                        y_true: y_true_batch}

        session.run(optimizer, feed_dict=feed_dict_tr)

        if i % int(data.train.num_examples / config.batch_size) == 0:
            x_valid_batch, y_valid_batch, _, valid_cls_batch = data.valid.next_batch(
                config.batch_size)
            feed_dict_val = {x: x_valid_batch,
                             y_true: y_valid_batch}

            val_loss = session.run(cost, feed_dict=feed_dict_val)
            epoch = int(i / int(data.train.num_examples / config.batch_size))

            show_progress(epoch, feed_dict_tr, feed_dict_val, val_loss)

            # Запоминаем полученную модель
            saver.save(session, config.model_dir + config.model_name)

    total_iterations += num_iteration


print('Начали обучение')

train(num_iteration=config.num_iteration)

print('Обучение завершено')
print('Конец')
