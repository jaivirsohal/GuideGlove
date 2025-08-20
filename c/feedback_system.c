#include <stdio.h>
#include <stdlib.h>      // for atof()
#include <pigpiod_if2.h>
#include <unistd.h>      // for usleep()
#include <signal.h>      // for Ctrl+C handler

#define BUZZER_PIN     18    // BCM 18 (hardware PWM0, pin 12)
#define MOTOR_PIN      17    // BCM 17 (pin 11)
#define INPUT_FILENAME "distances.txt"

int pi = -1;

// Cleanup on Ctrl+C
void cleanup(int signum) {
    printf("\nSignal received. Cleaning up...\n");
    if (pi >= 0) {
        set_PWM_dutycycle(pi, BUZZER_PIN, 0);
        gpio_write(pi, MOTOR_PIN, 0);
        pigpio_stop(pi);
    }
    _exit(0);
}

int main(void) {
    signal(SIGINT, cleanup);

    pi = pigpio_start(NULL, NULL);
    if (pi < 0) {
        fprintf(stderr, "Failed to connect to pigpiod daemon.\n");
        return 1;
    }

    // Initialize outputs
    set_PWM_frequency(pi, BUZZER_PIN, 1000);
    set_PWM_dutycycle(pi, BUZZER_PIN, 0);
    set_mode(pi, MOTOR_PIN, PI_OUTPUT);
    gpio_write(pi, MOTOR_PIN, 0);

    printf("Haptic & Audio Feedback Running on Pi Zero 2 W\n");
    printf("Buzzer: BCM %d, Motor: BCM %d\n", BUZZER_PIN, MOTOR_PIN);
    printf("Reading distances from %s\n", INPUT_FILENAME);

    while (1) {
        FILE *fp = fopen(INPUT_FILENAME, "r");
        if (!fp) {
            usleep(50000);
            continue;
        }

        char buf[32];
        float dist = -1.0f;
        if (fgets(buf, sizeof(buf), fp))
            dist = atof(buf);
        fclose(fp);

        if (dist > 0 && dist < 25) {
            // Map distance to frequency
            int freq = 3500 - (int)(dist * 70);
            if (freq < 800)  freq = 800;
            if (freq > 3000) freq = 3000;

            // Danger zone: constant high‐pitched + vibration
            if (dist < 5.0f) {
                printf("!!! DANGER: %.1f cm → constant feedback\n", dist);
                set_PWM_frequency(pi, BUZZER_PIN, freq);
                set_PWM_dutycycle(pi, BUZZER_PIN, 128);
                gpio_write(pi, MOTOR_PIN, 1);
                usleep(50000);
                continue;
            }

            // Rhythmic beeps
            int on_ms = 50;
            int off_ms;
            if (dist < 10.0f)       off_ms = dist * 4;
            else if (dist < 15.0f)  off_ms = dist * 6;
            else                    off_ms = dist * 9;
            if (off_ms < 10) off_ms = 10;

            printf("At %.1f cm: %d Hz, %d ms ON / %d ms OFF\n",
                   dist, freq, on_ms, off_ms);

            // Emit
            set_PWM_frequency(pi, BUZZER_PIN, freq);
            set_PWM_dutycycle(pi, BUZZER_PIN, 128);
            gpio_write(pi, MOTOR_PIN, 1);
            usleep(on_ms * 1000);

            set_PWM_dutycycle(pi, BUZZER_PIN, 0);
            gpio_write(pi, MOTOR_PIN, 0);
            usleep(off_ms * 1000);

        } else {
            // No obstacle nearby
            set_PWM_dutycycle(pi, BUZZER_PIN, 0);
            gpio_write(pi, MOTOR_PIN, 0);
            usleep(50000);
        }
    }

    return 0;
}
