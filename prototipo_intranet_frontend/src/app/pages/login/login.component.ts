import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule} from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

import Swal from 'sweetalert2'
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  
  // Variables formulario
  public submitted: boolean = false;
  public loginForm: FormGroup;

  // Spinner para cuando hacemos la petición
  // TODO - HACER EL SPINNER UN COMPONENTE INDEPENDIENTE
  public isLoading: boolean = false;
  public errorMessage: string = '';

  constructor(private formBuilder: FormBuilder,
              private authService: AuthService,
              private router: Router) { 

    this.loginForm = this.formBuilder.group({
      user: ['', [Validators.required]],
      password: ['', Validators.required]
    });

  }

  /**
   * Enviamos datos del usuario al servidor.
   * Si todo ok, guardamos token (tb se ha guardado en caché en el server),
   * para comparar después con este vaya que lo reemplazen o hagan 
   * substracción de sesión, etc.
   */
  onSubmit() {

    this.submitted = true;

    if (this.loginForm.valid) {

      // Indicamos flag para loader del botón
      this.isLoading = true;
      // parseamos email y contraseña:
      const {user, password} = this.loginForm.value

      this.authService.login(user, password).subscribe({
        next: () => this.router.navigateByUrl('/intranet'),
        error: (message) => {
          Swal.fire({
          title: "Error en la autenticación",
          text: message.error.detail,
          icon: "error",
          confirmButtonColor: "#004B3A",   
          confirmButtonText: "Ok"
          })
          this.isLoading = false;
        }
      })
    
    
    }

  }

}
