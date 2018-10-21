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
  private trainParams: ITrainParams;
  private nnParams: INNParams;

  constructor(private trainService: TrainService) {
  }

  ngOnInit() {
    this.trainService.getTrainParams().subscribe(params => this.trainParams = params);
    this.trainService.getNNParams().subscribe(params => this.nnParams = params);
  }

  train() {
    this.trainService.train(this.trainParams, this.nnParams);
  }

}
