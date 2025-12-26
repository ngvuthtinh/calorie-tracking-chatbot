import React from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { AppColors, Typography, Spacing } from '@/constants/theme';
import CalendarDay from './CalendarDay';

interface CalendarGridProps {
    month: string;
    year: number;
    selectedDate?: number;
    currentDate?: number;
    onDatePress?: (date: number) => void;
    style?: ViewStyle;
}

const WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'];

export default function CalendarGrid({
    month,
    year,
    selectedDate,
    currentDate,
    onDatePress,
    style,
}: CalendarGridProps) {
    // Generate days for the month (simplified - you may want to use a date library)
    const daysInMonth = new Date(year, getMonthIndex(month) + 1, 0).getDate();
    const days = Array.from({ length: daysInMonth }, (_, i) => i + 1);

    return (
        <View style={[styles.container, style]}>
            {/* Month/Year Header */}
            <Text style={styles.monthYear}>{`${month}, ${year}`}</Text>

            {/* Weekday Labels */}
            <View style={styles.weekdayRow}>
                {WEEKDAYS.map((day) => (
                    <Text
                        key={day}
                        style={[
                            styles.weekday,
                            (day === 'Sat' || day === 'Sun') && styles.weekdayWeekend,
                        ]}
                    >
                        {day}
                    </Text>
                ))}
            </View>

            {/* Calendar Grid */}
            <View style={styles.grid}>
                {days.map((date) => (
                    <CalendarDay
                        key={date}
                        date={date}
                        isSelected={selectedDate === date}
                        isToday={currentDate === date}
                        onPress={onDatePress}
                    />
                ))}
            </View>
        </View>
    );
}

function getMonthIndex(month: string): number {
    const months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];
    return months.indexOf(month);
}

const styles = StyleSheet.create({
    container: {
        marginVertical: Spacing.md,
    },
    monthYear: {
        ...Typography.headerMedium,
        color: AppColors.textDark,
        marginBottom: Spacing.md,
    },
    weekdayRow: {
        flexDirection: 'row',
        justifyContent: 'space-around',
        marginBottom: Spacing.sm,
    },
    weekday: {
        ...Typography.small,
        color: AppColors.textGray,
        width: 40,
        textAlign: 'center',
    },
    weekdayWeekend: {
        color: AppColors.primaryYellow,
    },
    grid: {
        flexDirection: 'row',
        flexWrap: 'wrap',
        justifyContent: 'space-around',
        gap: Spacing.xs,
    },
});
