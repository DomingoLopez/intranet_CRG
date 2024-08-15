import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { NormativaElement } from '../interfaces/normativa.interface';

@Injectable({
  providedIn: 'root'
})
export class NormativaService {

  private baseUrl: string = environment.baseURL;

  constructor(private http: HttpClient) { }

  /**
   * Funci�n para obtener la normativa de la intranet
   * @returns observable de avisos
   */
  getNormativa(): Observable <NormativaElement[]> {
    
    return this.http.get<NormativaElement[]>(`${this.baseUrl}/normativa/`);
  }

}
