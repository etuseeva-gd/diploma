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
    const width = params.image_width, height = params.image_height;
    params.image_size = width === height ? width : Math.max(width, height);
    return this.apiService.saveBaseParams(JSON.stringify(params));
  }
}
