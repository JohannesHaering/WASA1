import { Component, OnInit } from '@angular/core';
import { Filter } from '../filter'
import { BackendtrainingserviceService } from '../backendtrainingservice.service'
import { TrainingResult } from '../Trainingresult'
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { ErrorPopupComponent } from '../error-popup/error-popup.component';

@Component({
  selector: 'app-trainingpage',
  templateUrl: './trainingpage.component.html',
  styleUrls: ['./trainingpage.component.css']
})
export class TrainingpageComponent implements OnInit {

  availableFilter:String[] = [];
  selectedFilter:number = 0; 
  trainedName:String = "abc";
  state:number = 0;
  trainResult:Number = 0;
  nameAvailable:Boolean = false;

  availcalled:number=0;

  constructor(private backend:BackendtrainingserviceService, private dialog: MatDialog) { }

  ngOnInit(): void {
    this.backend.getAvailableFilter().subscribe(data => {this.availableFilter = data});
  }

  setName(name:string) {
    this.trainedName = name;
    this.nameAvailable = this.canStartTraining();
  }

  changeSelectedFilter(id:number){
    this.selectedFilter = id;
  }

  startTrainingPhase() {
    this.setTrainingState();
  }

  endTrainingPhase() {
    this.setTrainingEndState();
  }

  reset() {
    this.trainedName = '';
    this.trainResult = 0;
    this.resetState();
  }

  resetState() {
    this.state = 0; 
  }
  setTrainingState() {
    this.state=1;
  }
  setTrainingEndState(){
    this.state=2;
  }

  isReset(){
    return (this.state == 0);
  }
  isTraining(){
    return (this.state == 1); 
  }
  trainingEnded(){
    return (this.state == 2);
  }

  canStartTraining() {
    var truncname = this.trainedName.replace(/\s/g, "").toLowerCase();
    this.backend.isNameAvailable(truncname).subscribe(data => this.nameAvailable = data);
    if (truncname === '') {
      return false;
    }
    return true;
  }

  train() {
    if (!this.canStartTraining()) {
      return;
    }
    this.setTrainingState()
    this.backend.train(this.trainedName, this.availableFilter[this.selectedFilter]).subscribe(
      data => {
        this.trainResult = data; 
        this.setTrainingEndState(); 
      },
      error => {
        this.handleError(error);
        this.reset();
      }
      );
  }

  delete() {
    this.backend.deleteModel(this.trainedName).subscribe();
    this.reset();
  }

  handleError(error:any) {
    console.log(error);
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
