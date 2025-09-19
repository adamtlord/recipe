import { BADGE_VARIANTS } from '../constants';

/**
 * Get a badge variant based on index for consistent styling
 */
export const getBadgeVariant = (index: number): string => {
  return BADGE_VARIANTS[index % BADGE_VARIANTS.length];
};

/**
 * Validate ingredient input
 */
export const validateIngredient = (ingredient: string): boolean => {
  const trimmed = ingredient.trim();
  return trimmed.length > 0 && trimmed.length <= 100;
};

/**
 * Format ingredient name for display
 */
export const formatIngredient = (ingredient: string): string => {
  return ingredient.trim().toLowerCase().replace(/\s+/g, ' ');
};

/**
 * Check if Enter key was pressed
 */
export const isEnterKey = (event: React.KeyboardEvent): boolean => {
  return event.key === 'Enter';
};

/**
 * Check if Shift + Enter was pressed
 */
export const isShiftEnterKey = (event: React.KeyboardEvent): boolean => {
  return event.key === 'Enter' && event.shiftKey;
};

/**
 * Debounce function for search inputs
 */
export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  delay: number
): ((...args: Parameters<T>) => void) => {
  let timeoutId: number;
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
};

/**
 * Generate unique key for React elements
 */
export const generateKey = (prefix: string, index: number, item: string): string => {
  return `${prefix}-${index}-${item}`;
};
