// API Configuration
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  ENDPOINTS: {
    HEALTH: '/health',
    RECIPES: '/api/v1/recipes/generate',
    FOODS: '/api/v1/foods',
  },
  TIMEOUTS: {
    HEALTH_CHECK: 60000, // 1 minute
    RETRY_INTERVAL: 2000, // 2 seconds
  },
} as const;

// UI Constants
export const BADGE_VARIANTS = [
  'primary',
  'accent',
  'neutral',
  'info',
  'success',
  'warning',
  'error',
] as const;

export const UI_MESSAGES = {
  LOADING: {
    API_STARTUP: 'Waking up the robots...',
    THINKING: 'Robots are thinking real hard...',
  },
  ERROR: {
    API_FAILED: 'The robots could not be roused :(',
    API_FAILED_SUBTITLE: 'Please try again later.',
    GENERIC: 'Something went wrong. Please try again.',
  },
  SUCCESS: {
    RECIPES_TITLE: 'How about some:',
  },
  PLACEHOLDERS: {
    INGREDIENT_INPUT: 'What do you got on hand?',
    INGREDIENT_INPUT_MORE: 'Anything else?',
  },
  BUTTONS: {
    SEND_IT: 'Send It',
    TRY_AGAIN: 'Try Again',
    CLEAR: 'Clear Ingredients',
  },
} as const;

// App Configuration
export const APP_CONFIG = {
  MIN_INGREDIENTS_FOR_SUBMIT: 3,
  DEFAULT_MAX_RECIPES: 3,
  DEFAULT_CUISINE_STYLE: 'any',
} as const;

// Add to API_CONFIG for easier access
export const API_DEFAULTS = {
  DEFAULT_MAX_RECIPES: 3,
  DEFAULT_CUISINE_STYLE: 'any',
} as const;
