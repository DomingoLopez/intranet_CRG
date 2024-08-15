import { Component, computed } from '@angular/core';
import { HeaderComponent } from '../../components/header/header.component';
import { SearchbarComponent } from '../../components/searchbar/searchbar.component';
import { AvisosComponent } from '../../components/avisos/avisos.component';
import { FavoritosComponent } from '../../components/favoritos/favoritos.component';
import { NormativaComponent } from '../../components/normativa/normativa.component';
import { MisAplicacionesComponent } from '../../components/mis-aplicaciones/mis-aplicaciones.component';
import { TablonComponent } from '../../components/tablon/tablon.component';
import { FooterComponent } from '../../components/footer/footer.component';
import { AuthService } from '../../services/auth.service';
import { AccesosRapidosComponent } from '../../components/accesos-rapidos/accesos-rapidos.component';

@Component({
  standalone: true,
  imports: [
    HeaderComponent, 
    SearchbarComponent, 
    AvisosComponent, 
    FavoritosComponent,
    NormativaComponent,
    MisAplicacionesComponent,
    TablonComponent,
    FooterComponent,
    AccesosRapidosComponent
    ],
  templateUrl: './principal.component.html',
  styleUrls: ['./principal.component.scss']
})
export default class PrincipalComponent {

  // Como solo tenemos la propiedad computada, será solo de solo lectura
  public user = computed( () => this.authService.currentUser());

  constructor(private authService: AuthService){}



}
