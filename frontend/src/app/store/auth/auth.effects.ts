import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { of } from 'rxjs';
import { map, switchMap, catchError, tap } from 'rxjs/operators';
import { AuthService } from '../../core/auth/auth.service';
import * as AuthActions from './auth.actions';

@Injectable()
export class AuthEffects {
  constructor(
    private actions$: Actions,
    private authService: AuthService,
    private router: Router,
  ) {}

  login$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.login),
      switchMap(({ email, password }) =>
        this.authService.login(email, password).pipe(
          map((res: any) => AuthActions.loginSuccess({ user: res.data.user, accessToken: res.data.access_token })),
          catchError((err) => of(AuthActions.loginFailure({ error: err.error?.error?.message ?? 'Login failed' })))
        )
      )
    )
  );

  loginSuccess$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.loginSuccess, AuthActions.registerSuccess),
      tap(() => this.router.navigate(['/dashboard']))
    ),
    { dispatch: false }
  );

  register$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.register),
      switchMap((payload) =>
        this.authService.register(payload).pipe(
          map((res: any) => AuthActions.registerSuccess({ user: res.data.user, accessToken: res.data.access_token })),
          catchError((err) => of(AuthActions.registerFailure({ error: err.error?.error?.message ?? 'Registration failed' })))
        )
      )
    )
  );

  logout$ = createEffect(() =>
    this.actions$.pipe(
      ofType(AuthActions.logout),
      tap(() => this.authService.logout()),
      map(() => AuthActions.logoutSuccess())
    )
  );
}
