import { Component, OnInit, Input } from '@angular/core';
import { BackendserviceService } from '../backendservice.service';
import { Modelstatistic } from '../modelstatistic';

@Component({
  selector: 'app-modeldescription',
  templateUrl: './modeldescription.component.html',
  styleUrls: ['./modeldescription.component.css']
})
export class ModeldescriptionComponent implements OnInit {
  hitsratio:number = 10;

  @Input() statistic:Modelstatistic = {"hits": 10,"misses": 10};

  constructor(private backend:BackendserviceService) {
  }

  ngOnInit(): void {
  }


}
