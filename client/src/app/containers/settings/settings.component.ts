import {Component, OnInit} from '@angular/core';
import {SettingsService} from './settings.service';
import {IBaseParams} from '../../models/base-params.model';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {
  /**
   * Тут хранятся базовые параметры системы.
   */
    // private params: IBaseParams;
  private params: IBaseParams = {
    train_path: 'train_path',
    test_path: 'test_path',
    model_dir: 'model_dir',
    model_name: 'model_name',
    image_size: 128,
    image_height: 128,
    image_width: 128,
    num_channels: 3
  };

  private paramsArr: [];

  constructor(private settingsService: SettingsService) {
  }

  ngOnInit() {
    this.settingsService
      .getBaseParams()
      .subscribe(params => this.params = params);
  }

  saveParams() {
    this.settingsService.saveBaseParams(this.params);
  }

}
