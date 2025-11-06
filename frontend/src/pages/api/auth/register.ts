import type { APIRoute } from 'astro';
import { register } from '../../../controllers/authController';

export const prerender = false;

export const POST: APIRoute = async ({ request }) => {
	try {
		const body = await request.json();
		console.log('[API Auth] Registro intentado con:', { username: body.username });

		const result = await register(body);

		console.log('[API Auth] Resultado del registro:', result);

		if (!result.success) {
			return new Response(JSON.stringify(result), {
				status: 400,
				headers: { 'Content-Type': 'application/json' },
			});
		}

		return new Response(JSON.stringify(result), {
			status: 201,
			headers: { 'Content-Type': 'application/json' },
		});
	} catch (err: any) {
		console.error('[API Auth] Error:', err);
		return new Response(JSON.stringify({
			success: false,
			message: err?.message || 'Error interno del servidor'
		}), {
			status: 500,
			headers: { 'Content-Type': 'application/json' },
		});
	}
};

