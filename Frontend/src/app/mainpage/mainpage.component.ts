import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-mainpage',
  templateUrl: './mainpage.component.html',
  styleUrls: ['./mainpage.component.css']
})
export class MainpageComponent implements OnInit {
  activepage:number = 0;

  constructor() { }

  ngOnInit(): void {
    this.activepage = 1;
  }

  homeClicked() {
    this.activepage = 0; 
  }

  modelViewClicked() {
    this.activepage = 1;
  }

  trainingButtonClicked(){
    this.activepage = 2;
  }

}
