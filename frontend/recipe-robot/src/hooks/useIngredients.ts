import { useState } from 'react';
import type { UseIngredientsReturn } from '../types';

export const useIngredients = (): UseIngredientsReturn => {
  const [ingredients, setIngredients] = useState<string[]>([]);

  const addIngredient = (ingredient: string) => {
    const trimmedIngredient = ingredient.trim();
    if (trimmedIngredient && !ingredients.includes(trimmedIngredient)) {
      setIngredients(prev => [...prev, trimmedIngredient]);
    }
  };

  const removeIngredient = (index: number) => {
    setIngredients(prev => prev.filter((_, i) => i !== index));
  };

  const clearIngredients = () => {
    setIngredients([]);
  };

  return {
    ingredients,
    addIngredient,
    removeIngredient,
    clearIngredients,
  };
};
