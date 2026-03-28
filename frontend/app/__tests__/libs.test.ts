import { API_URL } from "@/libs/config";
import { sendGetNpcImage } from "@/libs/sendGetNpcImage";
import { sendStartGame } from "@/libs/sendStartGame";
import { sendTalk } from "@/libs/sendTalk";
import { sendTravel } from "@/libs/sendTravel";

describe('frontend library helpers', () => {
    const originalFetch = global.fetch;
    const mockFetch = jest.fn();

    beforeEach(() => {
        (global as any).fetch = mockFetch;
        mockFetch.mockReset();
    });

    afterAll(() => {
        (global as any).fetch = originalFetch;
    });

    it('sendStartGame returns session_token when the API succeeds', async () => {
        mockFetch.mockResolvedValue({
            ok: true,
            json: jest.fn().mockResolvedValue({ session_token: 'abc123' }),
        });

        const response = await sendStartGame();

        expect(response).toEqual({ session_token: 'abc123' });
        expect(mockFetch).toHaveBeenCalledWith(`${API_URL}/start`, { method: 'POST' });
    });

    it('sendStartGame throws when the API fails', async () => {
        mockFetch.mockResolvedValue({ ok: false, statusText: 'Server error' });

        await expect(sendStartGame()).rejects.toThrow('Failed to start game: Server error');
    });

    it('sendGetNpcImage returns a blob when the API succeeds', async () => {
        const blob = new Blob(['data'], { type: 'image/png' });

        mockFetch.mockResolvedValue({
            ok: true,
            blob: jest.fn().mockResolvedValue(blob),
        });

        const result = await sendGetNpcImage('token-1');

        expect(result).toBe(blob);
        expect(mockFetch).toHaveBeenCalledWith(`${API_URL}/image`, {
            headers: {
                'x-session-token': 'token-1',
            },
        });
    });

    it('sendGetNpcImage throws when the API response is not ok', async () => {
        mockFetch.mockResolvedValue({ ok: false, statusText: 'Not found' });

        await expect(sendGetNpcImage('token-2')).rejects.toThrow('Failed to get npc image: Not found');
    });

    it('sendTalk returns parsed JSON when the API succeeds', async () => {
        mockFetch.mockResolvedValue({
            ok: true,
            json: jest.fn().mockResolvedValue({ message: 'hello', game_end: false }),
        });

        const response = await sendTalk({ sessionToken: 'token-3', message: 'hi there' });

        expect(response).toEqual({ message: 'hello', game_end: false });
        expect(mockFetch).toHaveBeenCalledWith(`${API_URL}/talk`, {
            method: 'POST',
            body: JSON.stringify({ message: 'hi there' }),
            headers: {
                'x-session-token': 'token-3',
                'Content-Type': 'application/json',
            },
        });
    });

    it('sendTalk throws when the API response is not ok', async () => {
        mockFetch.mockResolvedValue({ ok: false, statusText: 'Bad request' });

        await expect(sendTalk({ sessionToken: 'token-4', message: 'test' })).rejects.toThrow(
            'Failed to talk: Bad request'
        );
    });

    it('sendTravel returns not_a_character_error on status 400', async () => {
        mockFetch.mockResolvedValue({ status: 400, ok: false });

        const response = await sendTravel({ sessionToken: 'token-5', destination: 'bob' });

        expect(response).toEqual({ type: 'not_a_character_error' });
        expect(mockFetch).toHaveBeenCalledWith(`${API_URL}/travel`, {
            method: 'POST',
            body: JSON.stringify({ npc: 'bob' }),
            headers: {
                'x-session-token': 'token-5',
                'Content-Type': 'application/json',
            },
        });
    });

    it('sendTravel returns success when the API succeeds', async () => {
        mockFetch.mockResolvedValue({ status: 200, ok: true });

        const response = await sendTravel({ sessionToken: 'token-6', destination: 'alice' });

        expect(response).toEqual({ type: 'success' });
    });

    it('sendTravel throws when the API returns a non-ok non-400 status', async () => {
        mockFetch.mockResolvedValue({ status: 500, ok: false, statusText: 'Server failure' });

        await expect(sendTravel({ sessionToken: 'token-7', destination: 'carl' })).rejects.toThrow(
            'Failed to travel: Server failure'
        );
    });
});
