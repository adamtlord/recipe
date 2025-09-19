import React from 'react';
import { LoadingSpinners } from '../ui/LoadingSpinner';
import { UI_MESSAGES } from '../../constants';

interface LoadingDisplayProps {
  ingredientCount: number;
}

export const LoadingDisplay: React.FC<LoadingDisplayProps> = ({ ingredientCount }) => {
  return (
    <div className="mt-6 space-y-2">
      <h3 className="text-center animate-pulse text-secondary">
        {UI_MESSAGES.LOADING.THINKING}
      </h3>
      <LoadingSpinners count={ingredientCount} />
    </div>
  );
};
