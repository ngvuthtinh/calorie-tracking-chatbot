import React from 'react';
import { View, Text, StyleSheet, ViewStyle, TextStyle } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { AppColors, Typography, Spacing, BorderRadius } from '@/constants/theme';

interface DropdownOption {
    label: string;
    value: string;
}

interface DropdownProps {
    label?: string;
    value: string;
    options: DropdownOption[];
    placeholder?: string;
    onValueChange: (value: string) => void;
    style?: ViewStyle;
    labelStyle?: TextStyle;
    contentStyle?: ViewStyle;
}

export default function Dropdown({
    label,
    value,
    options,
    placeholder = 'Select...',
    onValueChange,
    style,
    labelStyle,
    contentStyle,
}: DropdownProps) {
    return (
        <View style={[styles.container, style]}>
            {label && <Text style={[styles.label, labelStyle]}>{label}</Text>}
            <View style={[styles.pickerContainer, contentStyle]}>
                <Picker
                    selectedValue={value}
                    onValueChange={onValueChange}
                    style={styles.picker}
                    dropdownIconColor={AppColors.textGray}
                >
                    <Picker.Item
                        label={placeholder}
                        value=""
                        color={AppColors.textLight}
                    />
                    {options.map((option) => (
                        <Picker.Item
                            key={option.value}
                            label={option.label}
                            value={option.value}
                            color={AppColors.textDark}
                        />
                    ))}
                </Picker>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        marginBottom: Spacing.md,
    },
    label: {
        ...Typography.bodySmall,
        color: AppColors.textGray,
        marginBottom: Spacing.xs,
    },
    pickerContainer: {
        backgroundColor: AppColors.backgroundLightGray,
        borderRadius: BorderRadius.small,
        overflow: 'hidden',
        minHeight: 48,
        justifyContent: 'center',
    },
    picker: {
        color: AppColors.textDark,
    },
});
