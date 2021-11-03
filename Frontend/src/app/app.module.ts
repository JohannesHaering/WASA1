import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { MainpageComponent } from './mainpage/mainpage.component';
import { ModelviewpageComponent } from './modelviewpage/modelviewpage.component';
import { TrainingpageComponent } from './trainingpage/trainingpage.component';
import { ModeldescriptionComponent } from './modeldescription/modeldescription.component';
import { HttpClientModule } from '@angular/common/http';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { ErrorPopupComponent } from './error-popup/error-popup.component'
import { MatDialogModule } from '@angular/material/dialog';
import { DeletepopupComponent } from './deletepopup/deletepopup.component';

@NgModule({
  declarations: [
    AppComponent,
    MainpageComponent,
    ModelviewpageComponent,
    TrainingpageComponent,
    ModeldescriptionComponent,
    ErrorPopupComponent,
    DeletepopupComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    NoopAnimationsModule,
    MatDialogModule
  ],
  providers: [],
  bootstrap: [AppComponent],
  entryComponents: [
    ErrorPopupComponent
  ]
})
export class AppModule { }
