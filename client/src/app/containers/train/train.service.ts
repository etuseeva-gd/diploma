import {Injectable} from '@angular/core';
import {ApiService} from '../../services/api.service';
import {ITrainParams} from '../../models/train-params.model';
import {INNParams} from '../../models/nn-params.model';
import {timer} from 'rxjs';
import {switchMap} from 'rxjs/operators';

@Injectable()
export class TrainService {
  constructor(private apiService: ApiService) {
  }

  getTrainParams() {
    return this.apiService.getTrainParams();
  }

  getNNParams() {
    return this.apiService.getNNParams();
  }

  train(trainParams: ITrainParams, nnParams: INNParams) {
    const body = JSON.stringify({
      train_params: trainParams,
      nn_params: nnParams
    });
    return this.apiService.train(body);
  }

  getReport() {
    return timer(1, 3 * 1000)
      .pipe(
        switchMap(() => this.apiService.getReport())
      );
  }
}
