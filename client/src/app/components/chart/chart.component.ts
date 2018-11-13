import {Component, Input} from '@angular/core';

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.scss']
})
export class ChartComponent {
  @Input()
  public results: any = [];

  @Input()
  xAxisLabel: string = '';

  @Input()
  yAxisLabel: string = '';

  view: number[] = [700, 400];

  showXAxis: boolean = true;
  showYAxis: boolean = true;

  gradient: boolean = false;

  showLegend: boolean = true;

  showXAxisLabel: boolean = true;
  showYAxisLabel: boolean = true;

  timeline: boolean = false;

  autoScale: boolean = true;

  // colors
  scheme: any = {
    domain: [
      '#ff4081',
      '#3f51b5'
    ]
  };

}
