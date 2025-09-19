import React from 'react';
import type { Recipe } from '../../types';
import { RecipeCard } from './RecipeCard';
import { UI_MESSAGES } from '../../constants';

interface RecipeListProps {
  recipes: Recipe[];
  onTryAgain: () => void;
}

export const RecipeList: React.FC<RecipeListProps> = ({
  recipes,
  onTryAgain,
}) => {
  if (recipes.length === 0) {
    return null;
  }

  return (
    <div className="mt-6 space-y-4">
      <h2 className="text-2xl text-center text-secondary">
        {UI_MESSAGES.SUCCESS.RECIPES_TITLE}
      </h2>
      <div className="join join-vertical">
        {recipes.map((recipe) => (
          <RecipeCard
            key={recipe.recipe_name}
            recipe={recipe}
          />
        ))}
      </div>
      <div className="flex justify-center my-4">
        <button
          className="btn btn-primary btn-sm btn-outline"
          onClick={onTryAgain}
        >
          {UI_MESSAGES.BUTTONS.TRY_AGAIN}
        </button>
      </div>
    </div>
  );
};
