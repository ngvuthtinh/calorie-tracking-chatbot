import React, { useState, useEffect } from 'react';
import { View, StyleSheet, Text } from 'react-native';
import { useRouter } from 'expo-router';
import {
    PageContainer,
    ScreenHeader,
    CalendarGrid,
    StatCard,
    PrimaryButton,
    DailyDetailCard,
} from '@/components';
import { Spacing, AppColors } from '@/constants/theme';
import { OverviewService } from '@/services/overviewService';
import { CalendarService } from '@/services/calendarService';

export default function CalendarScreen() {
    const router = useRouter();
    const [selectedDate, setSelectedDate] = useState(new Date());
    const [stats, setStats] = useState({
        kcalEaten: 0,
        kcalBurnt: 0,
        daysOnTarget: 0,
    });
    const [dailyDetail, setDailyDetail] = useState<any>(null);

    useEffect(() => {
        fetchOverviewStats();
        // Fetch detail for today initially
        fetchDayDetail(new Date());
    }, []);

    const fetchOverviewStats = async () => {
        const data = await OverviewService.getOverviewStats(1);
        if (data) {
            setStats({
                kcalEaten: Math.round(data.total_calories_intake || 0),
                kcalBurnt: Math.round(data.total_calories_burned || 0),
                daysOnTarget: data.total_days_logged || 0,
            });
        }
    };

    const fetchDayDetail = async (date: Date) => {
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const dateStr = `${year}-${month}-${day}`;

        const data = await CalendarService.getDayView(1, dateStr);
        setDailyDetail(data); // null if failed, which is handled in UI
    };

    const handleDatePress = (date: number) => {
        const newDate = new Date(selectedDate.getFullYear(), selectedDate.getMonth(), date);
        setSelectedDate(newDate);
        fetchDayDetail(newDate);
    };

    const handleMonthChange = (direction: 'prev' | 'next') => {
        const currentMonth = selectedDate.getMonth();
        const currentYear = selectedDate.getFullYear();

        if (direction === 'prev') {
            setSelectedDate(new Date(currentYear, currentMonth - 1, 1));
        } else {
            setSelectedDate(new Date(currentYear, currentMonth + 1, 1));
        }
    };

    const handleViewChat = () => {
        const year = selectedDate.getFullYear();
        const month = String(selectedDate.getMonth() + 1).padStart(2, '0');
        const day = String(selectedDate.getDate()).padStart(2, '0');
        const dateStr = `${year}-${month}-${day}`;

        router.push({
            pathname: '/day-chat',
            params: { date: dateStr }
        });
    };

    const monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'];
    const currentMonth = monthNames[selectedDate.getMonth()];
    const currentYear = selectedDate.getFullYear();
    const today = new Date();
    const isCurrentMonth = selectedDate.getMonth() === today.getMonth() &&
        selectedDate.getFullYear() === today.getFullYear();

    return (
        <PageContainer scrollable>
            <ScreenHeader
                title="Overview"
                subtitle="Your total progress"
                showBackButton={false}
            />

            {/* Overview Stats */}
            <View style={styles.statsContainer}>
                <StatCard
                    icon="flame"
                    value={stats.kcalEaten.toString()}
                    label="total eaten"
                />
                <StatCard
                    icon="fitness"
                    value={stats.kcalBurnt.toString()}
                    label="total burnt"
                />
                <StatCard
                    icon="checkmark-circle"
                    value={stats.daysOnTarget.toString()}
                    label="days on target"
                />
            </View>

            {/* Calendar */}
            <View style={styles.calendarContainer}>
                <CalendarGrid
                    month={currentMonth}
                    year={currentYear}
                    selectedDate={selectedDate.getDate()}
                    currentDate={isCurrentMonth ? today.getDate() : undefined}
                    onDatePress={handleDatePress}
                    onMonthChange={handleMonthChange}
                />
            </View>

            {/* Daily Detail Card */}
            {dailyDetail && (
                <View style={styles.detailContainer}>
                    <DailyDetailCard
                        summary={dailyDetail.summary}
                        food_entries={dailyDetail.food_entries}
                        exercise_entries={dailyDetail.exercise_entries}
                        onViewChat={handleViewChat}
                    />
                </View>
            )}
        </PageContainer>
    );
}

const styles = StyleSheet.create({
    statsContainer: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        paddingHorizontal: Spacing.md,
        paddingVertical: Spacing.lg,
        gap: Spacing.sm,
    },
    calendarContainer: {
        paddingHorizontal: Spacing.md,
    },
    detailContainer: {
        paddingHorizontal: Spacing.md,
        paddingBottom: Spacing.lg,
    },
});
