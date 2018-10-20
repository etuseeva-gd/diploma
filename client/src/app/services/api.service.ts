import {Injectable} from '@angular/core';
import {TransportService} from './transport.service';
import {BaseParams, PredictParams, TrainParams} from '../models/params';

@Injectable()
export class ApiService {
  constructor(private transportService: TransportService) {
  }

  saveSettings(settings: BaseParams) {
    const body = JSON.stringify({});
    return this.transportService.post('/save_settings', body);
  }

  train(settings: TrainParams) {
    const body = JSON.stringify({});
    return this.transportService.post('/train', body);
  }

  predict(param: PredictParams) {
    const body = JSON.stringify({
      url: param.url
    });
    return this.transportService.post('/predict', body);
  }

}
