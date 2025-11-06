export interface User {
	id: number;
	username: string;
	password: string;
}

export interface LoginCredentials {
	username: string;
	password: string;
}

export interface AuthResponse {
	success: boolean;
	message?: string;
	user?: {
		username: string;
	};
}

