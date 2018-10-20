import {RouterModule} from '@angular/router';
import {ModuleWithProviders} from '@angular/core';
import {PredictComponent} from './containers/predict/predict.component';
import {TrainComponent} from './containers/train/train.component';
import {SettingsComponent} from './containers/settings/settings.component';

export const routing: ModuleWithProviders = RouterModule.forRoot([
  {
    path: '',
    pathMatch: 'full',
    redirectTo: '/predict'
  },
  {
    path: 'predict',
    pathMatch: 'full',
    component: PredictComponent
  },
  {
    path: 'train',
    pathMatch: 'full',
    component: TrainComponent
  },
  {
    path: 'settings',
    pathMatch: 'full',
    component: SettingsComponent
  },
  {
    path: '**',
    redirectTo: ''
  }
]);
