import React, { ReactNode } from 'react';
import { View, Text, StyleSheet, ViewStyle } from 'react-native';
import { AppColors, Typography, Spacing } from '@/constants/theme';
import IconButton from '../buttons/IconButton';
import { Ionicons } from '@expo/vector-icons';

interface ScreenHeaderProps {
    title: string;
    subtitle?: string;
    showBackButton?: boolean;
    onBackPress?: () => void;
    rightIcon?: keyof typeof Ionicons.glyphMap;
    onRightIconPress?: () => void;
    style?: ViewStyle;
}

export default function ScreenHeader({
    title,
    subtitle,
    showBackButton = false,
    onBackPress,
    rightIcon,
    onRightIconPress,
    style,
}: ScreenHeaderProps) {
    return (
        <View style={[styles.container, style]}>
            {showBackButton && onBackPress && (
                <IconButton
                    icon="arrow-back"
                    onPress={onBackPress}
                    size={24}
                    color={AppColors.textDark}
                    style={styles.backButton}
                />
            )}

            <View style={styles.textContainer}>
                <Text style={styles.title}>{title}</Text>
                {subtitle && <Text style={styles.subtitle}>{subtitle}</Text>}
            </View>

            {rightIcon && onRightIconPress && (
                <IconButton
                    icon={rightIcon}
                    onPress={onRightIconPress}
                    size={24}
                    color={AppColors.primaryYellow}
                    style={styles.rightButton}
                />
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingVertical: Spacing.md,
        paddingHorizontal: Spacing.md,
    },
    backButton: {
        marginRight: Spacing.sm,
    },
    textContainer: {
        flex: 1,
    },
    title: {
        ...Typography.headerLarge,
        color: AppColors.textDark,
    },
    subtitle: {
        ...Typography.bodySmall,
        color: AppColors.textGray,
        marginTop: Spacing.xs / 2,
    },
    rightButton: {
        marginLeft: Spacing.sm,
    },
});
