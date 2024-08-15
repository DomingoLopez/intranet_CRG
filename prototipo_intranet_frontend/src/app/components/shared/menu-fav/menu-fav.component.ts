import { Component, Input } from '@angular/core';
import { MenuElement } from '../../../interfaces/menu.interface';
import { CommonModule } from '@angular/common';
import { MenuService } from '../../../services/menu.service';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-menu-fav',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './menu-fav.component.html',
  styleUrl: './menu-fav.component.scss'
})


/**
 * Componente para disponer de un botón/estrellita con la que poder hacer fav
 * de componentes del menú, y guardarlos como accesos rápidos en nuestros favoritos.
 * Es mucho mejor esto que tener el componente en varios sitios a la vez, puesto a piñón.
 */
export class MenuFavComponent {

  @Input() menuItem?: MenuElement;

  constructor(private menuService: MenuService,
              private authService: AuthService
  ){}


  /**
   * Función que comprueba si el item está activo.
   * Si lo está, debe actualizar el item de menú para
   * ponerlo en el estado contrario, y hacer petición post
   * para actualizarlo en la tabla de favoritos.
   */
  switchFav(): void{

    const current_user = this.authService.currentUser() as any;
    const accion = this.menuItem?.is_fav ? false : true;

    // Esto es un poco guarrería (lo del as any), pero funciona. Esto mientras
    // no la liemos con llamadas a parámetros que no sean comunes está bien
    this.menuService.updateFav( current_user  , this.menuItem as any , accion).subscribe(res =>{
      console.log(res)
    })


  }


}
