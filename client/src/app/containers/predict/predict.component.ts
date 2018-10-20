import {Component, OnInit} from '@angular/core';
import {PredictParam} from '../../models/predict-param.model';
import {ApiService} from '../../services/api.service';

@Component({
  selector: 'app-predict',
  templateUrl: './predict.component.html',
  styleUrls: ['./predict.component.scss']
})
export class PredictComponent implements OnInit {
  private param: PredictParam;

  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
    this.param = new PredictParam();
  }

  predict() {
    this.apiService.predict(this.param);
  }

}
