import React from 'react';
import type { ApiStatus } from '../../types';
import { UI_MESSAGES } from '../../constants';

interface ApiStatusDisplayProps {
  apiStatus: ApiStatus;
}

export const ApiStatusDisplay: React.FC<ApiStatusDisplayProps> = ({ apiStatus }) => {
  if (apiStatus.isReady) {
    return null; // API is ready, don't show anything
  }

  if (apiStatus.hasFailed) {
    return (
      <div className="text-red-500">
        {UI_MESSAGES.ERROR.API_FAILED}
        <br />
        {UI_MESSAGES.ERROR.API_FAILED_SUBTITLE}
      </div>
    );
  }

  // API is loading
  return (
    <div className="text-red-500">
      <img
        src="https://media.tenor.com/6PA78Ba9-VUAAAAi/zzz-zzzz.gif"
        className="block mx-auto max-w-48"
        alt="Loading animation"
      />
      {UI_MESSAGES.LOADING.API_STARTUP}
      <div className="loading loading-bars loading-lg"></div>
    </div>
  );
};
