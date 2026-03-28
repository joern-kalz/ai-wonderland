import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import Main from "../app/_components/main/Main";

describe('Main', () => {
  const originalFetch = global.fetch;
  const originalCreateObjectURL = URL.createObjectURL;
  const originalRevokeObjectURL = URL.revokeObjectURL;

  beforeAll(() => {
    URL.createObjectURL = jest.fn(() => 'blob:url');
    URL.revokeObjectURL = jest.fn();
  });

  afterAll(() => {
    URL.createObjectURL = originalCreateObjectURL;
    URL.revokeObjectURL = originalRevokeObjectURL;
  });

  afterEach(() => {
    global.fetch = originalFetch;
    jest.restoreAllMocks();
  });

  const setupImageFetch = () => {
    const imageBlob = new Blob(['dummy'], { type: 'image/png' });
    return Promise.resolve({ ok: true, blob: async () => imageBlob });
  };

  it('renders loading spinner and then response when user talks', async () => {
    let resolveTalk: (value: unknown) => void = () => { };
    const talkPromise = new Promise((resolve) => {
      resolveTalk = resolve;
    });

    global.fetch = jest.fn((input) => {
      const url = typeof input === 'string' ? input : input.url;
      if (url.endsWith('/image')) {
        return setupImageFetch() as any;
      }
      if (url.endsWith('/talk')) {
        return talkPromise as any;
      }
      return Promise.reject(new Error(`Unexpected fetch: ${url}`));
    }) as unknown as typeof fetch;

    render(<Main sessionToken="test-token" />);

    const input = await screen.findByPlaceholderText('Type what you want to say...');
    fireEvent.change(input, { target: { value: 'Hello' } });
    fireEvent.submit(input.closest('form')!);

    expect(document.querySelector('.animate-spin')).toBeInTheDocument();

    resolveTalk({ ok: true, json: async () => ({ message: 'Hi there', game_end: false }) });
    await waitFor(() => expect(screen.getByText('Hi there')).toBeInTheDocument());
  });

});
