import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { NormativaService } from '../../services/normativa.service';
import { NormativaElement } from '../../interfaces/normativa.interface';
import { MatIconModule } from '@angular/material/icon';
import { SectionTitleComponent } from '../shared/section-title/section-title.component';

@Component({
  selector: 'app-normativa',
  standalone: true,
  imports: [CommonModule,MatIconModule,SectionTitleComponent],
  templateUrl: './normativa.component.html',
  styleUrl: './normativa.component.scss'
})
export class NormativaComponent implements OnInit{

  public normativa: NormativaElement[] = []

  constructor(private normativaService: NormativaService){}


  ngOnInit(): void {
    this.normativaService.getNormativa().subscribe(normativa =>{
      this.normativa = normativa;
    });
  }

}
