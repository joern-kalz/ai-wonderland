describe('config', () => {
    const originalEnv = process.env;

    beforeEach(() => {
        jest.resetModules();
        process.env = { ...originalEnv };
    });

    afterAll(() => {
        process.env = originalEnv;
    });

    it('defaults API_URL to localhost when NEXT_PUBLIC_API_URL is not set', async () => {
        delete process.env.NEXT_PUBLIC_API_URL;

        const { API_URL } = await import('../libs/config');

        expect(API_URL).toBe('http://localhost:8000');
    });

    it('removes the trailing slash from NEXT_PUBLIC_API_URL', async () => {
        process.env.NEXT_PUBLIC_API_URL = 'https://example.com/';

        const { API_URL } = await import('../libs/config');

        expect(API_URL).toBe('https://example.com');
    });

    it('preserves NEXT_PUBLIC_API_URL when there is no trailing slash', async () => {
        process.env.NEXT_PUBLIC_API_URL = 'https://example.com';

        const { API_URL } = await import('../libs/config');

        expect(API_URL).toBe('https://example.com');
    });
});
