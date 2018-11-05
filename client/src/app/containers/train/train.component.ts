import {Component, OnInit} from '@angular/core';
import {ITrainParams} from '../../models/train-params.model';
import {ILayerParams, INNParams} from '../../models/nn-params.model';
import {TrainService} from './train.service';
import {IReport} from "../../models/report.model";

@Component({
  selector: 'app-train',
  templateUrl: './train.component.html',
  styleUrls: ['./train.component.scss']
})
export class TrainComponent implements OnInit {
  private trainParams: ITrainParams;
  private nnParams: INNParams;

  private report: IReport;

  constructor(private trainService: TrainService) {
  }

  ngOnInit() {
    this.trainService.getTrainParams().subscribe(params => this.trainParams = params);
    this.trainService.getNNParams().subscribe(params => this.nnParams = params);
  }

  train() {
    this.trainService
      .train(this.trainParams, this.nnParams)
      .subscribe();
  }

  getReport() {
    this.trainService
      .getReport()
      .subscribe(report => this.report = report);
  }

  addLayer() {
    const layer = {
      filter_size: 3,
      num_filters: 32
    } as ILayerParams;

    this.nnParams.layer_params.push(layer);
  }

  removeLayer(index) {
    if (this.nnParams.layer_params.length === 1) {
      return;
    }

    this.nnParams.layer_params.splice(index, 1);
  }

}
