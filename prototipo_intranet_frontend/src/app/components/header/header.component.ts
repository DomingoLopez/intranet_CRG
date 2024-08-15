import { Component, ElementRef, HostListener, OnInit, computed, effect } from '@angular/core';
import { MenuElement } from '../../interfaces/menu.interface';
import { MenuService } from '../../services/menu.service';
import { CommonModule } from '@angular/common';
import {MatIconModule} from '@angular/material/icon'
import { AuthService } from '../../services/auth.service';
import { MenuFavComponent } from '../shared/menu-fav/menu-fav.component';

@Component({
  standalone: true,
  selector: 'app-header',
  imports: [CommonModule, MatIconModule, MenuFavComponent],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit{

  /******************************************
   * MENU
   ******************************************/
  public menu = computed( () => this.menuService.menu());
  // Elemento superior del manu de familias activo actual
  public activeItem?: MenuElement;

  // Niveles de activacion del elemento activo
  public currentItemsLevel1?: MenuElement[] = [];
  public currentItemsLevel2?: MenuElement[] = [];
  public currentItemsLevel3?: MenuElement[] = [];
  public currentItemsLevel4?: MenuElement[] = [];

  /******************************************
   * SUB MENU (WRAPPER)
   ******************************************/
  // Elementos activos del submenu (4 niveles)
  public activeItemSubmenu1?: MenuElement; 
  public activeItemSubmenu2?: MenuElement; 
  public activeItemSubmenu3?: MenuElement; 
  public activeItemSubmenu4?: MenuElement; 
  
  // Booleano para ver si el wrapper del menu esta activo o no
  public isWrapperMenuVisible = false;

  // Variable de hover sobre enlaces
  public showImageFav: boolean = false;

  // Usuario Activo, para obtener así el menú en función del usuario
  // porque nos traemos el menú personalizado del usuario.
  public user = this.authService.currentUser()

  constructor(private menuService: MenuService,
              private authService: AuthService){
}


  ngOnInit(): void {}


  // Comprobamos si el enlace seleccionado esta activo
  isActive(item: MenuElement): boolean {
    return this.activeItem === item;
  }

  isActiveSubmenuLevel1(item:MenuElement): boolean{
    return this.activeItemSubmenu1 === item;
  }
 
  isActiveSubmenuLevel2(item:MenuElement): boolean{
    return this.activeItemSubmenu2 === item;
  }
 
  isActiveSubmenuLevel3(item:MenuElement): boolean{
    return this.activeItemSubmenu3 === item;
  }

  isActiveSubmenuLevel4(item:MenuElement): boolean{
    return this.activeItemSubmenu4 === item;
  }

/**
 * Funci�n para cambiar los submenus cuando se pasa el raton por encima de los submenus padre,
 * para generar los hijos en el siguiente nivel, etc. 
 * @param event (evento que se emite, no hace falta en verdad)
 * @param item (item sobre el que se ha pasado el raton)
 * @param level (nivel de submenu)
 */
  onSwitchingSubmenusLevel(event: any, item: MenuElement, level:number){
    /* Si sobre el que estamos pasando el raton es otro elemento distinto,
       lo cambiamos por este, cargamos sus hijos como elementos activos
       en el nivel 2
    */

    switch(level){

      case 1 : 
        if(this.activeItemSubmenu1 != item){
          // Ponemos como elemento activo del nivel 1 el elemento seleccionado
          this.activeItemSubmenu1 = item;
          // Ponemos sus hijos como los elementos actuales del nivel 2
          this.currentItemsLevel2 = item.childs
        }
      break;

      case 2 : 
        if(this.activeItemSubmenu2 != item){
          // Ponemos como elemento activo del nivel 1 el elemento seleccionado
          this.activeItemSubmenu2 = item;
          // Ponemos sus hijos como los elementos actuales del nivel 2
          this.currentItemsLevel3 = item.childs
        }
      break;
        
      case 3 : 
        if(this.activeItemSubmenu3 != item){
          // Ponemos como elemento activo del nivel 1 el elemento seleccionado
          this.activeItemSubmenu3 = item;
          // Ponemos sus hijos como los elementos actuales del nivel 2
          this.currentItemsLevel4 = item.childs
        }
      break;     
      
      case 4 : 
      if(this.activeItemSubmenu4 != item){
        // Ponemos como elemento activo del nivel 1 el elemento seleccionado
        this.activeItemSubmenu4 = item;
      }
      break;   


      default:

      break;


    }
  }

 

  // Limpiar men�s activos
  cleanActiveItems(){
    this.currentItemsLevel1 = [];
    this.currentItemsLevel2 = [];
    this.currentItemsLevel3 = [];
    this.currentItemsLevel4 = [];

    this.activeItemSubmenu1 = undefined;
    this.activeItemSubmenu2 = undefined;
    this.activeItemSubmenu3 = undefined;
    this.activeItemSubmenu4 = undefined;
  }


  //Actualizamos elementos activos
  updateFirstLevelActiveItem(){
    this.currentItemsLevel1 = this.activeItem?.childs;
    this.activeItemSubmenu1 = undefined;
    // Cerramos los demas niveles
    this.currentItemsLevel2 = [];
    this.currentItemsLevel3 = [];
    this.currentItemsLevel4 = [];
    this.activeItemSubmenu2 = undefined;
    this.activeItemSubmenu3 = undefined;
    this.activeItemSubmenu4 = undefined;

  }

  updateSecondLevelActiveItem(){
    this.currentItemsLevel2 = this.activeItem?.childs;
  }


  updateThirdLevelActiveItem(){
    this.currentItemsLevel3 = this.activeItem?.childs;
  }


  //Cierre del menu
  closeSubmenuWrapper(){
    this.activeItem = undefined;
    this.isWrapperMenuVisible = false;
    this.cleanActiveItems();
  }

  //Apertura del menu
  openSubmenuWrapper(event: any, item: MenuElement){
    this.activeItem = item;
    this.isWrapperMenuVisible = true;
    this.updateFirstLevelActiveItem();
  }



// open/close function
  openCloseSubmenuWrapper(event: any, item: MenuElement){
    event.preventDefault();
    if(this.activeItem === item){
      this.closeSubmenuWrapper();
    }else{
      this.openSubmenuWrapper(event, item);

    }
  }

  // obtener elemento activo del nivel
  getActiveItemLevel(level:number){
    return this.activeItem?.childs
  }

  // Cerrar sesion del CI
  cerrarSesion(){
    this.authService.logout()
  }



}
