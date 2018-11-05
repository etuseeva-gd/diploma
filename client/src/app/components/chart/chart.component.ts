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
      'rgb(122, 163, 229)',
      'rgb(168, 56, 93)',
      'rgb(162, 126, 168)',
      'rgb(170, 227, 245)'
    ]
  };

}
