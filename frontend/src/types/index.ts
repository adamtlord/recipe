// Core data types
export interface Recipe {
  recipe_name: string;
  ingredients: string[];
  instructions: string;
}

export interface RecipeRequest {
  ingredients: string[];
  max_recipes?: number;
  cuisine_style?: string;
}

export interface RecipeResponse {
  recipes: Recipe[];
}

export interface Food {
  id: number;
  name: string;
}

// UI state types
export interface ApiStatus {
  isReady: boolean;
  isLoading: boolean;
  hasFailed: boolean;
  error?: string;
}

export interface AppState {
  ingredients: string[];
  recipes: Recipe[];
  isLoading: boolean;
  apiStatus: ApiStatus;
}

// Component prop types
export interface IngredientBadgeProps {
  ingredient: string;
  index: number;
  onRemove: (index: number) => void;
}

export interface RecipeCardProps {
  recipe: Recipe;
  isOpen?: boolean;
}

export interface IngredientInputProps {
  onAdd: (ingredient: string) => void;
  onSubmit: () => void;
  placeholder?: string;
}

// Hook return types
export interface UseApiStatusReturn {
  apiStatus: ApiStatus;
  checkApiHealth: () => Promise<void>;
}

export interface UseIngredientsReturn {
  ingredients: string[];
  addIngredient: (ingredient: string) => void;
  removeIngredient: (index: number) => void;
  clearIngredients: () => void;
}

export interface UseRecipesReturn {
  recipes: Recipe[];
  isLoading: boolean;
  generateRecipes: (ingredients: string[]) => Promise<void>;
  clearRecipes: () => void;
}
