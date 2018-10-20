import {Component, OnInit} from '@angular/core';
import {ApiService} from '../../services/api.service';
import {TrainParams} from '../../models/params';

@Component({
  selector: 'app-train',
  templateUrl: './train.component.html',
  styleUrls: ['./train.component.scss']
})
export class TrainComponent implements OnInit {
  private params: TrainParams;

  constructor(private apiService: ApiService) {
  }

  ngOnInit() {
    this.params = new TrainParams();
  }

  train() {
    this.apiService.train(this.params);
  }

}
