import { createReducer, on } from '@ngrx/store';
import { AuthUser } from '../../core/auth/auth.service';
import * as AuthActions from './auth.actions';

export interface AuthState {
  user: AuthUser | null;
  accessToken: string | null;
  loading: boolean;
  error: string | null;
}

export const initialState: AuthState = {
  user: null,
  accessToken: null,
  loading: false,
  error: null,
};

export const authReducer = createReducer(
  initialState,
  on(AuthActions.login, AuthActions.register, (state) => ({ ...state, loading: true, error: null })),
  on(AuthActions.loginSuccess, AuthActions.registerSuccess, (state, { user, accessToken }) => ({
    ...state, user, accessToken, loading: false, error: null,
  })),
  on(AuthActions.loginFailure, AuthActions.registerFailure, (state, { error }) => ({
    ...state, loading: false, error,
  })),
  on(AuthActions.logoutSuccess, () => initialState),
  on(AuthActions.loadProfileSuccess, (state, { user }) => ({ ...state, user })),
);
