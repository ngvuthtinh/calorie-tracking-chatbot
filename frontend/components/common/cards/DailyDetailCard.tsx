import React from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { AppColors, Typography, Spacing, BorderRadius } from '@/constants/theme';
import PrimaryButton from '../buttons/PrimaryButton';

interface CalorieItem {
    name: string;
    calories: string;
}

interface DailyDetailCardProps {
    date?: string;
    totalCalories: string;
    consumed: CalorieItem[];
    burnt: CalorieItem[];
    onViewChat?: () => void;
    style?: ViewStyle;
}

export default function DailyDetailCard({
    date,
    totalCalories,
    consumed,
    burnt,
    onViewChat,
    style,
}: DailyDetailCardProps) {
    return (
        <View style={[styles.card, style]}>
            {/* Header */}
            <View style={styles.header}>
                <Ionicons name="flame" size={20} color={AppColors.primaryYellow} />
                <Text style={styles.headerText}>Calories</Text>
                <Text style={styles.totalCalories}>{totalCalories}</Text>
            </View>

            {/* Consumed Section */}
            {consumed.length > 0 && (
                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Consume</Text>
                    {consumed.map((item, index) => (
                        <View key={`consumed-${index}`} style={styles.item}>
                            <Text style={styles.itemName}>{item.name}</Text>
                            <Text style={styles.itemCalories}>{item.calories}</Text>
                        </View>
                    ))}
                </View>
            )}

            {/* Burnt Section */}
            {burnt.length > 0 && (
                <View style={styles.section}>
                    <Text style={styles.sectionTitle}>Burnt</Text>
                    {burnt.map((item, index) => (
                        <View key={`burnt-${index}`} style={styles.item}>
                            <Text style={styles.itemName}>{item.name}</Text>
                            <Text style={styles.itemCalories}>{item.calories}</Text>
                        </View>
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
        borderRadius: BorderRadius.medium,
        padding: Spacing.md,
        marginTop: Spacing.md,
    },
    header: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: Spacing.md,
    },
    headerText: {
        ...Typography.bodyBold,
        color: AppColors.textDark,
        marginLeft: Spacing.sm,
        flex: 1,
    },
    totalCalories: {
        ...Typography.bodyBold,
        color: AppColors.textDark,
    },
    section: {
        marginBottom: Spacing.md,
    },
    sectionTitle: {
        ...Typography.bodyBold,
        color: AppColors.textDark,
        marginBottom: Spacing.sm,
    },
    item: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        paddingVertical: Spacing.xs,
    },
    itemName: {
        ...Typography.bodySmall,
        color: AppColors.textDark,
    },
    itemCalories: {
        ...Typography.bodySmall,
        color: AppColors.textGray,
    },
    button: {
        marginTop: Spacing.sm,
    },
});
