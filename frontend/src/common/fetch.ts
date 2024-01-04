interface Request {
    url: string;
    body: any;
    method: string;
}

export const request = async <T>(arg: Request | string):Promise<T> => {
    const baseURL = window.location.hostname
    if (typeof(arg) ==  'string') {
        const apiURL = arg.startsWith('/')? arg : `/${arg}`;
        return await(
          await fetch(`http://${baseURL}:8000${apiURL}`)
        ).json() as T;
    }

    const apiURL = arg.url.startsWith('/')? arg.url : `/${arg.url}`;
    const result = await fetch(
        `http://${baseURL}:8000${apiURL}`,
        {
            headers: {
                'Content-Type': 'application/json'
            },
            method: arg.method,
            body: JSON.stringify(arg.body)
        }
    )
    return (await result.json()) as T;
}