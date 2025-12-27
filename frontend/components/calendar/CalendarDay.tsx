import React, { useState } from 'react';
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
    const [cellSize, setCellSize] = useState(0);

    return (
        <View
            style={[styles.container, style]}
            onLayout={(event) => {
                const { width } = event.nativeEvent.layout;
                setCellSize(width);
            }}
        >
            <TouchableOpacity
                style={[
                    styles.day,
                    cellSize > 0 && { width: cellSize, height: cellSize },
                    isSelected && styles.selected,
                    isToday && !isSelected && styles.today,
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
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        width: '14.28%', // 100% / 7 days
        paddingVertical: 1, // Consistent vertical spacing
        alignItems: 'center',
        justifyContent: 'center',
    },
    day: {
        alignItems: 'center',
        justifyContent: 'center',
        borderRadius: 999, // Very large to ensure perfect circle
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
