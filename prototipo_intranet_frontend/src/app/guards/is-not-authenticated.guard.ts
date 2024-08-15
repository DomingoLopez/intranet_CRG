import { inject } from "@angular/core";
import { CanActivateFn, Router } from "@angular/router";
import { AuthService } from "../services/auth.service";
import { AuthStatus } from "../interfaces/auth-status.enum";


export const isNotAuthenticatedGuard: CanActivateFn = (route, state) => {

  const authService = inject( AuthService );
  const router = inject( Router );

  // Si estoy autenticado, redirecciono y devuelvo false
  if(authService.authStatus() === AuthStatus.authenticated){
    router.navigateByUrl('/intranet')
    return false;
  }

  return true;

}