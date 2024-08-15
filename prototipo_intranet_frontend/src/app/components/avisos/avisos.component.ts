import { Component, OnInit, ViewChild } from '@angular/core';
import { AvisosService } from '../../services/avisos.service';
import { Aviso } from '../../interfaces/avisos.interface';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { SectionTitleComponent } from '../shared/section-title/section-title.component';

@Component({
  selector: 'app-avisos',
  standalone: true,
  imports: [CommonModule, MatIconModule, SectionTitleComponent],
  templateUrl: './avisos.component.html',
  styleUrl: './avisos.component.scss'
})
export class AvisosComponent implements OnInit {

  avisos: Aviso[] = [];

  constructor(private avisosService: AvisosService){}
  

  ngOnInit(): void {
      this.avisosService.getAvisos().subscribe(avisos =>{
        this.avisos = avisos;
      });
  }



}
