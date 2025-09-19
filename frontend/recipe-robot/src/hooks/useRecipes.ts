import { useState } from 'react';
import { apiService } from '../services/api';
import type { UseRecipesReturn, Recipe } from '../types';

export const useRecipes = (): UseRecipesReturn => {
  const [recipes, setRecipes] = useState<Recipe[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const generateRecipes = async (ingredients: string[]) => {
    if (ingredients.length === 0) {
      throw new Error('No ingredients provided');
    }

    setIsLoading(true);
    try {
      const response = await apiService.generateRecipes({ ingredients });
      setRecipes(response.recipes);
    } catch (error) {
      console.error('Failed to generate recipes:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  const clearRecipes = () => {
    setRecipes([]);
  };

  return {
    recipes,
    isLoading,
    generateRecipes,
    clearRecipes,
  };
};
