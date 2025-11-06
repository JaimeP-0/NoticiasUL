import type { LoginCredentials, AuthResponse } from '../models/User';
import { login as authLogin } from '../services/authService';

export const login = async (credentials: LoginCredentials): Promise<AuthResponse> => {
	return await authLogin(credentials);
};

