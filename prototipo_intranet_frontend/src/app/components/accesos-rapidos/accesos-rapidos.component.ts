import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-accesos-rapidos',
  standalone: true,
  imports: [
    CommonModule,
    MatIconModule],
  templateUrl: './accesos-rapidos.component.html',
  styleUrl: './accesos-rapidos.component.scss'
})
export class AccesosRapidosComponent {

}
