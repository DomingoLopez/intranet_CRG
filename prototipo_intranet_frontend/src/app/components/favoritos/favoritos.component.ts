import { Component, OnInit, computed, effect } from '@angular/core';
import { MenuService } from '../../services/menu.service';
import { MenuElement } from '../../interfaces/menu.interface';
import { CommonModule } from '@angular/common';
import { MenuFavComponent } from '../shared/menu-fav/menu-fav.component';
import {CdkDragDrop, CdkDropList, CdkDrag, moveItemInArray} from '@angular/cdk/drag-drop';


@Component({
  selector: 'app-favoritos',
  standalone: true,
  imports: [CommonModule, MenuFavComponent,CdkDropList, CdkDrag],
  templateUrl: './favoritos.component.html',
  styleUrl: './favoritos.component.scss'
})
export class FavoritosComponent implements OnInit{


  public favoritos: MenuElement[] = [];


  constructor(private menuService: MenuService){

    effect(() => {
      this.favoritos = this.buscarElementosFavoritos(this.menuService.menu())
    });

  }

  ngOnInit(): void {
     
  }

 /**
 * Funcion que busca recursivamente aquellos elementos del menu
 * que no tengan hijos, que permitan marcar como favoritos y que
 * estan marcados como favoritos
 * @returns elementosEncontrados -> Array de elementos del menu favoritos
 */
  private buscarElementosFavoritos(menu: MenuElement[]): MenuElement[] {
    let elementosEncontrados: MenuElement[] = [];

    function buscar(menuItems: MenuElement[]) {
        for (const item of menuItems) {
            if (item.permitir_fav && item.is_fav && item.childs.length === 0) {
                elementosEncontrados.push(item);
            }
            if (item.childs.length > 0) {
                buscar(item.childs);
            }
        }
    }

    buscar(menu);
    return elementosEncontrados;
  }
  


  drop(event: CdkDragDrop<string[]>) {
    
    moveItemInArray(this.favoritos, event.previousIndex, event.currentIndex);
    console.log(this.favoritos)
  }



  
}
