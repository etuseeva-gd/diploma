import {Component, OnInit} from '@angular/core';
import {ITrainParams} from '../../models/train-params.model';
import {INNParams} from '../../models/nn-params.model';
import {TrainService} from './train.service';

@Component({
  selector: 'app-train',
  templateUrl: './train.component.html',
  styleUrls: ['./train.component.scss']
})
export class TrainComponent implements OnInit {
  // private trainParams: ITrainParams;
  private trainParams: ITrainParams = {
    learning_rate: "1e-3",
    num_iteration: 1000,
    batch_size: 32
  };

  // private nnParams: INNParams;
  private nnParams: INNParams = {
    layer_params: [
      {
        filter_size: 3,
        num_filters: 32},
      {
        filter_size: 3,
        num_filters: 32
      },
      {
        filter_size: 3,
        num_filters: 64
      }]
  };

  constructor(private trainService: TrainService) {
  }

  ngOnInit() {
    // this.trainService.getTrainParams().subscribe(params => this.trainParams = params);
    // this.trainService.getNNParams().subscribe(params => this.nnParams = params);
  }

  train() {
    this.trainService.train(this.trainParams, this.nnParams).subscribe();
  }

}
