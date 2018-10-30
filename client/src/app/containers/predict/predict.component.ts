import {Component, OnInit} from '@angular/core';
import {IPredict} from "../../models/predict.model";
import {PredictService} from "./predict.service";

@Component({
  selector: 'app-predict',
  templateUrl: './predict.component.html',
  styleUrls: ['./predict.component.scss']
})
export class PredictComponent implements OnInit {
  private params: IPredict;

  constructor(private predictService: PredictService) {
  }

  ngOnInit() {
    this.params = {url: ''} as IPredict;
  }

  predict() {
    this.predictService
      .predict(this.params)
      .subscribe();
  }

}
