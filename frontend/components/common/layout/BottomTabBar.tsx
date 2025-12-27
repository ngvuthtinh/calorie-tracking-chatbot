import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { AppColors, Typography, Spacing, Shadows } from '@/constants/theme';

interface TabItem {
    name: string;
    icon: keyof typeof Ionicons.glyphMap;
    label: string;
}

interface BottomTabBarProps {
    tabs: TabItem[];
    activeTab: string;
    onTabPress: (tabName: string) => void;
}

export default function BottomTabBar({ tabs, activeTab, onTabPress }: BottomTabBarProps) {
    return (
        <View style={styles.container}>
            {tabs.map((tab) => {
                const isActive = activeTab === tab.name;
                return (
                    <TouchableOpacity
                        key={tab.name}
                        style={styles.tab}
                        onPress={() => onTabPress(tab.name)}
                        activeOpacity={0.7}
                    >
                        <Ionicons
                            name={tab.icon}
                            size={24}
                            color={isActive ? AppColors.primaryYellow : AppColors.textGray}
                        />
                        <Text
                            style={[
                                styles.label,
                                isActive && styles.activeLabel,
                            ]}
                        >
                            {tab.label}
                        </Text>
                    </TouchableOpacity>
                );
            })}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        backgroundColor: AppColors.backgroundWhite,
        borderTopWidth: 1,
        borderTopColor: AppColors.borderGray,
        paddingBottom: Spacing.sm,
        paddingTop: Spacing.sm,
        ...Shadows.small,
    },
    tab: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        paddingVertical: Spacing.xs,
    },
    label: {
        ...Typography.small,
        color: AppColors.textGray,
        marginTop: Spacing.xs / 2,
    },
    activeLabel: {
        color: AppColors.primaryYellow,
        fontWeight: '600',
    },
});
