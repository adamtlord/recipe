import React from 'react';
import { Tooltip } from 'react-tooltip';
import { IngredientInput } from '@/components/ui/IngredientInput';
import { IngredientBadge } from '@/components/ui/IngredientBadge';
import type { UseIngredientsReturn } from '@/types';
import { UI_MESSAGES, APP_CONFIG } from '@/constants';
import { generateKey } from '@/utils';

interface IngredientFormProps {
  ingredients: UseIngredientsReturn['ingredients'];
  onAddIngredient: UseIngredientsReturn['addIngredient'];
  onRemoveIngredient: UseIngredientsReturn['removeIngredient'];
  onClearIngredients: UseIngredientsReturn['clearIngredients'];
  onSubmit: () => void;
}

export const IngredientForm: React.FC<IngredientFormProps> = ({
  ingredients,
  onAddIngredient,
  onRemoveIngredient,
  onClearIngredients,
  onSubmit,
}) => {
  const showSubmitButton = ingredients.length >= APP_CONFIG.MIN_INGREDIENTS_FOR_SUBMIT;
  const placeholder = ingredients.length > 2
    ? UI_MESSAGES.PLACEHOLDERS.INGREDIENT_INPUT_MORE
    : UI_MESSAGES.PLACEHOLDERS.INGREDIENT_INPUT;

  return (
    <>
      <div className="space-x-4">
        <IngredientInput
          onAdd={onAddIngredient}
          onSubmit={onSubmit}
          placeholder={placeholder}
        />
      </div>

      {ingredients.length > 0 && (
        <div className="flex relative flex-wrap gap-2 justify-center p-6 border-2 border-dashed border-secondary">
          {ingredients.map((ingredient, i) => (
            <IngredientBadge
              key={generateKey('ingredient', i, ingredient)}
              ingredient={ingredient}
              index={i}
              onRemove={onRemoveIngredient}
            />
          ))}
          <div className="absolute top-0 right-0 text-xs">
            <button
              className="p-1 rounded-none btn btn-ghost btn-square"
              data-tooltip-id="clear-ingredients"
              data-tooltip-place="bottom"
              data-tooltip-delay-show={500}
              onClick={onClearIngredients}
              aria-label={UI_MESSAGES.BUTTONS.CLEAR}
            >
              &times;
            </button>
            <Tooltip id="clear-ingredients" content={UI_MESSAGES.BUTTONS.CLEAR} />
          </div>
        </div>
      )}

      {showSubmitButton && (
        <button
          className="rounded-full animate-pulse btn btn-secondary btn-xl text-primary font-pressstart"
          onClick={onSubmit}
        >
          {UI_MESSAGES.BUTTONS.SEND_IT}
        </button>
      )}
    </>
  );
};
