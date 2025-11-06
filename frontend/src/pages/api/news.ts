import type { APIRoute } from 'astro';
import { getNews, postNews } from '../../../src/controllers/newsController';

export const GET: APIRoute = async () => {
    try {
        const data = await getNews();
        return new Response(JSON.stringify(data), {
            status: 200,
            headers: { 'Content-Type': 'application/json' },
        });
    } catch (err: any) {
        return new Response(JSON.stringify({ error: err?.message || 'Error' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' },
        });
    }
};

export const POST: APIRoute = async ({ request }) => {
    try {
        const body = await request.json();
        const created = await postNews(body);
        return new Response(JSON.stringify({ noticia: created }), {
            status: 201,
            headers: { 'Content-Type': 'application/json' },
        });
    } catch (err: any) {
        return new Response(JSON.stringify({ error: err?.message || 'Error' }), {
            status: 400,
            headers: { 'Content-Type': 'application/json' },
        });
    }
};


