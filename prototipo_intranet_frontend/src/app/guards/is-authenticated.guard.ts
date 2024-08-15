import { inject } from "@angular/core";
import { CanActivateFn, Router } from "@angular/router";
import { AuthService } from "../services/auth.service";
import { AuthStatus } from "../interfaces/auth-status.enum";


export const isAuthenticatedGuard: CanActivateFn = (route, state) => {

  const authService = inject( AuthService );
  const router = inject( Router );

  // Si estoy autenticado, devuelvo true, si no redirecciono al login 
  // de nuevo
  if(authService.authStatus() === AuthStatus.authenticated){
    return true;
  }

  if(authService.authStatus() === AuthStatus.checking){
    return false;
  }

  // const url = state.url;
  // localStorage.setIem('url',url);
  router.navigateByUrl('/login');
  return false;

}