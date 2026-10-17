import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter, withComponentInputBinding } from '@angular/router';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideStore } from '@ngrx/store';
import { provideEffects } from '@ngrx/effects';
import { provideStoreDevtools } from '@ngrx/store-devtools';
import { routes } from './app.routes';
import { jwtInterceptor } from './core/interceptors/jwt.interceptor';
import { refreshInterceptor } from './core/interceptors/refresh.interceptor';
import { authReducer } from './store/auth/auth.reducer';
import { dietReducer } from './store/diet/diet.reducer';
import { AuthEffects } from './store/auth/auth.effects';
import { DietEffects } from './store/diet/diet.effects';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes, withComponentInputBinding()),
    provideHttpClient(withInterceptors([jwtInterceptor, refreshInterceptor])),
    provideStore({ auth: authReducer, diet: dietReducer }),
    provideEffects([AuthEffects, DietEffects]),
    provideStoreDevtools({ maxAge: 25, logOnly: false }),
  ],
};
