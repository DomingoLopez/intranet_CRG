import { Component, OnInit } from '@angular/core';
import { TablonElement } from '../../interfaces/tablon.interface';
import { TablonService } from '../../services/tablon.service';
import { CommonModule } from '@angular/common';
import { SectionTitleComponent } from '../shared/section-title/section-title.component';

@Component({
  selector: 'app-tablon',
  standalone: true,
  imports: [CommonModule,SectionTitleComponent],
  templateUrl: './tablon.component.html',
  styleUrl: './tablon.component.scss'
})
export class TablonComponent implements OnInit{


  // Podemos reutilizar la interfaz de normativa
  public noticias: TablonElement[] = []

  constructor(private tablonService: TablonService){}


  ngOnInit(): void {
    
    this.tablonService.getNoticias().subscribe(noticias =>{
      this.noticias = noticias
    });

  }















}
