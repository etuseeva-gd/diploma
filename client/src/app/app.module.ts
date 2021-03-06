import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

// Графика
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './modules/material.module';

import { AppComponent } from './app.component';

// Используемые сервисы
import { ApiService } from './services/api.service';
import { TransportService } from './services/transport.service';
import {PredictService} from './containers/predict/predict.service';
import {SettingsService} from './containers/settings/settings.service';
import {TrainService} from './containers/train/train.service';

// Обьявленные компоненты
import { SettingsComponent } from './containers/settings/settings.component';
import { TrainComponent } from './containers/train/train.component';
import { PredictComponent } from './containers/predict/predict.component';
import { SpinnerComponent } from "./components/spinner/spinner.component";
import { ChartComponent } from "./components/chart/chart.component";

// Роутинг
import { routing } from './app.routing';

import { NgxChartsModule } from '@swimlane/ngx-charts';

@NgModule({
  declarations: [
    AppComponent,
    SettingsComponent,
    TrainComponent,
    PredictComponent,
    SpinnerComponent,
    ChartComponent
  ],
  imports: [
    BrowserModule,
    routing,
    FormsModule,
    HttpClientModule,
    MaterialModule,
    BrowserAnimationsModule,
    NgxChartsModule
  ],
  providers: [
    ApiService,
    TransportService,
    PredictService,
    SettingsService,
    TrainService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
