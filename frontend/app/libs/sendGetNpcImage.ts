export async function sendGetNpcImage(sessionToken: string): Promise<Blob> {
    const response = await fetch('https://picsum.photos/seed/picsum/1024/1024', {
        // headers: {
        //     'x-session-token': `${sessionToken}`,
        // }
    });

    return response.blob();
}