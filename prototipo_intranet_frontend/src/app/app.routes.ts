import { Routes } from '@angular/router';
import { Error404Component } from './pages/404/error404.component';
import { LoginComponent } from './pages/login/login.component';
import { isAuthenticatedGuard } from './guards/is-authenticated.guard';
import { isNotAuthenticatedGuard } from './guards/is-not-authenticated.guard';

export const routes: Routes = [

    {
        path: 'intranet',
        title: 'Intranet CRG',
        loadComponent: () => import('./pages/principal/principal.component'),
        canActivate: [isAuthenticatedGuard]
    },

    {
        path: 'login',
        component: LoginComponent,
        canActivate: [isNotAuthenticatedGuard]

    },

    {
      path: '404',
      component: Error404Component
    },

    {
        path: '',
        redirectTo: 'intranet',
        pathMatch: 'full'
    },

    {
        path:'**',
        redirectTo:'404'
    }


];
