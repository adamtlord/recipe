import { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import type { ApiStatus } from '../types';
import { API_CONFIG } from '../constants';

export const useApiStatus = () => {
  const [apiStatus, setApiStatus] = useState<ApiStatus>({
    isReady: false,
    isLoading: true,
    hasFailed: false,
  });

  const checkApiHealth = async (): Promise<boolean> => {
    try {
      const isHealthy = await apiService.checkHealth();
      return isHealthy;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  };

  useEffect(() => {
    let timeoutId: number | null = null;
    let isCancelled = false;

    const startTime = Date.now();
    const maxDuration = API_CONFIG.TIMEOUTS.HEALTH_CHECK;
    const retryInterval = API_CONFIG.TIMEOUTS.RETRY_INTERVAL;

    const retryCheck = async () => {
      if (isCancelled) return;

      const isReady = await checkApiHealth();

      if (isReady) {
        setApiStatus({
          isReady: true,
          isLoading: false,
          hasFailed: false,
        });
        return; // API is ready, stop retrying
      }

      const elapsed = Date.now() - startTime;
      if (elapsed < maxDuration && !isCancelled) {
        // Schedule next retry
        timeoutId = setTimeout(retryCheck, retryInterval);
      } else if (!isCancelled) {
        // Timeout reached, API failed to start
        setApiStatus({
          isReady: false,
          isLoading: false,
          hasFailed: true,
          error: 'API failed to start within timeout period',
        });
      }
    };

    // Start the initial check
    retryCheck();

    // Cleanup function
    return () => {
      isCancelled = true;
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, []);

  return { apiStatus, checkApiHealth };
};
