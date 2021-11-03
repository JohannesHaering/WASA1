import { Component, OnInit, Inject } from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material/dialog";

@Component({
  selector: 'app-deletepopup',
  templateUrl: './deletepopup.component.html',
  styleUrls: ['./deletepopup.component.css']
})
export class DeletepopupComponent implements OnInit {

  name:string="";
  private dialogRef: MatDialogRef<DeletepopupComponent>;

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: any
 ) { this.name = data.name;}

  ngOnInit(): void {
  }

  close() {
    this.dialogRef.close();
  }

}
