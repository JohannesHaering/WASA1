import { Injectable } from '@angular/core';
import { Modelstatistic } from './modelstatistic';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import config from '../assets/config.json'

@Injectable({
  providedIn: 'root'
})
export class BackendserviceService {
  config:any = config;
  baseIp:string = 'http://127.0.0.1:5000/';
  getModelIp:string = 'models';
  getModelStatisticIp:string = 'models/';
  setActiveIP:string = 'models/set/'
  
  constructor(private http:HttpClient) {
    this.baseIp = config.backendip + ':' + config.backendport + '/'
  }

  setActive(modelname:String):Observable<boolean> {
    return this.http.get<boolean>(this.baseIp + this.setActiveIP + modelname);
  }

  isActive(modelname:String):Observable<boolean> {
    return this.http.get<boolean>(this.baseIp + this.createIsActiveIP(modelname));
  }

  getAvailableModels(): Observable<String[]>{
    return this.http.get<String[]>(this.baseIp + this.getModelIp)
  }

  getModelstatistics(modelname:String):Observable<Modelstatistic> {
    return this.http.get<Modelstatistic>(this.baseIp + this.getModelStatisticIp + modelname);
  }

  createIsActiveIP(modelname:String) {
      return 'models/' + modelname + '/isActive'
  }

}
