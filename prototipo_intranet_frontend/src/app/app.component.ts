import { Component, computed, effect } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';
import { AuthService } from './services/auth.service';
import { AuthStatus } from './interfaces/auth-status.enum';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {

  // variable para comprobar si ya estamos logueados o no
  public finishedAuthCheck = computed<boolean>( () => {
    // Si aun estoy en checking, es que aun no he terminado de
    // comprobar si ya estoy autenticado o no
    if(this.authService.authStatus() === AuthStatus.checking)
      return false;
    
    return true;
  });


  // variable efecto, que se lanza tras recibir una accion
  // El efecto se lanza la primera vez que se crea, y luego 
  // cada vez que la señal en el efecto cambie.
  public authStatusChangedEffect = effect( () => {
    
    console.log('authStatus',this.authService.authStatus())

    switch(this.authService.authStatus()){

      case AuthStatus.checking:
        return;
      
      case AuthStatus.authenticated:
        this.router.navigateByUrl('/intranet');
        return;

      case AuthStatus.notAuthenticated:
        this.router.navigateByUrl('/login')
        return;

    }

  });


  constructor(private authService: AuthService, 
              private router: Router){}



  

}
