import { Component, OnInit } from '@angular/core';
import { miAplicacion } from '../../interfaces/misaplicaciones.interface';
import { MisaplicacionesService } from '../../services/misaplicaciones.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-mis-aplicaciones',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './mis-aplicaciones.component.html',
  styleUrl: './mis-aplicaciones.component.scss'
})
export class MisAplicacionesComponent implements OnInit{

  public misAplicaciones: miAplicacion[] = [];

  constructor(private misaplicacionesService : MisaplicacionesService){}



  ngOnInit(): void {
    this.misaplicacionesService.getMisAplicaciones().subscribe(misapps =>{
      this.misAplicaciones = misapps;
    });
  }





}
