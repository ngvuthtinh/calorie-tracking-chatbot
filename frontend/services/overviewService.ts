import { API_ENDPOINTS } from '@/config/api';

export interface OverviewStats {
    total_days_logged: number;
    current_streak: number;
    weight_start: number;
    weight_current: number;
    start_date: string;
    today_intake_kcal: number;
    today_burned_kcal: number;
    total_calories_intake: number;
    total_calories_burned: number;
}

export class OverviewService {
    static async getOverviewStats(userId: number): Promise<OverviewStats | null> {
        try {
            const response = await fetch(`${API_ENDPOINTS.OVERVIEW}?user_id=${userId}`);

            if (!response.ok) {
                console.error('Failed to fetch overview stats:', response.status);
                return null;
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching overview stats:', error);
            return null;
        }
    }
}
