import React from 'react';
import type { IngredientBadgeProps } from '../../types';
import { getBadgeVariant } from '../../utils';

export const IngredientBadge: React.FC<IngredientBadgeProps> = ({
  ingredient,
  index,
  onRemove,
}) => {
  const variant = getBadgeVariant(index);

  return (
    <div className={`items-center badge badge-${variant}`}>
      <span>{ingredient}</span>
      <span
        className="opacity-50 cursor-pointer hover:opacity-100"
        onClick={() => onRemove(index)}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            onRemove(index);
          }
        }}
        aria-label={`Remove ${ingredient}`}
      >
        ×
      </span>
    </div>
  );
};
