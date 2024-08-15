import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, map, Observable, of } from 'rxjs';
import { Aviso } from '../interfaces/avisos.interface';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AvisosService {

  private baseUrl: string = environment.baseURL;


  constructor(private http: HttpClient) { }

  /**
   * Función para obtener los avisos de la intranet
   * @returns observable de avisos
   */
  getAvisos(): Observable <Aviso[]> {
    
    return this.http.get<Aviso[]>(`${this.baseUrl}/avisos/`);
  }


  
}
