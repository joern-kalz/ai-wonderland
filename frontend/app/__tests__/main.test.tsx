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

  it('renders loading spinner and then new travel error when travel fails', async () => {
    let resolveTravel: (value: unknown) => void = () => { };
    const travelPromise = new Promise((resolve) => {
      resolveTravel = resolve;
    });

    global.fetch = jest.fn((input) => {
      const url = typeof input === 'string' ? input : input.url;
      if (url.endsWith('/image')) {
        return setupImageFetch() as any;
      }
      if (url.endsWith('/travel')) {
        return travelPromise as any;
      }
      return Promise.reject(new Error(`Unexpected fetch: ${url}`));
    }) as unknown as typeof fetch;

    render(<Main sessionToken="test-token" />);

    const travelButton = await screen.findByRole('button', { name: /Travel/i });
    fireEvent.click(travelButton);

    const travelInput = await screen.findByPlaceholderText('Type the name of the character you want to travel to...');
    fireEvent.change(travelInput, { target: { value: 'Alice' } });
    fireEvent.submit(travelInput.closest('form')!);

    expect(document.querySelector('.animate-spin')).toBeInTheDocument();

    resolveTravel({ ok: false, status: 400, statusText: 'Bad Request' });
    await waitFor(() => expect(screen.getByText('"Alice" is not the name of a character. Please enter a character name')).toBeInTheDocument());
    expect(document.querySelector('.animate-spin')).not.toBeInTheDocument();
  });

  it('renders "The End" when talk ends game', async () => {
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

    resolveTalk({ ok: true, json: async () => ({ message: 'Bye', game_end: true }) });
    await waitFor(() => expect(screen.getByText('The End')).toBeInTheDocument());
  });

  it('renders loading spinner and then new image when travel succeeds', async () => {
    let resolveTravel: (value: unknown) => void = () => { };
    const travelPromise = new Promise((resolve) => {
      resolveTravel = resolve;
    });

    const createObjectURLMock = URL.createObjectURL as jest.Mock;
    let imageIndex = 0;
    createObjectURLMock.mockReset();
    createObjectURLMock.mockImplementation(() => `blob:url-${++imageIndex}`);

    global.fetch = jest.fn((input) => {
      const url = typeof input === 'string' ? input : input.url;
      if (url.endsWith('/image')) {
        return setupImageFetch() as any;
      }
      if (url.endsWith('/travel')) {
        return travelPromise as any;
      }
      return Promise.reject(new Error(`Unexpected fetch: ${url}`));
    }) as unknown as typeof fetch;

    render(<Main sessionToken="test-token" />);

    const firstImage = await screen.findByRole('img', { name: /Fetched Blob/i });
    await waitFor(() => expect(firstImage).toHaveAttribute('src', 'blob:url-1'));

    const travelButton = await screen.findByRole('button', { name: /Travel/i });
    fireEvent.click(travelButton);

    const travelInput = await screen.findByPlaceholderText('Type the name of the character you want to travel to...');
    fireEvent.change(travelInput, { target: { value: 'Alice' } });
    fireEvent.submit(travelInput.closest('form')!);

    expect(document.querySelector('.animate-spin')).toBeInTheDocument();

    resolveTravel({ ok: true });
    await waitFor(() => expect(screen.getByRole('img', { name: /Fetched Blob/i })).toHaveAttribute('src', 'blob:url-2'));
    expect(document.querySelector('.animate-spin')).not.toBeInTheDocument();
  });

  it('renders "Type what you want to say..." when switching to travel and then back to talk', async () => {
    global.fetch = jest.fn((input) => {
      const url = typeof input === 'string' ? input : input.url;
      if (url.endsWith('/image')) {
        return setupImageFetch() as any;
      }
      return Promise.reject(new Error(`Unexpected fetch: ${url}`));
    }) as unknown as typeof fetch;

    render(<Main sessionToken="test-token" />);

    const travelButton = await screen.findByRole('button', { name: /Travel/i });
    fireEvent.click(travelButton);

    await screen.findByPlaceholderText('Type the name of the character you want to travel to...');

    const talkButton = screen.getByRole('button', { name: /Talk/i });
    fireEvent.click(talkButton);

    await screen.findByPlaceholderText('Type what you want to say...');
  });

});
