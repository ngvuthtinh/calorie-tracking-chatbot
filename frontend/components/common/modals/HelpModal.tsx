import React from 'react';
import { View, Text, Modal, TouchableOpacity, StyleSheet, ScrollView } from 'react-native';
import { AppColors, Spacing } from '@/constants/theme';

interface HelpModalProps {
    visible: boolean;
    onClose: () => void;
}

export default function HelpModal({ visible, onClose }: HelpModalProps) {
    return (
        <Modal
            visible={visible}
            animationType="slide"
            transparent={true}
            onRequestClose={onClose}
        >
            <View style={styles.modalOverlay}>
                <View style={styles.modalContent}>
                    <View style={styles.modalHeader}>
                        <Text style={styles.modalTitle}>💡 How to Use</Text>
                        <TouchableOpacity onPress={onClose}>
                            <Text style={styles.closeButton}>✕</Text>
                        </TouchableOpacity>
                    </View>

                    <ScrollView style={styles.modalScroll}>
                        <View style={styles.sectionContainer}>
                            <Text style={styles.sectionTitle}>🍎 Log Food</Text>
                            <Text style={styles.exampleText}>• &quot;Breakfast: 2 eggs, 1 bread&quot;</Text>
                            <Text style={styles.exampleText}>• &quot;Lunch: banana (200kcal)&quot;</Text>
                            <Text style={styles.exampleText}>• &quot;Eat: 1 apple&quot;</Text>
                            <Text style={styles.exampleText}>• &quot;Drink: 50ml coffe&quot;</Text>
                            <Text style={styles.exampleText}>• &quot;Dinner: 200g beef, salad&quot;</Text>
                            <Text style={styles.exampleText}>• &quot;Snack: apple&quot;</Text>
                        </View>

                        <View style={styles.sectionContainer}>
                            <Text style={styles.sectionTitle}>🏃 Log Exercise</Text>
                            <Text style={styles.exampleText}>• &quot;Exercise: run 30 min&quot;</Text>
                            <Text style={styles.exampleText}>• &quot;Exercise: gym 1 hour&quot;</Text>
                            <Text style={styles.exampleText}>• &quot;Exercise: swim 45 min&quot;</Text>
                            <Text style={styles.exampleText}>• &quot;Exercise: walk 2 km&quot;</Text>
                        </View>

                        <View style={styles.sectionContainer}>
                            <Text style={styles.sectionTitle}>✏️ Edit Entries</Text>
                            <Text style={styles.exampleText}>• &quot;Edit food f1: 3 eggs&quot;</Text>
                            <Text style={styles.exampleText}>• &quot;Edit exercise x2: run 45 min&quot;</Text>
                            <Text style={styles.exampleText}>• &quot;Add f1: 1 banana&quot;</Text>
                        </View>

                        <View style={styles.sectionContainer}>
                            <Text style={styles.sectionTitle}>🗑️ Delete Entries</Text>
                            <Text style={styles.exampleText}>• &quot;Delete food f1&quot;</Text>
                            <Text style={styles.exampleText}>• &quot;Delete exercise x2&quot;</Text>
                        </View>

                        <View style={styles.sectionContainer}>
                            <Text style={styles.sectionTitle}>📊 Check Stats</Text>
                            <Text style={styles.exampleText}>• &quot;Show summary today&quot;</Text>
                            <Text style={styles.exampleText}>• &quot;Show summary 2025-12-25&quot;</Text>
                            <Text style={styles.exampleText}>• &quot;Show weekly stats&quot;</Text>
                            <Text style={styles.exampleText}>• &quot;Show stats this week&quot;</Text>
                        </View>

                        <View style={styles.sectionContainer}>
                            <Text style={styles.sectionTitle}>🔄 Move Entries</Text>
                            <Text style={styles.exampleText}>• &quot;Move f1 to lunch&quot;</Text>
                            <Text style={styles.exampleText}>• &quot;Move f2 to dinner&quot;</Text>
                        </View>
                    </ScrollView>

                    <TouchableOpacity
                        style={styles.modalButton}
                        onPress={onClose}
                    >
                        <Text style={styles.modalButtonText}>Got it!</Text>
                    </TouchableOpacity>
                </View>
            </View>
        </Modal>
    );
}

const styles = StyleSheet.create({
    modalOverlay: {
        flex: 1,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        justifyContent: 'center',
        alignItems: 'center',
    },
    modalContent: {
        backgroundColor: 'white',
        borderRadius: 16,
        padding: Spacing.lg,
        width: '90%',
        maxHeight: '80%',
    },
    modalHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: Spacing.md,
    },
    modalTitle: {
        fontSize: 24,
        fontWeight: 'bold',
        color: AppColors.textDark,
    },
    closeButton: {
        fontSize: 28,
        color: AppColors.textGray,
        fontWeight: '300',
    },
    modalScroll: {
        maxHeight: 400,
    },
    sectionContainer: {
        marginBottom: Spacing.lg,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: '600',
        color: AppColors.textDark,
        marginBottom: Spacing.sm,
    },
    exampleText: {
        fontSize: 14,
        color: AppColors.textGray,
        marginBottom: 4,
        paddingLeft: Spacing.sm,
    },
    modalButton: {
        backgroundColor: AppColors.primaryYellow,
        paddingVertical: Spacing.md,
        borderRadius: 8,
        alignItems: 'center',
        marginTop: Spacing.md,
    },
    modalButtonText: {
        fontSize: 16,
        fontWeight: '600',
        color: AppColors.textDark,
    },
});
