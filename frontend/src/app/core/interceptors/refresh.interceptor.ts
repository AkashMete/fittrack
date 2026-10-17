import {
  HttpInterceptorFn,
  HttpRequest,
  HttpHandlerFn,
  HttpErrorResponse,
} from '@angular/common/http';
import { inject } from '@angular/core';
import { catchError, switchMap, throwError } from 'rxjs';
import { AuthService } from '../auth/auth.service';

// On 401, attempts one silent token refresh then retries the original request.
// If the refresh also fails, clears the session and re-throws.
export const refreshInterceptor: HttpInterceptorFn = (req: HttpRequest<unknown>, next: HttpHandlerFn) => {
  const auth = inject(AuthService);

  return next(req).pipe(
    catchError((err: HttpErrorResponse) => {
      // Only intercept 401s that are NOT the refresh or login endpoints themselves
      const isAuthEndpoint = req.url.includes('/auth/refresh') || req.url.includes('/auth/login');
      if (err.status === 401 && !isAuthEndpoint) {
        return auth.refresh().pipe(
          switchMap(() => {
            // Retry with the new token (jwtInterceptor will attach it)
            return next(req.clone());
          }),
          catchError((refreshErr) => {
            auth.clearSession();
            return throwError(() => refreshErr);
          })
        );
      }
      return throwError(() => err);
    })
  );
};
