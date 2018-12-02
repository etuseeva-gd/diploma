import { Component, OnInit, OnDestroy } from '@angular/core';
import { ITrainParams } from '../../models/train-params.model';
import { ILayerParams, INNParams } from '../../models/nn-params.model';
import { TrainService } from './train.service';
import { IReport } from "../../models/report.model";

@Component({
  selector: 'app-train',
  templateUrl: './train.component.html',
  styleUrls: ['./train.component.scss']
})
export class TrainComponent implements OnInit, OnDestroy {
  private _subs = [];

  private trainParams: ITrainParams;
  private nnParams: INNParams;

  private _reportId; // @todo rename
  private report: IReport;

  private accuracyResults: any = [];
  private lossResults: any = [];

  private isTrainEnded: boolean = false;

  private btnIsDisabled: boolean = false;

  constructor(private trainService: TrainService) {
  }

  ngOnInit() {
    const trainSub = this.trainService.getTrainParams().subscribe(params => this.trainParams = params);
    const nnSub = this.trainService.getNNParams().subscribe(params => this.nnParams = params);

    const id = this.trainService
      .getReport()
      .subscribe(report => {
        this.btnIsDisabled = !report.is_train_ended;

        if (!this.btnIsDisabled) {
          id.unsubscribe();
        }
      });

    this._subs = [trainSub, nnSub, id];
  }

  ngOnDestroy(): void {
    this._subs.forEach(s => s.unsubscribe());
  }

  train() {
    const trainSub = this.trainService
      .train(this.trainParams, this.nnParams)
      .subscribe(() => this.getReport());
    this._subs.push(trainSub);
  }

  getReport() {
    const id = this.trainService
      .getReport()
      .subscribe(report => {
        this.isTrainEnded = false;

        this.report = report;

        // @todo сделать модель для этого
        const results = [
          {
            name: 'Тренировочная точность',
            series: []
          },
          {
            name: 'Проверочная точность',
            series: []
          },
          {
            name: 'Тренировочная потеря',
            series: []
          },
          {
            name: 'Проверочная потеря',
            series: []
          }
        ];

        (report.statistics || []).forEach(statistic => {
          const epoch = statistic.epoch;

          // Accuracy
          const trainAcc = statistic.train_accuracy;
          results[0].series.push({
            name: epoch,
            value: trainAcc * 100
          });

          const testAcc = statistic.test_accuracy;
          results[1].series.push({
            name: epoch,
            value: testAcc * 100
          });

          // Loss
          const trainLoss = statistic.train_loss;
          results[2].series.push({
            name: epoch,
            value: trainLoss
          });

          const testLoss = statistic.test_loss;
          results[3].series.push({
            name: epoch,
            value: testLoss
          });
        });

        this.accuracyResults = [results[0], results[1]];
        this.lossResults = [results[2], results[3]];

        if (report.is_train_ended) {
          this.isTrainEnded = true;
          id.unsubscribe();
        }
      });

    this._subs.push(id);
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
