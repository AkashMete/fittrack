import { createReducer, on } from '@ngrx/store';
import { FoodItem, DietLog } from './diet.actions';
import * as DietActions from './diet.actions';

export interface DietState {
  foods: FoodItem[];
  foodsMeta: any;
  todayLog: DietLog | null;
  loading: boolean;
  error: string | null;
}

export const initialState: DietState = {
  foods: [],
  foodsMeta: null,
  todayLog: null,
  loading: false,
  error: null,
};

export const dietReducer = createReducer(
  initialState,
  on(DietActions.loadFoods, DietActions.loadTodayLog, DietActions.addLogEntry, (s) => ({ ...s, loading: true, error: null })),
  on(DietActions.loadFoodsSuccess, (s, { foods, meta }) => ({ ...s, foods, foodsMeta: meta, loading: false })),
  on(DietActions.createFoodSuccess, (s, { food }) => ({ ...s, foods: [food, ...s.foods] })),
  on(DietActions.deleteFoodSuccess, (s, { id }) => ({ ...s, foods: s.foods.filter((f) => f.id !== id) })),
  on(DietActions.loadTodayLogSuccess, DietActions.addLogEntrySuccess, DietActions.deleteLogEntrySuccess, (s, { log }) => ({ ...s, todayLog: log, loading: false })),
  on(DietActions.dietError, (s, { error }) => ({ ...s, loading: false, error })),
);
