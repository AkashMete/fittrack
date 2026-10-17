import { createFeatureSelector, createSelector } from '@ngrx/store';
import { DietState } from './diet.reducer';

export const selectDietState = createFeatureSelector<DietState>('diet');
export const selectFoods = createSelector(selectDietState, (s) => s.foods);
export const selectFoodsMeta = createSelector(selectDietState, (s) => s.foodsMeta);
export const selectTodayLog = createSelector(selectDietState, (s) => s.todayLog);
export const selectDietLoading = createSelector(selectDietState, (s) => s.loading);
export const selectDietError = createSelector(selectDietState, (s) => s.error);
