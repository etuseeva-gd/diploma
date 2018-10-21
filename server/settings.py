from file import File

# Расположение параметров
base_params = 'params/base-params.txt'
train_params = 'params/train-params.txt'


class Settings:
    # Данный класс отвечает за параметры сети, где находятся тренировочные данные и тд.
    def __init__(self):
        lines = File.read(base_params)
        # todo спарсить данные и получить нужные классы


class ProgramConfig:
    def __init__(self,
                 train_path,
                 test_path,
                 model_dir,
                 model_name,
                 image_size,
                 num_channels):
        self._train_path = train_path
        self._test_path = test_path
        self._model_dir = model_dir
        self._model_name = model_name
        self._image_size = image_size
        self._num_channels = num_channels


class TrainConfig:
    def __init__(self,
                 learning_rate,
                 num_iteration,
                 validation_size,
                 batch_size):
        self._learning_rate = learning_rate
        self._num_iteration = num_iteration
        self._validation_size = validation_size
        self._batch_size = batch_size
