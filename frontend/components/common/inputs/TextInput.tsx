import React from 'react';
import {
    TextInput as RNTextInput,
    View,
    StyleSheet,
    TextInputProps as RNTextInputProps,
    ViewStyle,
} from 'react-native';
import { AppColors, Typography, Spacing, BorderRadius } from '@/constants/theme';
import IconButton from '../buttons/IconButton';
import { Ionicons } from '@expo/vector-icons';

interface TextInputProps extends RNTextInputProps {
    containerStyle?: ViewStyle;
    rightIcon?: keyof typeof Ionicons.glyphMap;
    onRightIconPress?: () => void;
}

export default function TextInput({
    containerStyle,
    rightIcon,
    onRightIconPress,
    style,
    ...props
}: TextInputProps) {
    return (
        <View style={[styles.container, containerStyle]}>
            <RNTextInput
                style={[styles.input, rightIcon && styles.inputWithIcon, style]}
                placeholderTextColor={AppColors.textLight}
                {...props}
            />
            {rightIcon && onRightIconPress && (
                <IconButton
                    icon={rightIcon}
                    onPress={onRightIconPress}
                    size={24}
                    color="white"
                    backgroundColor={AppColors.primaryYellow}
                    variant="circular"
                    style={styles.iconButton}
                />
            )}
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: AppColors.backgroundLightGray,
        borderRadius: BorderRadius.pill,
        paddingHorizontal: Spacing.md,
        paddingVertical: Spacing.xs,
    },
    input: {
        flex: 1,
        ...Typography.body,
        color: AppColors.textDark,
        paddingVertical: Spacing.sm,
    },
    inputWithIcon: {
        paddingRight: Spacing.sm,
    },
    iconButton: {
        marginLeft: Spacing.sm,
    },
});
