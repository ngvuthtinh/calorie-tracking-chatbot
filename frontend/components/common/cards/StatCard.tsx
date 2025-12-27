import React from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { AppColors, Typography, Spacing, BorderRadius } from '@/constants/theme';

interface StatCardProps {
    icon: keyof typeof Ionicons.glyphMap;
    value: string | number;
    label: string;
    iconColor?: string;
    style?: ViewStyle;
}

export default function StatCard({
    icon,
    value,
    label,
    iconColor = AppColors.primaryYellow,
    style,
}: StatCardProps) {
    return (
        <View style={[styles.card, style]}>
            <Ionicons name={icon} size={24} color={iconColor} style={styles.icon} />
            <Text style={styles.value}>{value}</Text>
            <Text style={styles.label}>{label}</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    card: {
        backgroundColor: AppColors.backgroundLightGray,
        borderRadius: BorderRadius.medium,
        padding: Spacing.md,
        alignItems: 'center',
        justifyContent: 'center',
        minWidth: 100,
        flex: 1,
    },
    icon: {
        marginBottom: Spacing.xs,
    },
    value: {
        ...Typography.headerMedium,
        color: AppColors.textDark,
        marginBottom: Spacing.xs / 2,
    },
    label: {
        ...Typography.small,
        color: AppColors.textGray,
        textAlign: 'center',
    },
});
