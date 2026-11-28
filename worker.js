export default {
    async fetch(request, env) {
        const url = new URL(request.url);

        if (url.pathname === "/status") {
            return new Response("Backend is working!");
        }

        return env.ASSETS.fetch(request);
    }
};
