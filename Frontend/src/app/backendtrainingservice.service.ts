import { Injectable } from '@angular/core';
import { Filter } from './filter';
import { TrainingResult } from './Trainingresult';
import { HttpClient,HttpErrorResponse } from '@angular/common/http'
import { Observable, throwError } from 'rxjs'
import {catchError} from 'rxjs/operators';
import { boolreturn } from './boolreturn';
import { Stringreturn } from './stringreturn';
import config from '../assets/config.json'

@Injectable({
  providedIn: 'root'
})
export class BackendtrainingserviceService {
  config:any = config;
  availableFilter:Filter[] = [{name:"Filter1"}, {name:"Filter2"},{name:"Filter3"}];
  takenNames:String[] = ["Model1", "Model2", "Model3"];

  baseIp:string = 'http://127.0.0.1:5000/';
  startTrainingIp:string = 'models/train';
  getFilterIp:string = 'models/filters';
  isNameAvailableIp:string = 'models/availability/';
  deleteModelIp:string = 'models/'

  constructor(private http:HttpClient) { 
    this.baseIp = config.backendip + ':' + config.backendport + '/'
  }

  getAvailableFilter(): Observable<String[]>{
    return this.http.get<String[]>(this.baseIp.concat(this.getFilterIp));
  }

  isNameAvailable(name:String):Observable<Boolean>{
    return this.http.get<Boolean>(this.baseIp + this.isNameAvailableIp + name);
  }

  train(modelname:String, filter:String):Observable<Number> {
    return this.http.post<Number>(this.baseIp + this.startTrainingIp, {"modelName":modelname, "filterName":filter});
  }

  deleteModel(model:String):Observable<boolean>{
    return this.http.delete<boolean>(this.baseIp + this.deleteModelIp + model);
  }

}
