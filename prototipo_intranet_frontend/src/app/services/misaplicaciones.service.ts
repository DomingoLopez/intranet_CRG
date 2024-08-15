import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { miAplicacion } from '../interfaces/misaplicaciones.interface';

@Injectable({
  providedIn: 'root'
})
export class MisaplicacionesService {

  private baseUrl: string = environment.baseURL;


  constructor(private http: HttpClient) { }

  /**
   * Función para obtener los avisos de la intranet
   * @returns observable de mis aplicaciones
   */
  getMisAplicaciones(): Observable <miAplicacion[]> {
    
    return this.http.get<miAplicacion[]>(`${this.baseUrl}/misaplicaciones/`);
  }

}
