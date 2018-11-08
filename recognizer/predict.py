import tensorflow as tf
import numpy as np
import os
import glob
import cv2
import sys


from utility.image import prepare_image, get_image_by_path, get_image_by_url
from utility.constants import model_dir, model_name, train_path
from models.params import Params


def is_model_exists():
    return os.path.isfile(model_dir + model_name + '.meta')


def predict(x_batch):
    session = tf.Session()

    # ВОССТАНОВЛЕНИЕ МОДЕЛИ
    # ----------
    # Загружаем/восстанавливаем сохраненную обученную модель
    saver = tf.train.import_meta_graph(
        model_dir + model_name + '.meta'
    )
    saver.restore(session, tf.train.latest_checkpoint(model_dir))

    graph = tf.get_default_graph()

    # Отвечает за предсказание сети
    y_pred = graph.get_tensor_by_name("y_pred:0")

    # Передаем данные сети на вход
    x = graph.get_tensor_by_name("x:0")
    y = graph.get_tensor_by_name("y:0")

    # Узнаем сколько/каких классов нужно нам распознать
    classes = os.listdir(train_path)

    y_test_images = np.zeros((1, len(classes)))

    # ПРЕДСКАЗАНИЕ
    # ----------
    feed_dict_test = {x: x_batch, y: y_test_images}
    result = session.run(y_pred, feed_dict=feed_dict_test)

    print(result)

    # Возвращаем какой класс и какая вертоятность что это он
    return classes[np.argmax(result)], np.amax(result) * 100


def loc_predict(image):
    # Инициализируем наши параметры
    params = Params()

    # ПОДГОТОВКА ВХОДНЫХ ДАННЫХ
    # ----------
    # Считываем изображение, которое необходимо распознать
    # Ввиду того, что вход НС имеет вид [None, image_height, image_width, num_channels]
    # мы преобразуем наши данные к нужной форме
    images = [prepare_image(image, params.base_params.image_size)]
    images = np.array(images, dtype=np.uint8)
    x_batch = images.reshape(
        1,
        params.base_params.image_height,
        params.base_params.image_width,
        params.base_params.num_channels
    )

    return predict(x_batch)


def console_prediction():
    # Получаем данные о местоположении файла
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_path = sys.argv[1]
    path = dir_path + '/' + image_path

    # Получаем текущее изображение
    image = get_image_by_path(path)

    cls, probability = loc_predict(image)
    print('Это {0} на {1}%'.format(cls, probability))


def web_prediction(url):
    # Выкачиваем текущее изображение из интернета
    image = get_image_by_url(url)
    return loc_predict(image)


if __name__ == '__main__':
    # console_prediction()

    path = 'C:/Users/lenok/Desktop/diploma/recognizer/testing_data/dogs/'
    files = os.listdir(path)
    for file in files:
        print(path + file)
        image = get_image_by_path(path + file)
        cls, probability = loc_predict(image)

        print('Это {0} на {1}%'.format(cls, probability))
