import React from 'react';

interface HeaderProps {
  children?: React.ReactNode;
}

export const Header: React.FC<HeaderProps> = ({ children }) => {
  return (
    <div className="p-8 mx-auto space-y-6 text-center rounded-b-xl bg-slate-700">
      <h1 className="text-5xl font-bold text-primary font-pressstart">
        Recipe Robot
      </h1>
      {children}
    </div>
  );
};
