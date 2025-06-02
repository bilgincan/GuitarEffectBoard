class ApiConnection {
    baseUrl: string;

    constructor(baseUrl: string) {
        this.baseUrl = baseUrl;
    }

    async get(path: string) {
        const urlPath = this.baseUrl + path;
        return await fetch(urlPath, {method: 'GET'});
    }

    async post(path: string, body: any) {
        const urlPath = this.baseUrl + path;
        return await fetch(urlPath, {method: 'POST', body: body});
    }
}