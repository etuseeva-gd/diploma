import tensorflow as tf
import numpy as np
import os
import glob
import cv2
import sys


from utility.image import prepare_image_for_predict, get_image_by_path, get_image_by_url
from utility.constants import model_dir, model_name, train_path
from models.params import Params
from utility.file import read, write_a, write_w
from utility.jsonfile import read_json


def is_model_exists():
    return os.path.isfile(model_dir + model_name + '.meta')


def predict(image):
    if not is_model_exists():
        raise Exception('В начале обучите данные! Модель не найдена!')

    # Инициализируем наши параметры
    params = Params()

    # ПОДГОТОВКА ВХОДНЫХ ДАННЫХ
    # ----------
    # Считываем изображение, которое необходимо распознать
    # Ввиду того, что вход НС имеет вид [None, image_height, image_width, num_channels]
    # мы преобразуем наши данные к нужной форме
    images = prepare_image_for_predict(image, params.base_params.image_size)
    x_batch = images.reshape(
        1,
        params.base_params.image_height,
        params.base_params.image_width,
        params.base_params.num_channels
    )

    # ВОССТАНОВЛЕНИЕ МОДЕЛИ
    # ----------
    session = tf.Session()

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
    classes = next(os.walk(train_path))[1]

    y_test_images = np.zeros((1, len(classes)))

    name_of_classes = read_json(train_path + '/classes.json')

    # ПРЕДСКАЗАНИЕ
    # ----------
    feed_dict_test = {x: x_batch, y: y_test_images}
    result = session.run(y_pred, feed_dict=feed_dict_test)

    # Возвращаем какой класс и какая вертоятность что это он
    cls_id = classes[np.argmax(result)]
    return name_of_classes[cls_id] + ' (' + cls_id + ')', np.amax(result) * 100


def predict_wrapper(path, is_result_to_file, result_path):
    # Получаем текущее изображение
    image = get_image_by_path(path)

    cls, probability = predict(image)

    result = u'{0} -> {1} ({2:.3f}%)'.format(path, cls, probability)
    print(result)

    if is_result_to_file:
        write_a(result_path, result + '\n')


def console_prediction():
    result_path = 'result.txt'

    # Куда выводить результат - в консоль или файл
    is_result_to_file = sys.argv[1] == '-f'

    #  Получаем данные о местоположении файла
    path = sys.argv[2]
    if not os.path.exists(path):
        raise Exception('Переданный путь отсутствует - '  + path)

    write_w(result_path, '')  # очищаем файл с результатом, если он есть
    if os.path.isdir(path):
        # Получаем данные по списку изображений
        files = os.listdir(path)
        for file in files:
            predict_wrapper(path + file, is_result_to_file, result_path)
    else:
        predict_wrapper(path, is_result_to_file, result_path)


def web_prediction(url):
    try:
         # Выкачиваем текущее изображение из интернета
        image = get_image_by_url(url)
        return predict(image)
    except Exception as error:
        print('Поймана ошибка: ' + repr(error))


if __name__ == '__main__':
    try:
        console_prediction()
    except IndexError as error:
        print('Поймана ошибка: ' + repr(error))
        print('Проверьте коректность входных аргументов')
    except Exception as error:
        print('Поймана ошибка: ' + repr(error))

    # path = 'C:/Users/lenok/Desktop/diploma/recognizer/training_data/dogs/'
    # files = os.listdir(path)
    # for file in files:
    #     # print(path + file)
    #     image = get_image_by_path(path + file)
    #     cls, probability = loc_predict(image)
    #     print('Это {0} на {1}%'.format(cls, probability))
