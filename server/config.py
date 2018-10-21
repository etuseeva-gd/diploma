train_path = 'training_data'
test_path = 'testing_data'

model_dir = 'model/'
model_name = 'model'

# Размер изображения
image_size = 128
image_height = 128
image_width = 128

# Количество канналов в изображении (green, blue, red)
# если изображение черно-белое, то = 1
num_channels = 3

# Параметры, от которых меняется скорость, качество и тд обучения
learning_rate = 1e-4
num_iteration = 1000 
batch_size = 10

validation_size = 0.2  # 20% данных будет также использовано для валидации