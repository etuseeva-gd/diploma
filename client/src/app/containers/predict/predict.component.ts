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

  public history: any[] = [];
  private isRecognized: boolean = false;

  constructor(private predictService: PredictService) {
  }

  ngOnInit() {
    this.params = {url: ''} as IPredict;
  }

  predict() {
    this.isRecognized = true;

    this.predictService
      .predict(this.params)
      .subscribe(result => {
        this.history.push({
          url: this.params.url,
          result
        });
        this.isRecognized = false;
        this.params.url = '';
      });
  }
}
