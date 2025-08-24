#include <stdio.h>
#include <stdlib.h>      // For atof()
#include <pigpiod_if2.h>
#include <unistd.h>
#include <signal.h>      // For handling Ctrl+C

// --- PIN DEFINITIONS ---
#define BUZZER_PIN 22
#define MOTOR_PIN  26 // GPIO 26 will control the vibration motor
#define INPUT_FILENAME "distances.txt"

// Global variable for pigpio connection, for cleanup
int pi;

// Cleanup function for Ctrl+C
void cleanup(int signum) {
    printf("\nSignal received. Cleaning up outputs...\n");
    if (pi >= 0) {
        set_PWM_dutycycle(pi, BUZZER_PIN, 0); // Ensure buzzer is off
        gpio_write(pi, MOTOR_PIN, 0);       // Ensure motor is off
        pigpio_stop(pi);
    }
    exit(0);
}

int main(void) {
    signal(SIGINT, cleanup);
    pi = pigpio_start(NULL, NULL);
    if (pi < 0) {
        fprintf(stderr, "Failed to connect to pigpiod daemon.\n");
        return 1;
    }

    // --- SETUP PINS ---
    set_PWM_dutycycle(pi, BUZZER_PIN, 0);     // Initialize buzzer off
    set_mode(pi, MOTOR_PIN, PI_OUTPUT);      // Set motor pin as an output
    gpio_write(pi, MOTOR_PIN, 0);            // Initialize motor off

    printf("Haptic & Audio Feedback System Running.\n");
    printf("Buzzer: GPIO %d, Motor: GPIO %d\n", BUZZER_PIN, MOTOR_PIN);
    printf("Reading from %s. Press Ctrl+C to stop.\n", INPUT_FILENAME);

    while (1) {
        FILE *file_ptr = fopen(INPUT_FILENAME, "r");
        float distance = -1.0;

        if (file_ptr == NULL) {
            usleep(50000); // Check file faster: every 50ms
            continue;
        }

        char buffer[32];
        if (fgets(buffer, sizeof(buffer), file_ptr) != NULL) {
            distance = atof(buffer);
        }
        fclose(file_ptr);

        // --- DYNAMIC PITCH AND RHYTHM ---
        if (distance > 0 && distance < 25) {
            int beep_duration_ms = 50;
            int silent_delay_ms;
            int beep_frequency_hz;

            beep_frequency_hz = (int)(3500 - (distance * 70));
            if (beep_frequency_hz < 800) beep_frequency_hz = 800;
            if (beep_frequency_hz > 3000) beep_frequency_hz = 3000;

            // --- DANGER ZONE : Constant High-Pitched Tone & Vibration ---
            if (distance < 5) {
                printf("!!! DANGER - Object at %.1f cm !!! Constant Feedback\n", distance);
                // Turn BOTH buzzer and motor ON
                set_PWM_frequency(pi, BUZZER_PIN, beep_frequency_hz);
                set_PWM_dutycycle(pi, BUZZER_PIN, 128);
                gpio_write(pi, MOTOR_PIN, 1); // Motor ON
                usleep(50000);
                continue;
            }
            
            // --- RHYTHM LOGIC (Unchanged) ---
            if (distance < 10) {
                silent_delay_ms = (int)(distance * 4);
            } else if (distance < 15) {
                silent_delay_ms = (int)(distance * 6);
            } else {
                silent_delay_ms = (int)(distance * 9);
            }
            if (silent_delay_ms < 10) silent_delay_ms = 10;

            printf("Object at %.1f cm. Freq: %dHz, Rhythm: %dms ON, %dms OFF.\n",
                   distance, beep_frequency_hz, beep_duration_ms, silent_delay_ms);

            // --- Execute the synchronized beep and vibration ---
            set_PWM_frequency(pi, BUZZER_PIN, beep_frequency_hz);
            set_PWM_dutycycle(pi, BUZZER_PIN, 128); // Buzzer ON
            gpio_write(pi, MOTOR_PIN, 1);          // Motor ON
            usleep(beep_duration_ms * 1000);

            set_PWM_dutycycle(pi, BUZZER_PIN, 0); // Buzzer OFF
            gpio_write(pi, MOTOR_PIN, 0);          // Motor OFF
            usleep(silent_delay_ms * 1000);

        } else {
            // If no object is close, turn both outputs off.
            set_PWM_dutycycle(pi, BUZZER_PIN, 0);
            gpio_write(pi, MOTOR_PIN, 0);
            usleep(50000); // Check file every 50ms
        }
    }
    
    return 0;
}
