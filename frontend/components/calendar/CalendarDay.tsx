import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ViewStyle } from 'react-native';
import { AppColors, Typography, Spacing, BorderRadius } from '@/constants/theme';

interface CalendarDayProps {
    date: number;
    isSelected?: boolean;
    isToday?: boolean;
    onPress?: (date: number) => void;
    style?: ViewStyle;
}

export default function CalendarDay({
    date,
    isSelected = false,
    isToday = false,
    onPress,
    style,
}: CalendarDayProps) {
    return (
        <TouchableOpacity
            style={[
                styles.day,
                isSelected && styles.selected,
                isToday && !isSelected && styles.today,
                style,
            ]}
            onPress={() => onPress?.(date)}
            activeOpacity={0.7}
        >
            <Text
                style={[
                    styles.text,
                    isSelected && styles.selectedText,
                    isToday && !isSelected && styles.todayText,
                ]}
            >
                {date.toString().padStart(2, '0')}
            </Text>
        </TouchableOpacity>
    );
}

const styles = StyleSheet.create({
    day: {
        width: 40,
        height: 40,
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: BorderRadius.pill,
    },
    selected: {
        backgroundColor: AppColors.primaryYellow,
    },
    today: {
        borderWidth: 1,
        borderColor: AppColors.primaryYellow,
    },
    text: {
        ...Typography.bodySmall,
        color: AppColors.textDark,
    },
    selectedText: {
        fontWeight: '700',
        color: AppColors.textDark,
    },
    todayText: {
        color: AppColors.primaryYellow,
        fontWeight: '600',
    },
});
