import { API_ENDPOINTS } from '@/config/api';

export interface ProfileData {
    age?: number;
    gender?: string;
    height_cm?: number;
    weight_kg?: number;
    activity_level?: string;
}

export interface GoalData {
    goal_type: string;
    target_weight_kg?: number;
    weekly_diff_kg?: number;
}

export interface HealthMetrics {
    bmi: number;
    bmr: number;
    tdee: number;
}

export interface ProfileResponse {
    success: boolean;
    message: string;
    profile: ProfileData | null;
    goal: GoalData | null;
    health_metrics: HealthMetrics;
}

export class ProfileService {
    static async getProfile(userId: number): Promise<ProfileResponse | null> {
        try {
            const response = await fetch(`${API_ENDPOINTS.PROFILE}?user_id=${userId}`);
            if (!response.ok) {
                console.error('Failed to fetch profile:', response.status);
                return null;
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching profile:', error);
            return null;
        }
    }

    static async updateProfile(
        userId: number,
        data: {
            age: number;
            gender: string;
            height_cm: number;
            weight_kg: number;
            target_weight_kg?: number;
            goal_type: string;   
        }
    ): Promise<ProfileResponse | null> {
        try {
            const response = await fetch(API_ENDPOINTS.PROFILE, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: userId,
                    ...data,
                }),
            });

            if (!response.ok) {
                console.error('Failed to update profile:', response.status);
                return null;
            }

            return await response.json();
        } catch (error) {
            console.error('Error updating profile:', error);
            return null;
        }
    }
}
