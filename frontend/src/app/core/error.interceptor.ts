import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthService } from './auth.service';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const authService = inject(AuthService);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401) {
        authService.logout();
        router.navigate(['/login']);
      } else if (error.status === 403) {
        console.error('Accès refusé:', error.message);
      } else if (error.status === 404) {
        console.error('Ressource non trouvée:', error.message);
      } else if (error.status === 0) {
        console.error('Serveur inaccessible. Vérifiez que le backend est démarré.');
      }
      return throwError(() => error);
    })
  );
};
