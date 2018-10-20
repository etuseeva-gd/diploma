import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  private menu = [
    {
      icon: 'settings',
      name: 'Настройки',
      urls: ['/settings']
    },
    {
      icon: 'fitness_center',
      name: 'Тренировать',
      urls: ['/train']
    },
    {
      icon: 'help',
      name: 'Распознать',
      urls: ['/predict']
    }
  ];

  ngOnInit(): void {

  }
}
