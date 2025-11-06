import type { APIRoute } from 'astro';
import { getCommentsByNewsId, postComment } from '../../controllers/commentController';

export const prerender = false;

export const GET: APIRoute = async ({ url }) => {
	try {
		const noticiaId = url.searchParams.get('noticiaId');
		if (!noticiaId) {
			return new Response(JSON.stringify({ error: 'noticiaId requerido' }), {
				status: 400,
				headers: { 'Content-Type': 'application/json' },
			});
		}
		const comments = await getCommentsByNewsId(Number(noticiaId));
		return new Response(JSON.stringify(comments), {
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
		const created = await postComment(body);
		return new Response(JSON.stringify({ comentario: created }), {
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

