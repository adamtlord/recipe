import React from 'react';
import { getBadgeVariant } from '../../utils';

interface LoadingSpinnerProps {
  variant?: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  variant = 'primary',
  size = 'md',
  className = '',
}) => {
  const sizeClasses = {
    sm: 'loading-sm',
    md: 'loading-md',
    lg: 'loading-lg',
  };

  return (
    <span
      className={`loading loading-spinner text-${variant} ${sizeClasses[size]} ${className}`}
    />
  );
};

interface LoadingSpinnersProps {
  count: number;
  className?: string;
}

export const LoadingSpinners: React.FC<LoadingSpinnersProps> = ({
  count,
  className = '',
}) => {
  return (
    <div className={`flex flex-wrap gap-2 justify-center ${className}`}>
      {Array.from({ length: count }).map((_, i) => (
        <LoadingSpinner
          key={i}
          variant={getBadgeVariant(i)}
        />
      ))}
    </div>
  );
};
