import { createAction, props } from '@ngrx/store';
import { AuthUser } from '../../core/auth/auth.service';

export const login = createAction('[Auth] Login', props<{ email: string; password: string }>());
export const loginSuccess = createAction('[Auth] Login Success', props<{ user: AuthUser; accessToken: string }>());
export const loginFailure = createAction('[Auth] Login Failure', props<{ error: string }>());

export const register = createAction('[Auth] Register', props<{ email: string; password: string; first_name?: string }>());
export const registerSuccess = createAction('[Auth] Register Success', props<{ user: AuthUser; accessToken: string }>());
export const registerFailure = createAction('[Auth] Register Failure', props<{ error: string }>());

export const logout = createAction('[Auth] Logout');
export const logoutSuccess = createAction('[Auth] Logout Success');

export const loadProfile = createAction('[Auth] Load Profile');
export const loadProfileSuccess = createAction('[Auth] Load Profile Success', props<{ user: AuthUser }>());
