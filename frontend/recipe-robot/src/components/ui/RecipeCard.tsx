import React from 'react';
import type { RecipeCardProps } from '../../types';

export const RecipeCard: React.FC<RecipeCardProps> = ({
  recipe,
  isOpen = false,
}) => {
  return (
    <div className="border collapse collapse-arrow join-item border-base-300">
      <input
        type="radio"
        name="recipe-accordion"
        defaultChecked={isOpen}
      />
      <div className="font-semibold collapse-title">
        {recipe.recipe_name}
      </div>
      <div className="space-y-2 text-xs leading-relaxed collapse-content">
        <h3 className="text-accent">Ingredients</h3>
        <ul className="list-disc list-inside text-white">
          {recipe.ingredients.map((ingredient, index) => (
            <li key={`${recipe.recipe_name}-ingredient-${index}`}>
              {ingredient}
            </li>
          ))}
        </ul>
        <h3 className="text-accent">Instructions</h3>
        <p className="text-white">{recipe.instructions}</p>
      </div>
    </div>
  );
};
