import os

# Расположение параметров - базовых, тренировочных, сети
# absolute_path = 'C:/Users/lenok/Desktop/diploma/recognizer/'
absolute_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
absolute_path = absolute_path.replace("\\", "/") 

base_params_path = absolute_path + '/params/base.json'
train_params_path = absolute_path + '/params/train.json'
nn_params_path = absolute_path + '/params/nn.json'

# Параметры, о расположенни тренировочных данных
train_path = absolute_path + '/training_data'
test_path = absolute_path + '/testing_data'

# Параметры с расположением модели
model_dir = absolute_path + '/model/'
model_name = 'model'

# Файл с репортом
report_path = absolute_path + '/report.txt'

# Флаг, который говорит о том, что обучение закочилось
end_flag = 'END'
