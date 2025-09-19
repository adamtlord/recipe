import React from 'react';
import type { IngredientInputProps } from '../../types';
import { isEnterKey, isShiftEnterKey, validateIngredient } from '../../utils';
import { UI_MESSAGES } from '../../constants';

export const IngredientInput: React.FC<IngredientInputProps> = ({
  onAdd,
  onSubmit,
  placeholder = UI_MESSAGES.PLACEHOLDERS.INGREDIENT_INPUT,
}) => {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (isShiftEnterKey(e)) {
      e.preventDefault();
      onSubmit();
      return;
    }

    if (isEnterKey(e)) {
      e.preventDefault();
      const value = e.currentTarget.value;

      if (validateIngredient(value)) {
        onAdd(value);
        e.currentTarget.value = '';
      }
    }
  };

  return (
    <input
      name="ingredient"
      type="text"
      className="w-full rounded-xl join input input-xl input-primary"
      placeholder={placeholder}
      onKeyDown={handleKeyDown}
      aria-label="Add ingredient"
    />
  );
};
