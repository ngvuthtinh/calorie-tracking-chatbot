import React, { useState, useEffect } from 'react';
import { View, StyleSheet, Text, ScrollView, Alert, TextInput as RNTextInput } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import {
    PageContainer,
    ScreenHeader,
    PrimaryButton,
} from '@/components';
import { Dropdown } from '@/components/common/inputs';
import { Spacing, AppColors, Typography, BorderRadius } from '@/constants/theme';
import { API_ENDPOINTS } from '@/config/api';

const GENDER_OPTIONS = [
    { label: 'Male', value: 'male' },
    { label: 'Female', value: 'female' },
];

const GOAL_OPTIONS = [
    { label: 'Lose weight', value: 'lose_weight' },
    { label: 'Maintain weight', value: 'maintain_weight' },
    { label: 'Gain weight', value: 'gain_weight' },
];

export default function MyIndexScreen() {
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');
    const [height, setHeight] = useState('');
    const [weight, setWeight] = useState('');
    const [goal, setGoal] = useState('');
    const [loading, setLoading] = useState(false);
    const [profileUpdated, setProfileUpdated] = useState(false);
    const [healthMetrics, setHealthMetrics] = useState<any>(null);
    const [goalData, setGoalData] = useState<any>(null);

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        try {
            const response = await fetch(`${API_ENDPOINTS.PROFILE}?user_id=1`);
            if (response.ok) {
                const data = await response.json();
                if (data.profile) {
                    setAge(data.profile.age?.toString() || '');
                    setGender(data.profile.gender || '');
                    setHeight(data.profile.height_cm?.toString() || '');
                    setWeight(data.profile.weight_kg?.toString() || '');
                    setProfileUpdated(true); // Profile exists, so show Edit button
                }
                if (data.goal) {
                    setGoal(data.goal.goal_type || '');
                    setGoalData(data.goal);
                }
                if (data.health_metrics) {
                    setHealthMetrics(data.health_metrics);
                }
            }
        } catch (error) {
            console.error('Failed to fetch profile:', error);
        }
    };

    const handleSave = async () => {
        // Validate all fields
        if (!age || !gender || !height || !weight || !goal) {
            Alert.alert('Error', 'Please fill in all fields');
            return;
        }

        setLoading(true);
        try {
            const response = await fetch(API_ENDPOINTS.PROFILE, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: 1,
                    age: parseInt(age),
                    gender,
                    height_cm: parseFloat(height),
                    weight_kg: parseFloat(weight),
                    goal_type: goal,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                setProfileUpdated(true);
                setHealthMetrics(data.health_metrics);
                setGoalData(data.goal);
                Alert.alert('Success', 'Profile updated successfully!');
            } else {
                Alert.alert('Error', 'Failed to update profile');
            }
        } catch (error) {
            console.error('Failed to save profile:', error);
            Alert.alert('Error', 'Failed to update profile');
        } finally {
            setLoading(false);
        }
    };

    const getBMICategory = (bmi: number) => {
        if (bmi < 18.5) return 'Underweight';
        if (bmi < 25) return 'Normal range';
        if (bmi < 30) return 'Overweight';
        return 'Obese';
    };

    const getGoalLabel = (goalType: string) => {
        const option = GOAL_OPTIONS.find(opt => opt.value === goalType);
        return option ? option.label : goalType;
    };

    return (
        <PageContainer scrollable>
            <ScreenHeader
                title="My Index"
                subtitle="Enter your index to get useful advice!"
                showBackButton={false}
            />

            <View style={styles.content}>
                {/* User Icon */}
                <View style={styles.iconContainer}>
                    <Ionicons name="person-circle-outline" size={80} color={AppColors.borderGray} />
                </View>

                {/* Form Fields */}
                <View style={styles.inputGroup}>
                    <Text style={styles.inputLabel}>Age</Text>
                    <RNTextInput
                        style={styles.input}
                        value={age}
                        onChangeText={setAge}
                        placeholder="Enter your age"
                        placeholderTextColor={AppColors.textLight}
                        keyboardType="numeric"
                    />
                </View>

                <Dropdown
                    label="Gender"
                    value={gender}
                    options={GENDER_OPTIONS}
                    placeholder="Select gender"
                    onValueChange={setGender}
                />

                <View style={styles.inputGroup}>
                    <Text style={styles.inputLabel}>Height</Text>
                    <RNTextInput
                        style={styles.input}
                        value={height}
                        onChangeText={setHeight}
                        placeholder="Enter height (cm)"
                        placeholderTextColor={AppColors.textLight}
                        keyboardType="numeric"
                    />
                </View>

                <View style={styles.inputGroup}>
                    <Text style={styles.inputLabel}>Weight</Text>
                    <RNTextInput
                        style={styles.input}
                        value={weight}
                        onChangeText={setWeight}
                        placeholder="Enter weight (kg)"
                        placeholderTextColor={AppColors.textLight}
                        keyboardType="numeric"
                    />
                </View>

                <Dropdown
                    label="Goal"
                    value={goal}
                    options={GOAL_OPTIONS}
                    placeholder="Select your goal"
                    onValueChange={setGoal}
                />

                {/* Save/Edit Button */}
                <PrimaryButton
                    title={profileUpdated ? "Edit" : "Save"}
                    onPress={handleSave}
                    disabled={loading}
                    style={styles.saveButton}
                />

                {/* Success Message */}
                {profileUpdated && healthMetrics && (
                    <View style={styles.successCard}>
                        <Text style={styles.successText}>✅ Profile updated</Text>
                        <Text style={styles.metricText}>
                            - BMI: {healthMetrics.bmi?.toFixed(1)} ({getBMICategory(healthMetrics.bmi)})
                        </Text>
                        <Text style={styles.metricText}>
                            - Estimated maintenance calories (TDEE): {Math.round(healthMetrics.tdee || 0)} kcal/day
                        </Text>
                        {goalData && (
                            <Text style={styles.metricText}>
                                - Goal: {getGoalLabel(goalData.goal_type)} → daily target set
                            </Text>
                        )}
                    </View>
                )}
            </View>
        </PageContainer>
    );
}

const styles = StyleSheet.create({
    content: {
        paddingHorizontal: Spacing.md,
        paddingBottom: Spacing.xl,
    },
    iconContainer: {
        alignItems: 'center',
        marginVertical: Spacing.lg,
    },
    inputGroup: {
        marginBottom: Spacing.md,
    },
    inputLabel: {
        ...Typography.bodySmall,
        color: AppColors.textGray,
        marginBottom: Spacing.xs,
    },
    input: {
        backgroundColor: AppColors.backgroundLightGray,
        borderRadius: BorderRadius.small,
        paddingVertical: Spacing.md,
        paddingHorizontal: Spacing.md,
        minHeight: 48,
        ...Typography.body,
        color: AppColors.textDark,
    },
    saveButton: {
        marginTop: Spacing.md,
    },
    successCard: {
        backgroundColor: '#E8F5E9',
        borderRadius: BorderRadius.medium,
        padding: Spacing.md,
        marginTop: Spacing.lg,
    },
    successText: {
        ...Typography.bodyBold,
        color: '#2E7D32',
        marginBottom: Spacing.sm,
    },
    metricText: {
        ...Typography.bodySmall,
        color: '#1B5E20',
        marginBottom: Spacing.xs,
    },
});
