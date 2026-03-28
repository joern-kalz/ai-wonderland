import { render, screen, fireEvent } from "@testing-library/react";
import Toggle, { Choice } from "../app/_components/main/Toggle";

describe('Toggle', () => {
    it('renders each choice button', () => {
        const choices: Choice[] = [
            { children: 'Choice 1', onClick: jest.fn(), active: true },
            { children: 'Choice 2', onClick: jest.fn(), active: false },
        ];

        render(<Toggle choices={choices} />);

        expect(screen.getByRole('button', { name: /Choice 1/i })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /Choice 2/i })).toBeInTheDocument();
    });

    it('calls the onClick callback when a button is clicked', () => {
        const choice1Handler = jest.fn();
        const choice2Handler = jest.fn();
        const choices: Choice[] = [
            { children: 'Choice 1', onClick: choice1Handler, active: true },
            { children: 'Choice 2', onClick: choice2Handler, active: false },
        ];

        render(<Toggle choices={choices} />);

        fireEvent.click(screen.getByRole('button', { name: /Choice 2/i }));
        expect(choice2Handler).toHaveBeenCalledTimes(1);
        expect(choice1Handler).not.toHaveBeenCalled();
    });

    it('applies active styles to the active choice', () => {
        const choices: Choice[] = [
            { children: 'Choice 1', onClick: jest.fn(), active: true },
            { children: 'Choice 2', onClick: jest.fn(), active: false },
            { children: 'Choice 3', onClick: jest.fn(), active: false },
        ];

        render(<Toggle choices={choices} />);

        expect(screen.getByRole('button', { name: /Choice 1/i })).toHaveClass('font-bold');
        expect(screen.getByRole('button', { name: /Choice 2/i })).not.toHaveClass('font-bold');
        expect(screen.getByRole('button', { name: /Choice 3/i })).not.toHaveClass('font-bold');
    });
});
