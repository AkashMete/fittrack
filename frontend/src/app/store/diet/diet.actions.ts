import { createAction, props } from '@ngrx/store';

export interface FoodItem {
  id: string;
  name: string;
  brand?: string;
  category?: string;
  calories_per_100g: number;
  protein_per_100g: number;
  carbs_per_100g: number;
  fat_per_100g: number;
  fiber_per_100g?: number;
  sugar_per_100g?: number;
  default_serving_g: number;
  serving_unit: string;
  tags?: string[];
  is_global: boolean;
}

export interface DietLogEntry {
  entry_id: string;
  food_item_id: string;
  food_name: string;
  quantity_g: number;
  meal_type: string;
  calories: number;
  protein_g: number;
  carbs_g: number;
  fat_g: number;
  logged_at: string;
}

export interface DietLog {
  id: string;
  date: string;
  entries: DietLogEntry[];
  total_calories: number;
  total_protein_g: number;
  total_carbs_g: number;
  total_fat_g: number;
  notes?: string;
}

// Foods
export const loadFoods = createAction('[Diet] Load Foods', props<{ q?: string; category?: string; page?: number }>());
export const loadFoodsSuccess = createAction('[Diet] Load Foods Success', props<{ foods: FoodItem[]; meta: any }>());
export const loadFoodsFailure = createAction('[Diet] Load Foods Failure', props<{ error: string }>());
export const createFood = createAction('[Diet] Create Food', props<{ payload: Partial<FoodItem> }>());
export const createFoodSuccess = createAction('[Diet] Create Food Success', props<{ food: FoodItem }>());
export const deleteFood = createAction('[Diet] Delete Food', props<{ id: string }>());
export const deleteFoodSuccess = createAction('[Diet] Delete Food Success', props<{ id: string }>());

// Daily log
export const loadTodayLog = createAction('[Diet] Load Today Log', props<{ date: string }>());
export const loadTodayLogSuccess = createAction('[Diet] Load Today Log Success', props<{ log: DietLog }>());
export const addLogEntry = createAction('[Diet] Add Log Entry', props<{ date: string; payload: any }>());
export const addLogEntrySuccess = createAction('[Diet] Add Log Entry Success', props<{ log: DietLog }>());
export const deleteLogEntry = createAction('[Diet] Delete Log Entry', props<{ date: string; entryId: string }>());
export const deleteLogEntrySuccess = createAction('[Diet] Delete Log Entry Success', props<{ log: DietLog }>());
export const dietError = createAction('[Diet] Error', props<{ error: string }>());
