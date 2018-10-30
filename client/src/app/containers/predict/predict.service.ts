import {Injectable} from '@angular/core';
import {ApiService} from '../../services/api.service';
import {IPredict} from "../../models/predict.model";

@Injectable()
export class PredictService {
  constructor(private apiService: ApiService) {
  }

  predict(params: IPredict) {
    return this.apiService.predict(JSON.stringify(params));
  }

}
