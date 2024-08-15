import { Injectable, computed, inject, signal } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, catchError, map, of, tap, throwError } from 'rxjs';
import { User } from '../interfaces/user.interface';
import { AuthStatus } from '../interfaces/auth-status.enum';
import { LoginResponse } from '../interfaces/login-response.interface';
import { CheckTokenResponse } from '../interfaces/check-token.response';

@Injectable({
  providedIn: 'root'
})
export class AuthService{

  private baseUrl: string = environment.baseURL;
  // Señales, son como observables, pero no, son como variables inteligentes
  // que saben dónde están llamadas, y cualquier cambio en ellas afecta a donde
  // se llama, es un poco evolución de los estados de la web, etc. 

  private _currentUser = signal<User|null>(null);
  private _authStatus = signal<AuthStatus>(AuthStatus.checking);

  //! Al mundo exterior
  public currentUser = computed ( () => this._currentUser())
  public authStatus = computed ( () => this._authStatus())


  constructor(private http: HttpClient) { 
    this.checkAuthStatus().subscribe();
  } 



  /**
   * Función para establecer usuario autenticado en signals,
   * guardar token en localStorage
   * @param user: id de usuario
   * @param token: Bearer token recibido
   * @returns 
   */
  private setAuthentication(user: User, token:string): boolean {

    this._currentUser.set( user );
    this._authStatus.set( AuthStatus.authenticated );
    this.addToLocalStorage(user, token);

    return true;
  }


  /**
   * Función para enviar los parámetros del formulario al server y loguearse
   * @param user: id de usuario
   * @param password: contraseña de usuario
   * @returns 
   */
  login(user: string, password: string): Observable <boolean> {

    const body = {user, password}
    // return this.http.post<LoginResponse>(`${this.baseUrl}/auth/login`, body)
    return this.http.post<LoginResponse>(`${this.baseUrl}/auth/`,body)
      .pipe(
        map( ({ user, token }) => this.setAuthentication( user, token )),
        catchError( err => {
          return throwError(err)
        })
      );
  }
  



  /**
  * Función para añadir los elementos necesarios del usuario 
  * al localStorage
  */
  addToLocalStorage(user:User, token: string){
    localStorage.setItem('token', token);
    localStorage.setItem('id_empleado', user.id_empleado);
    localStorage.setItem('centro', user.centro);
    localStorage.setItem('nomcentro', user.nomcentro);
    localStorage.setItem('nombre', user.nombre);
  }


  /**
  * Función para añadir los elementos necesarios del usuario 
  * al localStorage
  */
    cleanLocalStorage(){
      localStorage.removeItem('token');
      localStorage.removeItem('id_empleado');
      localStorage.removeItem('centro');
      localStorage.removeItem('nomcentro');
      localStorage.removeItem('nombre');
    }




  
  /**
   * Función para desloguearse, y quitar token, etc.
   * Unset de todo lo que haya del usuario
   */
  logout() {
    this.cleanLocalStorage()
    this._currentUser.set(null);
    this._authStatus.set( AuthStatus.notAuthenticated );
  }


  checkAuthStatus(): Observable<boolean>{

    const token = localStorage.getItem('token');
    // Si token no existe, directamente false
    if ( !token ) {
      this.logout();
      return of(false);
    }

    // Si el token existe, habrá que comprobar con el backend si es válido
    // creamos headers
    // AQUÍ 
    const headers = new HttpHeaders()
        .set('Authorization', `Bearer ${token}`)

    return this.http.get<CheckTokenResponse>(`${this.baseUrl}/auth/checktoken`, {headers})
                    .pipe(
                      map( ({user, token}) =>  this.setAuthentication(user,token)),
                      catchError( (err) =>{
                        console.log("error",err)
                        this._authStatus.set( AuthStatus.notAuthenticated );
                        return of(false);
                      })
                    )
  }
  

}
