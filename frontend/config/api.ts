// API Configuration
const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
    CHAT: `${API_BASE_URL}/api/chat`,
    CALENDAR_DAY: (date: string) => `${API_BASE_URL}/api/day/${date}`,
    OVERVIEW: `${API_BASE_URL}/api/overview`,
    PROFILE: `${API_BASE_URL}/api/profile`,
};

export default API_BASE_URL;
