import type { APIRoute } from 'astro';
import { login } from '../../../controllers/authController';

export const prerender = false;

export const POST: APIRoute = async ({ request }) => {
	try {
		const body = await request.json();
		console.log('[API Auth] Login intentado con:', { username: body.username });
		
		const result = await login(body);
		
		console.log('[API Auth] Resultado del login:', result);
		
		if (!result.success) {
			return new Response(JSON.stringify(result), {
				status: 401,
				headers: { 'Content-Type': 'application/json' },
			});
		}

		return new Response(JSON.stringify(result), {
			status: 200,
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

