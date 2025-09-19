import axios, { type AxiosResponse, type AxiosError } from 'axios';
import type { RecipeRequest, RecipeResponse, Food } from '../types';
import { API_CONFIG, API_DEFAULTS } from '../constants';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// API Service Class
class ApiService {
  /**
   * Check if the API is healthy and ready
   */
  async checkHealth(): Promise<boolean> {
    try {
      const response: AxiosResponse = await apiClient.get(API_CONFIG.ENDPOINTS.HEALTH);
      return response.status === 200;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  /**
   * Generate recipes based on ingredients
   */
  async generateRecipes(request: RecipeRequest): Promise<RecipeResponse> {
    try {
      const response: AxiosResponse<RecipeResponse> = await apiClient.post(
        API_CONFIG.ENDPOINTS.RECIPES,
        {
          ingredients: request.ingredients,
          max_recipes: request.max_recipes || API_DEFAULTS.DEFAULT_MAX_RECIPES,
          cuisine_style: request.cuisine_style || API_DEFAULTS.DEFAULT_CUISINE_STYLE,
        }
      );
      return response.data;
    } catch (error) {
      console.error('Recipe generation failed:', error);
      throw new Error('Failed to generate recipes. Please try again.');
    }
  }

  /**
   * Search for food ingredients
   */
  async searchFoods(query: string): Promise<Food[]> {
    try {
      const response: AxiosResponse<Food[]> = await apiClient.get(
        API_CONFIG.ENDPOINTS.FOODS,
        { params: { q: query } }
      );
      return response.data;
    } catch (error) {
      console.error('Food search failed:', error);
      throw new Error('Failed to search foods. Please try again.');
    }
  }
}

// Export singleton instance
export const apiService = new ApiService();

// Export types for error handling
export type ApiError = {
  message: string;
  code?: string;
  status?: number;
};
