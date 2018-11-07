import {Component, OnInit} from '@angular/core';
import {IPredict} from "../../models/predict.model";
import {PredictService} from "./predict.service";
import {IPredictResult} from "../../models/predict-result.model";

@Component({
  selector: 'app-predict',
  templateUrl: './predict.component.html',
  styleUrls: ['./predict.component.scss']
})
export class PredictComponent implements OnInit {
  private params: IPredict;

  private result: IPredictResult = null;
  private isRecognized: boolean = false;

  constructor(private predictService: PredictService) {
  }

  ngOnInit() {
    this.params = {url: ''} as IPredict;
  }

  predict() {
    this.clearResult();
    this.isRecognized = true;

    this.predictService
      .predict(this.params)
      .subscribe(result => {
        this.result = result;
        this.isRecognized = false;
      });
  }

  clearResult() {
    this.result = null;
  }
}
