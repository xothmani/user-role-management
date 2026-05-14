import { Routes } from '@angular/router';
import { authGuard } from './core/auth.guard';
import { LayoutComponent } from './layout/layout.component';

export const routes: Routes = [
  {
    path: 'login',
    loadComponent: () =>
      import('./modules/auth/login/login.component').then((c) => c.LoginComponent)
  },
  {
    path: '',
    component: LayoutComponent,
    canActivate: [authGuard],
    children: [
      { path: '', redirectTo: 'utilisateurs', pathMatch: 'full' },
      {
        path: 'utilisateurs',
        loadComponent: () =>
          import('./modules/utilisateurs/utilisateurs-list/utilisateurs-list.component').then(
            (c) => c.UtilisateursListComponent
          )
      },
      {
        path: 'utilisateurs/nouveau',
        loadComponent: () =>
          import('./modules/utilisateurs/utilisateurs-form/utilisateurs-form.component').then(
            (c) => c.UtilisateursFormComponent
          )
      },
      {
        path: 'utilisateurs/:id/modifier',
        loadComponent: () =>
          import('./modules/utilisateurs/utilisateurs-form/utilisateurs-form.component').then(
            (c) => c.UtilisateursFormComponent
          )
      },
      {
        path: 'roles',
        loadComponent: () =>
          import('./modules/roles/roles-list/roles-list.component').then(
            (c) => c.RolesListComponent
          )
      },
      {
        path: 'roles/nouveau',
        loadComponent: () =>
          import('./modules/roles/roles-form/roles-form.component').then(
            (c) => c.RolesFormComponent
          )
      },
      {
        path: 'roles/:id/modifier',
        loadComponent: () =>
          import('./modules/roles/roles-form/roles-form.component').then(
            (c) => c.RolesFormComponent
          )
      },
      {
        path: 'permissions',
        loadComponent: () =>
          import('./modules/permissions/permissions-list/permissions-list.component').then(
            (c) => c.PermissionsListComponent
          )
      },
      {
        path: 'permissions/nouveau',
        loadComponent: () =>
          import('./modules/permissions/permissions-form/permissions-form.component').then(
            (c) => c.PermissionsFormComponent
          )
      },
      {
        path: 'permissions/:id/modifier',
        loadComponent: () =>
          import('./modules/permissions/permissions-form/permissions-form.component').then(
            (c) => c.PermissionsFormComponent
          )
      },
      {
        path: 'historique',
        loadComponent: () =>
          import('./modules/historique/historique-list/historique-list.component').then(
            (c) => c.HistoriqueListComponent
          )
      }
    ]
  },
  { path: '**', redirectTo: 'login' }
];
