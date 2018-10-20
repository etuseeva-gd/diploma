import {Component, OnInit} from '@angular/core';
import {ApiService} from '../../services/api.service';
import {BaseParams} from '../../models/params';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {
  /**
   * Тут хранятся базовые параметры системы.
   */
  private params: BaseParams;

  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
    this.params = new BaseParams();
  }

  saveSettings() {
    this.apiService.saveSettings(this.params);
  }

}
