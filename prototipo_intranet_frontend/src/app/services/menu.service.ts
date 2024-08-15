import { Injectable, computed, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { catchError, map, Observable, of, throwError } from 'rxjs';
import { MenuElement } from '../interfaces/menu.interface';
import { MenuFavRequest } from '../interfaces/menu-fav.interface';
import { environment } from '../../environments/environment';
import { User } from '../interfaces/user.interface';

@Injectable({
  providedIn: 'root'
})
export class MenuService {

  private baseUrl: string = environment.baseURL;
  // Menu del aplicativo, una vez lo obtenemos
  // guardamos este
  private _menu = signal<MenuElement[]>([]);
  public menu = computed ( () => this._menu())

  constructor(private http: HttpClient) { 
    this.loadMenu();
  }

  /**
   * Funcion para obtener el menu de la intranet
   * @returns observable de menu
   */
  private loadMenu(): void {
    this.http.get<MenuElement[]>(`${this.baseUrl}/menu/`).pipe(
      map((menu: MenuElement[]) => {
        this._menu.set(menu); // Guardamos el menú en el signal
      }),
      catchError((error) => {
        console.error('Error al obtener el menú:', error);
        this._menu.set([]); // Devolvemos un array vacío en caso de error
        return of([]);
      })
    ).subscribe();
  }
  

  /**
   * Funcion para buscar en los menus una cadena
   * @param searchQuery 
   */
  searchInMenu(searchQuery: string): MenuElement[] {
    return this.filterMenu(this.menu(), searchQuery);
  }

  /**
   * Funcion auxiliar recursiva para buscar en los hijos de Elementos.
   * Asi nos aseguramos que buscamos en todos
   * @param menu 
   * @param searchQuery 
   * @returns 
   */
  private filterMenu(menu: MenuElement[], searchQuery: string): MenuElement[] {
    const filteredMenu: MenuElement[] = [];
    for (const item of menu) {
      if (item.childs.length === 0 && item.label.toLowerCase().includes(searchQuery.toLowerCase()) && item.label.toLowerCase() != '#' && item.url.toLowerCase() != '#' ) {
        const filteredItem = {
          id_menu: item.id_menu,
          label: item.label,
          categoria: item.categoria,
          tipo_activo: item.tipo_activo,
          url: item.url,
          order: item.order,
          permitir_fav: item.permitir_fav,
          is_fav: item.is_fav,
          ruta: item.ruta,
          childs: item.childs
        };
        filteredMenu.push(filteredItem);
      } else if (item.childs.length > 0) {
        const filteredChilds = this.filterMenu(item.childs, searchQuery);
        filteredMenu.push(...filteredChilds); // Añadir solo los hijos filtrados, si los hay
      }
    }
    return filteredMenu;
  }


  /**
   * Función para actualizar el menú, sin tener que volver a pedirlo vía server.
   * El procesamiento lo hacemos en el cliente y ahorramos execution time en el server.
   * Básicamente, para cada item, lo mapea y si es fav, lo pongo no fav y viceversa. 
   * Si tiene hijos, devuelvo la función recursiva.
   * @param menu 
   * @param item_fav 
   */

  private updateMenuFav(menu: MenuElement[], item_fav: MenuElement): MenuElement[] {
    return menu.map(item => {
      if (item.childs.length == 0 && item_fav.id_menu == item.id_menu) {
        item.is_fav = item.is_fav ? false : true;
        return {...item};
      } else if (item.childs.length > 0) {
        return {...item, childs: this.updateMenuFav(item.childs, item_fav) };
      } else {
        return item;
      }
    });
  }



  /**
   * Actualiza si un item de menú es favorito o no haciendo llamada al server para cambiarlo.
   * En la devolución, si todo ok, lo cambiamos también aquí, si no, no lo cambiamos
   * @param empleado 
   * @param item_menu 
   * @param accion 
   * @returns 
   */
  public updateFav(empleado: User, item_menu: MenuElement, accion: Boolean ): Observable<Boolean> {
    
    const menuFav: MenuFavRequest = {
      id_empleado: empleado.id_empleado,
      id_menu: item_menu.id_menu,
      accion: accion
    };
    
    const body = menuFav
    let menu = this.menu()
    return this.http.post<Boolean>(`${this.baseUrl}/fav/`,body)
      .pipe(
        map( (resp) => {
            //Con [...menu] conseguimos hacer una copia superficial y también detecta el cambio
            //let menu_def = this.updateMenu([...menu], item_menu );
            const menu_def = this.updateMenuFav(menu, item_menu );
            //Seteamos el menú
            this._menu.set(menu_def);
            return true;
        }),
        catchError( err => {
          console.log(err)
          return of(false);
        })
      )
  }


  
}
