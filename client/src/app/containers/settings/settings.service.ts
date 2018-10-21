import {Injectable} from '@angular/core';
import {ApiService} from '../../services/api.service';
import {IBaseParams} from '../../models/base-params.model';

@Injectable()
export class SettingsService {
  constructor(private apiService: ApiService) {
  }

  getBaseParams() {
    return this.apiService.getBaseParams();
  }

  saveBaseParams(params: IBaseParams) {
    return this.apiService.saveBaseParams(JSON.stringify(params));
  }
}
