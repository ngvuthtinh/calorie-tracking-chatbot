import React from 'react';
import { View, Text, StyleSheet, ViewStyle, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { AppColors, Typography, Spacing } from '@/constants/theme';
import CalendarDay from './CalendarDay';

interface CalendarGridProps {
    month: string;
    year: number;
    selectedDate?: number;
    currentDate?: number;
    onDatePress?: (date: number) => void;
    onMonthChange?: (direction: 'prev' | 'next') => void;
    style?: ViewStyle;
}

const WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'];

export default function CalendarGrid({
    month,
    year,
    selectedDate,
    currentDate,
    onDatePress,
    onMonthChange,
    style,
}: CalendarGridProps) {
    // Calculate the first day of the month (0 = Sunday, 1 = Monday, etc.)
    const monthIndex = getMonthIndex(month);
    const firstDayOfMonth = new Date(year, monthIndex, 1).getDay();

    // Convert Sunday (0) to 7 for Monday-first week
    const startOffset = firstDayOfMonth === 0 ? 6 : firstDayOfMonth - 1;

    // Generate days for the month
    const daysInMonth = new Date(year, monthIndex + 1, 0).getDate();

    // Create array with empty cells for offset, then actual days
    const calendarCells = [
        ...Array(startOffset).fill(null),
        ...Array.from({ length: daysInMonth }, (_, i) => i + 1)
    ];

    return (
        <View style={[styles.container, style]}>
            {/* Month/Year Header with Navigation */}
            <View style={styles.headerRow}>
                <TouchableOpacity
                    onPress={() => onMonthChange?.('prev')}
                    style={styles.navButton}
                >
                    <Ionicons name="chevron-back" size={24} color={AppColors.textDark} />
                </TouchableOpacity>

                <Text style={styles.monthYear}>{`${month}, ${year}`}</Text>

                <TouchableOpacity
                    onPress={() => onMonthChange?.('next')}
                    style={styles.navButton}
                >
                    <Ionicons name="chevron-forward" size={24} color={AppColors.textDark} />
                </TouchableOpacity>
            </View>

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
                {calendarCells.map((date, index) => (
                    date === null ? (
                        <View key={`empty-${index}`} style={styles.emptyCell} />
                    ) : (
                        <CalendarDay
                            key={date}
                            date={date}
                            isSelected={selectedDate === date}
                            isToday={currentDate === date}
                            onPress={onDatePress}
                        />
                    )
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
    headerRow: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: Spacing.md,
    },
    navButton: {
        padding: Spacing.xs,
    },
    monthYear: {
        ...Typography.headerMedium,
        color: AppColors.textDark,
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
    },
    emptyCell: {
        width: '14.28%', // 100% / 7 days = 14.28%
        aspectRatio: 1,
        alignItems: 'center',
        justifyContent: 'center',
    },
});
