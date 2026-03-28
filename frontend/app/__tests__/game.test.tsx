import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Game from '../app/_components/Game';
import { sendStartGame } from '../libs/sendStartGame';
import { useSearchParams } from 'next/navigation';

jest.mock('next/navigation', () => ({
    useSearchParams: jest.fn(),
}));

jest.mock('../libs/sendStartGame', () => ({
    sendStartGame: jest.fn(),
}));

jest.mock('../app/_components/main/Main', () => ({
    __esModule: true,
    default: ({ sessionToken }: { sessionToken: string }) => (
        <div data-testid="main">Main {sessionToken}</div>
    ),
}));

describe('Game', () => {
    const useSearchParamsMock = useSearchParams as jest.MockedFunction<typeof useSearchParams>;
    const sendStartGameMock = sendStartGame as jest.MockedFunction<typeof sendStartGame>;

    beforeEach(() => {
        jest.clearAllMocks();
    });

    it('renders Menu when there is no session_token in the query string', () => {
        useSearchParamsMock.mockReturnValue({ get: () => null } as any);

        render(<Game />);

        expect(screen.getByRole('button', { name: /enter wonderland/i })).toBeInTheDocument();
    });

    it('renders Main when session_token is present in the query string', () => {
        useSearchParamsMock.mockReturnValue({ get: () => 'abc123' } as any);

        render(<Game />);

        expect(screen.getByTestId('main')).toHaveTextContent('Main abc123');
    });

    it('calls sendStartGame and transitions from Menu to Main', async () => {
        useSearchParamsMock.mockReturnValue({ get: () => null } as any);
        sendStartGameMock.mockResolvedValue({ session_token: 'token-xyz' });

        render(<Game />);

        const startButton = screen.getByRole('button', { name: /enter wonderland/i });
        fireEvent.click(startButton);

        await waitFor(() => expect(sendStartGameMock).toHaveBeenCalledTimes(1));
        expect(await screen.findByTestId('main')).toHaveTextContent('Main token-xyz');
    });
});
