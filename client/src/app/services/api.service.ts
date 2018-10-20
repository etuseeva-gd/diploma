import {Injectable} from '@angular/core';
import {TransportService} from './transport.service';
import {BaseSettings, TrainSettings} from '../models/settings.model';
import {PredictParam} from '../models/predict-param.model';

@Injectable()
export class ApiService {

  constructor(private transportService: TransportService) {
  }

  saveSettings(settings: BaseSettings) {

  }

  train(settings: TrainSettings) {
    const body = JSON.stringify({});
    return this.transportService.post('/train', body);
  }

  predict(param: PredictParam) {
    const body = JSON.stringify({
      url: param.url
    });
    return this.transportService.post('/predict', body);
  }

}
