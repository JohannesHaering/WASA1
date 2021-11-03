import { Component, OnInit } from '@angular/core';
import { BackendserviceService } from '../backendservice.service';
import { Modelstatistic } from '../modelstatistic';
import { BackendtrainingserviceService } from '../backendtrainingservice.service';
import {MatDialog, MatDialogConfig} from "@angular/material/dialog";
import { ErrorPopupComponent } from '../error-popup/error-popup.component';
import { DeletepopupComponent } from '../deletepopup/deletepopup.component';

@Component({
  selector: 'app-modelviewpage',
  templateUrl: './modelviewpage.component.html',
  styleUrls: ['./modelviewpage.component.css']
})
export class ModelviewpageComponent implements OnInit {

  availableModels:String[] = [];
  selectedModel:number = 0;
  selectedModelActive:boolean = true;
  selectedModelStatistic:Modelstatistic = {"hits": 100,"misses": 100};
  constructor(private backend:BackendserviceService, private trainingbackend:BackendtrainingserviceService, private dialog: MatDialog) { }

  ngOnInit(): void {
    this.reset()
  }

  getModels(){
    this.backend.getAvailableModels().subscribe(data => this.setModels(data), err => this.handleError(err));
  }

  setModels(data:String[]){
    this.availableModels = data;
    this.setSelectedModelStatistic();
  }

  changeSelectedModel(modelid:number){
    this.selectedModel = modelid;
    this.setSelectedModelStatistic();
  }

  setSelectedModelStatistic() {
    this.backend.getModelstatistics(this.availableModels[this.selectedModel]).subscribe(data => {this.selectedModelStatistic = data; }, err => this.handleError(err));
    this.updateModelActive();
  }

  updateModelActive() {
    this.backend.isActive(this.availableModels[this.selectedModel]).subscribe(data => {this.selectedModelActive = data}, err => this.handleError(err));
  }

  deploySelectedModel() {
    this.backend.setActive(this.availableModels[this.selectedModel]).subscribe(data => {this.getModels()}, err => this.handleError(err));
  }

  tryDeleteModel() {
    this.deletePopUp().subscribe(result => {
      if (result) {
        this.deleteModel();
      }
    });
  }

  deletePopUp() {
    const dialogConfig = new MatDialogConfig();

    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    
    dialogConfig.data = {
      'name':this.availableModels[this.selectedModel]
    };
    dialogConfig.width = '500px';

    const dia = this.dialog.open(DeletepopupComponent, dialogConfig);
    return dia.afterClosed();
  }

  deleteModel() {
    this.trainingbackend.deleteModel(this.availableModels[this.selectedModel]).subscribe(data => {this.reset()}, err => this.handleError(err));
  }

  reset(){
    this.selectedModel = 0;
    this.getModels();
  }

  getModelState(){
    if(this.selectedModelActive) {
       return "active";
    }
    return "inactive";
  }

  handleError(error:any) {
    if (error.status == 500) {
      this.openDialog(error.message);
    }
    else {
      this.openDialog(error.error.message);
    }
  }

  openDialog(message: string) {

    const dialogConfig = new MatDialogConfig();

    dialogConfig.disableClose = false;
    dialogConfig.autoFocus = true;
    
    dialogConfig.data = {
      'message':message
    };
    dialogConfig.width = '500px';
    this.dialog.open(ErrorPopupComponent, dialogConfig);
  }

}
