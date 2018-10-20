import {Component, OnInit} from '@angular/core';
import {TrainSettings} from '../../models/settings.model';
import {ApiService} from '../../services/api.service';

@Component({
  selector: 'app-train',
  templateUrl: './train.component.html',
  styleUrls: ['./train.component.scss']
})
export class TrainComponent implements OnInit {
  private settings: TrainSettings;

  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
    this.settings = new TrainSettings();
  }

  train() {
    this.apiService.train(this.settings);
  }

}
