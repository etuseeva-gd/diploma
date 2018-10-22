from utility.jsonfile import read_json, write_json
from utility.constants import nn_params_path, base_params_path, train_params_path


class Params:
    # Данный класс отвечает за параметры сети, где находятся тренировочные данные и тд.
    def __init__(self):
        self.init_params()

    def init_params(self):
        self._base_params = BaseParams()
        self._train_params = TrainParams()
        self._nn_params = NNParams()

    @staticmethod
    def set_new_params(type, data):
        # Записываем в файл новые настройки

        path = ''
        if type == 'base':
            path = base_params_path
        elif type == 'train':
            path = train_params_path
        elif type == 'nn':
            path = nn_params_path
        write_json(path, data)

    @property
    def base_params(self):
        return self._base_params

    @property
    def train_params(self):
        return self._train_params

    @property
    def nn_params(self):
        return self._nn_params


class BaseParams:
    def __init__(self):
        # Сразу инициализируем класс теми значениями, которые
        # узнали из файлика с параметрами
        data = read_json(base_params_path)

        self._train_path = data['train_path']
        self._test_path = data['test_path']
        self._model_dir = data['model_dir']
        self._model_name = data['model_name']
        self._image_size = int(data['image_size'])
        self._image_height = int(data['image_height'])
        self._image_width = int(data['image_width'])

        # Количество канналов в изображении (green, blue, red)
        # если изображение черно-белое, то = 1
        self._num_channels = data['num_channels']

    @property
    def train_path(self):
        return self._train_path

    @property
    def test_path(self):
        return self._test_path

    @property
    def model_dir(self):
        return self._model_dir

    @property
    def model_name(self):
        return self._model_name

    @property
    def image_size(self):
        return self._image_size

    @property
    def image_height(self):
        return self._image_height

    @property
    def image_width(self):
        return self._image_width

    @property
    def num_channels(self):
        return self._num_channels


class TrainParams:
    def __init__(self):
        # Сразу инициализируем класс теми значениями, которые
        # узнали из файлика с параметрами
        data = read_json(train_params_path)
        self._learning_rate = float(data["learning_rate"])
        self._num_iteration = int(data["num_iteration"])
        self._batch_size = int(data["batch_size"])

    @property
    def learning_rate(self):
        return self._learning_rate

    @property
    def num_iteration(self):
        return self._num_iteration

    @property
    def batch_size(self):
        return self._batch_size


class NNParams:
    def __init__(self):
        # Сразу инициализируем класс теми значениями, которые
        # узнали из файлика с параметрами
        data = read_json(nn_params_path)
        self._layer_params = []
        for layer_params in data['layer_params']:
            self._layer_params.append({
                'filter_size': int(layer_params['filter_size']),
                'num_filters': int(layer_params['num_filters'])
            })

    @property
    def layer_params(self):
        return self._layer_params

    def get_filter_size(self, layer_index):
        return self._layer_params[layer_index]['filter_size']

    def get_num_filters(self, layer_index):
        return self._layer_params[layer_index]['num_filters']
