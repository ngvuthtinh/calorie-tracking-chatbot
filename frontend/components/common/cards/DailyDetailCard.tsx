import React from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { AppColors, Typography, Spacing, BorderRadius } from '@/constants/theme';
import PrimaryButton from '../buttons/PrimaryButton';

interface LogItem {
    id: number | string;
    name: string;
    calories: number;
}

interface DailyDetailCardProps {
    summary?: {
        intake_kcal: number;
        burned_kcal: number;
        net_kcal: number;
    };
    food_entries?: LogItem[];
    exercise_entries?: LogItem[];
    onViewChat?: () => void;
    style?: ViewStyle;
}

export default function DailyDetailCard({
    summary,
    food_entries = [],
    exercise_entries = [],
    onViewChat,
    style,
}: DailyDetailCardProps) {
    return (
        <View style={[styles.card, style]}>
            {/* Calories Summary Cards */}
            <View style={styles.caloriesSummary}>
                {/* Intake Card */}
                <View style={styles.calorieCard}>
                    <View style={styles.cardIconContainer}>
                        <Text style={styles.cardIcon}>🍽️</Text>
                    </View>
                    <View style={styles.cardContent}>
                        <Text style={styles.cardLabel}>Intake</Text>
                        <Text style={styles.cardValue}>
                            {Math.round(summary?.intake_kcal || 0)}
                        </Text>
                        <Text style={styles.cardUnit}>kcal</Text>
                    </View>
                </View>

                {/* Burn Card */}
                <View style={[styles.calorieCard, styles.burnCard]}>
                    <View style={styles.cardIconContainer}>
                        <Text style={styles.cardIcon}>🔥</Text>
                    </View>
                    <View style={styles.cardContent}>
                        <Text style={styles.cardLabel}>Burn</Text>
                        <Text style={styles.cardValue}>
                            {Math.round(summary?.burned_kcal || 0)}
                        </Text>
                        <Text style={styles.cardUnit}>kcal</Text>
                    </View>
                </View>
            </View>

            {/* Net Calories */}
            <View style={styles.netCalories}>
                <Text style={styles.netLabel}>Net Calories</Text>
                <Text style={styles.netValue}>
                    {Math.round(summary?.net_kcal || 0)} kcal
                </Text>
            </View>

            {/* Food Entries */}
            {food_entries.length > 0 && (
                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Consume</Text>
                    {food_entries.map((entry, index) => (
                        <Text key={`food-${entry.id}-${index}`} style={styles.itemText}>
                            {entry.name} +{Math.round(entry.calories || 0)} calories
                        </Text>
                    ))}
                </View>
            )}

            {/* Exercise Entries */}
            {exercise_entries.length > 0 && (
                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Burnt</Text>
                    {exercise_entries.map((entry, index) => (
                        <Text key={`exercise-${entry.id}-${index}`} style={styles.itemText}>
                            {entry.name} -{Math.round(entry.calories || 0)} calories
                        </Text>
                    ))}
                </View>
            )}

            {/* View Chat Button */}
            {onViewChat && (
                <PrimaryButton
                    title="View chat"
                    onPress={onViewChat}
                    style={styles.button}
                />
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    card: {
        backgroundColor: AppColors.backgroundLightGray,
        borderRadius: 12,
        padding: Spacing.md,
        marginTop: Spacing.md,
    },
    caloriesSummary: {
        flexDirection: 'row',
        gap: Spacing.sm,
        marginBottom: Spacing.md,
    },
    calorieCard: {
        flex: 1,
        backgroundColor: 'white',
        borderRadius: 12,
        padding: Spacing.md,
        alignItems: 'center',
        borderWidth: 2,
        borderColor: AppColors.primaryYellow,
    },
    burnCard: {
        borderColor: '#FF6B6B',
    },
    cardIconContainer: {
        marginBottom: Spacing.xs,
    },
    cardIcon: {
        fontSize: 32,
    },
    cardContent: {
        alignItems: 'center',
    },
    cardLabel: {
        fontSize: 12,
        fontWeight: '500',
        color: AppColors.textGray,
        marginBottom: 4,
        textTransform: 'uppercase',
    },
    cardValue: {
        fontSize: 20,
        fontWeight: '700',
        color: AppColors.textDark,
    },
    cardUnit: {
        fontSize: 12,
        color: AppColors.textGray,
        marginTop: 2,
    },
    netCalories: {
        backgroundColor: 'white',
        borderRadius: 8,
        padding: Spacing.sm,
        alignItems: 'center',
        marginBottom: Spacing.md,
        borderLeftWidth: 4,
        borderLeftColor: AppColors.primaryYellow,
    },
    netLabel: {
        ...Typography.bodySmall,
        fontWeight: '600',
        color: AppColors.textDark,
    },
    netValue: {
        ...Typography.body,
        fontWeight: '700',
        color: AppColors.primaryYellow,
    },
    section: {
        marginBottom: Spacing.md,
    },
    sectionTitle: {
        ...Typography.bodyBold,
        color: AppColors.textDark,
        marginBottom: Spacing.sm,
    },
    itemText: {
        ...Typography.bodySmall,
        color: AppColors.textGray,
        paddingVertical: 2,
    },
    button: {
        marginTop: Spacing.sm,
    },
});
