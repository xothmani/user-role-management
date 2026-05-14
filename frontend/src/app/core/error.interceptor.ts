import { HttpInterceptorFn, HttpErrorResponse } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';
import { AuthService } from './auth.service';
import { ToastService } from './toast.service';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const authService = inject(AuthService);
  const toastService = inject(ToastService);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      if (error.status === 401 && req.url.includes('/api/auth/')) {
        authService.logout();
        router.navigate(['/login']);
      } else {
        toastService.error(toErrorMessage(error));
      }
      return throwError(() => error);
    })
  );
};

function toErrorMessage(error: HttpErrorResponse): string {
  switch (error.status) {
    case 0:   return 'Serveur inaccessible. Vérifiez que le backend est démarré.';
    case 400: return error.error?.message || 'Requête invalide.';
    case 401: return 'Session expirée ou non authentifié. Veuillez vous reconnecter.';
    case 403: return 'Accès refusé. Vous ne disposez pas des droits nécessaires.';
    case 409: return error.error?.message || 'Conflit : cette ressource est encore utilisée.';
    case 404: return 'Ressource non trouvée.';
    case 500: return 'Erreur serveur interne. Veuillez réessayer.';
    default:  return `Erreur inattendue (${error.status}).`;
  }
}
