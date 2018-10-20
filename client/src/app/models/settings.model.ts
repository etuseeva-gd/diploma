export class BaseSettings {
  imageSize: number; // 128
  numChannels: number; // 3

  trainingPath: string; // 'training_data'
  testingPath: string; // 'testing_data'

  modelDir: string; // 'model/'
  modelName: string; // 'model'

  // Ссылка на архив (или что то такое)
  url: string;

  constructor() {
    this.imageSize = 128;
    this.numChannels = 3;

    this.trainingPath = 'training_data';
    this.testingPath = 'testing_data';

    this.modelDir = 'model/';
    this.modelName = 'model';

    // this.url = '';
  }
}

export class TrainSettings {
  learningRate: number | string; // '1e-4'
  numIteration: number; // 1000

  batchSize: number; // 32 or 10

  constructor() {
    this.learningRate = '1e-4';
    this.numIteration = 1000;
    this.batchSize = 10;
  }
}

export class NetworkSettings {
  // Количество conv слоев
  numConvLayers: number;
  convLayersParams: ConvLayerSettings[];

  // Количество flat слоев
  numFlatLayers: number;
  flatLayerParams: LayerSettings[];

  // Количество fc слоев
  numFCLayers: number;
  fcLayerParams: FCLayerSettings[];

  constructor() {
    this.numConvLayers = 3;
    this.convLayersParams = [
      new ConvLayerSettings(3, 32),
      new ConvLayerSettings(3, 32),
      new ConvLayerSettings(3, 64)
    ];

    // Количество flat слоев
    this.numFlatLayers = 1;
    this.flatLayerParams = [];

    // Количество fc слоев
    this.numFCLayers = 2;
    this.fcLayerParams = [
      new FCLayerSettings(128)
    ];
  }
}

/**
 * Настройки для абстрактного слоя.
 */
export class LayerSettings {
}

export class ConvLayerSettings extends LayerSettings {
  filterSize: number;
  numFilters: number;

  constructor(filterSize, numFilters) {
    super();

    this.filterSize = filterSize || null;
    this.numFilters = numFilters || null;
  }
}

export class FCLayerSettings extends LayerSettings {
  size: number;

  constructor(size) {
    super();

    this.size = size || null;
  }
}


