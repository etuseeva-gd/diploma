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

// Обьявленные компоненты
import { SettingsComponent } from './containers/settings/settings.component';
import { TrainComponent } from './containers/train/train.component';
import { PredictComponent } from './containers/predict/predict.component';

// Роутинг
import { routing } from './app.routing';

@NgModule({
  declarations: [
    AppComponent,
    SettingsComponent,
    TrainComponent,
    PredictComponent
  ],
  imports: [
    BrowserModule,
    routing,
    FormsModule,
    HttpClientModule,
    MaterialModule,
    BrowserAnimationsModule
  ],
  providers: [
    ApiService,
    TransportService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
