import {Injectable} from '@angular/core';
import {TransportService} from './transport.service';
import {map} from 'rxjs/operators';
import {IBaseParams} from '../models/base-params.model';
import {Observable} from 'rxjs/internal/Observable';
import {ITrainParams} from '../models/train-params.model';
import {INNParams} from '../models/nn-params.model';
import {IReport} from "../models/report.model";

@Injectable()
export class ApiService {
  constructor(private transportService: TransportService) {
  }

  // Для settigns service
  getBaseParams(): Observable<IBaseParams> {
    return this.transportService.get('/get_base_params')
      .pipe(
        map(data => data as IBaseParams)
      );
  }

  saveBaseParams(body) {
    return this.transportService.post('/save_base_params', body);
  }

  // Для train service
  getTrainParams(): Observable<ITrainParams> {
    return this.transportService.get('/get_train_params')
      .pipe(
        map(data => data as ITrainParams)
      );
  }

  getNNParams(): Observable<INNParams> {
    return this.transportService.get('/get_nn_params')
      .pipe(
        map(data => data as INNParams)
      );
  }

  train(body) {
    return this.transportService.post('/train', body);
  }

  getReport() {
    return this.transportService.get('/get_report')
      .pipe(
        map(data => data as IReport)
      );
  }

  // Для predict service
  predict(body) {
    return this.transportService.post('/predict', body);
  }
}
