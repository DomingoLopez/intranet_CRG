import { Component, computed, effect, signal } from '@angular/core';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';  
import { debounceTime } from 'rxjs/operators';
import { MenuService } from '../../services/menu.service';
import { MenuElement } from '../../interfaces/menu.interface';
import { MenuFavComponent } from '../shared/menu-fav/menu-fav.component';
import { CommonModule } from '@angular/common';


@Component({
  selector: 'app-searchbar',
  standalone: true,
  imports: [
    MatInputModule,
    MatFormFieldModule,
    MatIconModule,
    MenuFavComponent,
    FormsModule,
    CommonModule
  ],
  templateUrl: './searchbar.component.html',
  styleUrl: './searchbar.component.scss'
})
export class SearchbarComponent {

  // Controlador de apertura de box de busqueda
  public isResultBoxVisible:boolean = false;
  // Valor boolean para controlar el elemento activo de la búsqueda realizada
  public activeResultSearchElement?: MenuElement;
  // Cadena de busqueda
  public searchQuery: string = '';
  // Delay en la busqueda
  private searchTimeout: any;

  // Elementos encontrados tras la busqueda
  public resultSearch: MenuElement[] = []

  constructor(private menuService: MenuService){

    effect(() => {
        // Invocamos aquí a checkFavSearchResult pasándole el menú
        // ya que hay que volver a generar 
        this.updateSearchResults(this.menuService.menu())
    });

  }

  /**
   * 
   */
  updateSearchResults(menu: MenuElement[]): void{
    // Si estamos mostrando resultados, entonces
    // hemos de actualizar los resultados
    if(this.resultSearch.length > 0){
      this.searchInMenu()
    }

  }


  /**
   * Al hacer focus sobre la barra de búsqueda
   * muestra el contenedor de búsqueda
   */
  onFocusSearchBar(): void{
    this.isResultBoxVisible = true;
  }


  /**
   * Al quitar el foco de la barra, oculta el contenedor
   * y pon la query vacía y resultados vacíos.
   */
  onBlurSearchBar():void{
    this.isResultBoxVisible = false;
    this.resultSearch= [];
    this.searchQuery = "";
  }

/**
 * Cerrar conteneodr de búsqueda, etc.
 */
  closeSearchBox():void{
    this.isResultBoxVisible = false;
    this.resultSearch= [];
    this.searchQuery = "";
  }

  /* Al buscar en el input de busqueda, si hay mas de 4 letras
  * ponemos timeout de medio segundo para buscar
  */
  onSearchInput(event: any): void {
    clearTimeout(this.searchTimeout); // Limpiar el temporizador anterior
    // Establecer un nuevo temporizador
    if (this.searchQuery.trim().length >= 4) {
      this.searchTimeout = setTimeout(() => {  
        this.searchInMenu();
      }, 500);
    } else {
      this.resultSearch= []; // Limpiar los resultados si la longitud es menor que 4
    }

  }

  /**
   * Funcion para buscar en el menu segun la cadena de búsqueda
   */
  searchInMenu():void{
    if (this.searchQuery.trim() !== '') {
      let results = this.menuService.searchInMenu(this.searchQuery);
      this.resultSearch = results;
    } else {
      this.resultSearch= [];
    }
  }

  /**
   * Elemento está activo o no
   * @param item 
   * @returns 
   */
  isActive(item: MenuElement):boolean{
    return item === this.activeResultSearchElement
  }


/**
 * Funcion para cambiar los submenus cuando se pasa el raton por encima de los submenus padre,
 * para generar los hijos en el siguiente nivel, etc. 
 * @param event (evento que se emite, no hace falta en verdad)
 * @param item (item sobre el que se ha pasado el raton)
 * @param level (nivel de submenu)
 */
onSwitchingResultSearchElement(event: any, item: MenuElement){
  this.activeResultSearchElement = item
}



}
