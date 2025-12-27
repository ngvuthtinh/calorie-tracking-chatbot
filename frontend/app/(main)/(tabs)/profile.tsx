import React, { useState, useEffect } from 'react';
import { View, StyleSheet, Text, Alert, TextInput as RNTextInput} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import {
    PageContainer,
    ScreenHeader,
    PrimaryButton,
} from '@/components';
import { Dropdown } from '@/components/common/inputs';
import { Spacing, AppColors, Typography, BorderRadius } from '@/constants/theme';
import { ProfileService } from '@/services/profileService';

const GENDER_OPTIONS = [
    { label: 'Male', value: 'male' },
    { label: 'Female', value: 'female' },
];

const GOAL_OPTIONS = [
    { label: 'Lose weight', value: 'lose_weight' },
    { label: 'Maintain weight', value: 'maintain_weight' },
    { label: 'Gain weight', value: 'gain_weight' },
];

const ACTIVITY_OPTIONS = [
    { label: 'Sedentary (little or no exercise)', value: 'sedentary' },
    { label: 'Lightly Active (1-3 days/week)', value: 'lightly_active' },
    { label: 'Moderately Active (3-5 days/week)', value: 'moderately_active' },
    { label: 'Very Active (6-7 days/week)', value: 'very_active' },
    { label: 'Extra Active (fulltime job)', value: 'extra_active' },
];

export default function ProfileScreen() {
    const [age, setAge] = useState('');
    const [gender, setGender] = useState('');
    const [height, setHeight] = useState('');
    const [weight, setWeight] = useState('');
    const [activityLevel, setActivityLevel] = useState('');
    const [targetWeight, setTargetWeight] = useState('');
    const [targetDate, setTargetDate] = useState('');
    const [loading, setLoading] = useState(false);
    const [profileUpdated, setProfileUpdated] = useState(false);
    const [healthMetrics, setHealthMetrics] = useState<any>(null);
    const [goalData, setGoalData] = useState<any>(null);
    const [savedProfile, setSavedProfile] = useState<any>(null); // Store saved profile data

    useEffect(() => {
        fetchProfile();
    }, []);

    const fetchProfile = async () => {
        const data = await ProfileService.getProfile(1);
        if (data && data.success) {
            if (data.profile) {
                setAge(data.profile.age?.toString() || '');
                setGender(data.profile.gender || '');
                setHeight(data.profile.height_cm?.toString() || '');
                setWeight(data.profile.weight_kg?.toString() || '');
                setActivityLevel(data.profile.activity_level || 'sedentary');
                setSavedProfile(data.profile); // Save the profile data
                setProfileUpdated(true);
            }
            if (data.goal) {
                setTargetWeight(data.goal.target_weight_kg?.toString() || '');
                setTargetDate(data.goal.target_date || '');
                setGoalData(data.goal);
            }
            if (data.health_metrics) {
                setHealthMetrics(data.health_metrics);
            }
        }
    };

    const handleSave = async () => {
        if (!age || !gender || !height || !weight || !activityLevel) {
            Alert.alert('Error', 'Please fill in all fields');
            return;
        }

        setLoading(true);
        try {
            const data = await ProfileService.updateProfile(1, {
                age: parseInt(age),
                gender,
                height_cm: parseFloat(height),
                weight_kg: parseFloat(weight),
                activity_level: activityLevel,
                target_weight_kg: targetWeight ? parseFloat(targetWeight) : undefined,
                target_date: targetDate || undefined,
            });

            if (data && data.success) {
                setProfileUpdated(true);
                setHealthMetrics(data.health_metrics);
                setGoalData(data.goal);
                setSavedProfile(data.profile); // Update saved profile after successful save
                Alert.alert('Success', 'Profile updated successfully!');
            } else {
                Alert.alert('Error', 'Failed to update profile');
            }
        } catch (error) {
            console.error('Save profile error:', error);
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

    const getDaysRemaining = (targetDate: string) => {
        if (!targetDate) return null;
        const today = new Date();
        const target = new Date(targetDate);
        const diffTime = target.getTime() - today.getTime();
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return diffDays > 0 ? diffDays : 0;
    };

    return (
        <PageContainer scrollable>
            <ScreenHeader
                title="Profile"
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
                    contentStyle={styles.dropdownContent}
                    textStyle={styles.dropdownText}
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
                    label="Activity Level"
                    value={activityLevel}
                    options={ACTIVITY_OPTIONS}
                    placeholder="Select activity level"
                    onValueChange={setActivityLevel}
                    contentStyle={styles.dropdownContent}
                    textStyle={styles.dropdownText}
                />

                <View style={styles.inputGroup}>
                    <Text style={styles.inputLabel}>Target Weight</Text>
                    <RNTextInput
                        style={styles.input}
                        value={targetWeight}
                        onChangeText={setTargetWeight}
                        placeholder="Enter target weight (kg)"
                        placeholderTextColor={AppColors.textLight}
                        keyboardType="numeric"
                    />
                </View>

                <View style={styles.inputGroup}>
                    <Text style={styles.inputLabel}>Target Date (Optional)</Text>
                    <RNTextInput
                        style={styles.input}
                        value={targetDate}
                        onChangeText={setTargetDate}
                        placeholder="YYYY-MM-DD (e.g., 2025-06-30)"
                        placeholderTextColor={AppColors.textLight}
                    />
                </View>

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
                        <View style={styles.successHeader}>
                            <Ionicons name="checkmark-circle" size={24} color="#2E7D32" />
                            <Text style={styles.successTitle}>Profile Updated</Text>
                        </View>

                        {goalData && goalData.daily_target_kcal && (
                            <View style={styles.targetContainer}>
                                <Text style={styles.targetLabel}>Daily Calorie Target</Text>
                                <Text style={styles.targetValue}>{goalData.daily_target_kcal} kcal</Text>
                                {goalData.goal_type && (
                                    <>
                                        <View style={styles.badgeContainer}>
                                            <Text style={styles.badgeText}>
                                                {getGoalLabel(goalData.goal_type)}
                                            </Text>
                                        </View>
                                        <Text style={styles.targetNote}>
                                            {goalData.goal_type === 'lose_weight' && '(TDEE - 500 kcal to lose ~0.5kg/week)'}
                                            {goalData.goal_type === 'gain_weight' && '(TDEE + 500 kcal to gain ~0.5kg/week)'}
                                            {goalData.goal_type === 'maintain_weight' && '(Same as TDEE to maintain weight)'}
                                        </Text>
                                    </>
                                )}
                            </View>
                        )}

                        <View style={styles.statsRow}>
                            <View style={styles.statItem}>
                                <Text style={styles.statLabel}>Current Weight</Text>
                                <Text style={styles.statValue}>{savedProfile?.weight_kg || 0} kg</Text>
                            </View>
                            {goalData?.target_weight_kg && (
                                <View style={styles.statItem}>
                                    <Text style={styles.statLabel}>Target Weight</Text>
                                    <Text style={styles.statValue}>{goalData.target_weight_kg} kg</Text>
                                </View>
                            )}
                        </View>

                        {goalData?.target_date && (
                            <View style={styles.timelineContainer}>
                                <Text style={styles.timelineText}>
                                    🎯 Target Date: <Text style={styles.boldText}>{goalData.target_date}</Text>
                                </Text>
                                <Text style={styles.timelineText}>
                                    ⏱️ Days Remaining: <Text style={styles.boldText}>{getDaysRemaining(goalData.target_date)} days</Text>
                                </Text>
                            </View>
                        )}

                        <View style={styles.divider} />

                        <View style={styles.healthStats}>
                            <Text style={styles.healthText}>
                                • BMI: <Text style={styles.boldText}>{healthMetrics.bmi?.toFixed(1)}</Text> ({getBMICategory(healthMetrics.bmi)})
                            </Text>
                            <Text style={styles.healthText}>
                                • TDEE: <Text style={styles.boldText}>{Math.round(healthMetrics.tdee || 0)}</Text> kcal/day
                            </Text>
                            <Text style={styles.noteText}>
                                (TDEE = calories you burn daily to maintain current weight)
                            </Text>
                        </View>
                    </View>
                )}
            </View>
        </PageContainer >
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
    successHeader: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: Spacing.md,
    },
    successTitle: {
        ...Typography.bodyBold,
        fontSize: 16,
        color: '#2E7D32',
        marginLeft: Spacing.xs,
    },
    targetContainer: {
        backgroundColor: '#C8E6C9',
        borderRadius: BorderRadius.small,
        padding: Spacing.md,
        alignItems: 'center',
        marginBottom: Spacing.md,
    },
    targetLabel: {
        ...Typography.bodySmall,
        color: '#1B5E20',
        marginBottom: Spacing.xs / 2,
    },
    targetValue: {
        fontSize: 24,
        fontWeight: '700',
        color: '#1B5E20',
        marginBottom: Spacing.xs,
    },
    badgeContainer: {
        backgroundColor: '#A5D6A7',
        paddingHorizontal: Spacing.sm,
        paddingVertical: 2,
        borderRadius: BorderRadius.pill,
    },
    badgeText: {
        fontSize: 12,
        fontWeight: '600',
        color: '#1B5E20',
        textTransform: 'capitalize',
    },
    statsRow: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: Spacing.md,
    },
    statItem: {
        flex: 1,
        alignItems: 'center',
    },
    statLabel: {
        fontSize: 12,
        color: '#2E7D32',
        marginBottom: 2,
    },
    statValue: {
        fontSize: 16,
        fontWeight: '600',
        color: '#1B5E20',
    },
    divider: {
        height: 1,
        backgroundColor: '#A5D6A7',
        marginVertical: 8,
    },
    timelineContainer: {
        backgroundColor: '#E8F5E9',
        padding: Spacing.sm,
        borderRadius: BorderRadius.small,
        marginBottom: 5,
    },
    timelineText: {
        fontSize: 13,
        color: '#2E7D32',
        marginBottom: 4,
    },
    healthStats: {
        paddingHorizontal: Spacing.xs,
    },
    healthText: {
        fontSize: 14,
        color: '#1B5E20',
        marginBottom: Spacing.xs,
        lineHeight: 20,
    },
    boldText: {
        fontWeight: '700',
    },
    noteText: {
        fontSize: 11,
        color: '#558B2F',
        fontStyle: 'italic',
        marginTop: 2,
    },
    targetNote: {
        fontSize: 11,
        color: '#558B2F',
        fontStyle: 'italic',
        marginTop: 4,
        textAlign: 'center',
    },
    dropdownContent: {
        height: 100,
    },
    dropdownText: {
        fontSize: 20,
    }
});
