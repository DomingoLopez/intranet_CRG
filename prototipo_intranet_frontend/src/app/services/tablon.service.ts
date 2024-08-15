import { Injectable, OnInit } from '@angular/core';
import { map, Observable, of } from 'rxjs';
import { TablonElement } from '../interfaces/tablon.interface';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class TablonService{

  private baseUrl: string = environment.baseURL;

  constructor(private http: HttpClient) { }


  getNoticias(): Observable<TablonElement[]> {

    return this.http.get<TablonElement[]>(`${this.baseUrl}/tablon/`).pipe(
      map(noticias => noticias.map(noticia => ({
        ...noticia, 
        titulo:this.decodeHtml(noticia.titulo)
      })))
    );

  }

  private decodeHtml(html:string): string{
    const txt = document.createElement('textarea');
    txt.innerHTML = html;
    return txt.value;
  }



}
