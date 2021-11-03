import { Component, OnInit, Inject } from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-error-popup',
  templateUrl: './error-popup.component.html',
  styleUrls: ['./error-popup.component.css']
})
export class ErrorPopupComponent implements OnInit {

  message:string="";
  private dialogRef: MatDialogRef<ErrorPopupComponent>;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any
 ) { this.message = data.message;}

  ngOnInit(): void {
  }

  close() {
    this.dialogRef.close();
  }

}
