import { render, screen, fireEvent } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import { IngredientBadge } from '../IngredientBadge';

describe('IngredientBadge', () => {
  it('renders ingredient name', () => {
    const mockOnRemove = vi.fn();

    render(
      <IngredientBadge
        ingredient="tomato"
        index={0}
        onRemove={mockOnRemove}
      />
    );

    expect(screen.getByText('tomato')).toBeInTheDocument();
  });

  it('calls onRemove when remove button is clicked', () => {
    const mockOnRemove = vi.fn();

    render(
      <IngredientBadge
        ingredient="tomato"
        index={0}
        onRemove={mockOnRemove}
      />
    );

    const removeButton = screen.getByRole('button');
    fireEvent.click(removeButton);

    expect(mockOnRemove).toHaveBeenCalledWith(0);
  });

  it('calls onRemove when Enter key is pressed on remove button', () => {
    const mockOnRemove = vi.fn();

    render(
      <IngredientBadge
        ingredient="tomato"
        index={0}
        onRemove={mockOnRemove}
      />
    );

    const removeButton = screen.getByRole('button');
    fireEvent.keyDown(removeButton, { key: 'Enter' });

    expect(mockOnRemove).toHaveBeenCalledWith(0);
  });

  it('applies correct badge variant based on index', () => {
    const mockOnRemove = vi.fn();

    const { container } = render(
      <IngredientBadge
        ingredient="tomato"
        index={0}
        onRemove={mockOnRemove}
      />
    );

    const badge = container.querySelector('.badge');
    expect(badge).toHaveClass('badge-primary');
  });
});
