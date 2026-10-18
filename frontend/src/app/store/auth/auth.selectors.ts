import { createSelector, createFeatureSelector } from '@ngrx/store';
import { AuthState } from './auth.reducer';

export const selectAuthState = createFeatureSelector<AuthState>('auth');
export const selectUser = createSelector(selectAuthState, (s) => s.user);
export const selectAccessToken = createSelector(selectAuthState, (s) => s.accessToken);
export const selectIsLoggedIn = createSelector(selectAuthState, (s) => !!s.accessToken);
export const selectAuthLoading = createSelector(selectAuthState, (s) => s.loading);
export const selectAuthError = createSelector(selectAuthState, (s) => s.error);
