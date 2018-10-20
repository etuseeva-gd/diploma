import {Component, OnInit} from '@angular/core';
import {BaseSettings} from '../../models/settings.model';
import {ApiService} from '../../services/api.service';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss']
})
export class SettingsComponent implements OnInit {
  /**
   * Тут хранятся базовые параметры системы.
   */
  private settings: BaseSettings;

  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
    this.settings = new BaseSettings();
  }

  saveSettings() {
    this.apiService.saveSettings(this.settings);
  }

}
