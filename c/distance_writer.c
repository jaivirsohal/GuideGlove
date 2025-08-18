#include <stdio.h>
#include <pigpiod_if2.h>
#include <unistd.h>    // for usleep(), sleep()
#include <time.h>

#define TRIG_PIN        23  // BCM 23 (pin 16)
#define ECHO_PIN        24  // BCM 24 (pin 18)
#define OUTPUT_FILENAME "distances.txt"

int main(void) {
    int pi = pigpio_start(NULL, NULL);
    if (pi < 0) {
        fprintf(stderr, "Failed to connect to pigpiod daemon\n");
        return 1;
    }

    // Set up the pins
    set_mode(pi, TRIG_PIN, PI_OUTPUT);
    set_mode(pi, ECHO_PIN, PI_INPUT);
    gpio_write(pi, TRIG_PIN, 0);
    sleep(1);  // let sensor settle

    printf("Writing distance data to %s. Press Ctrl+C to stop.\n", OUTPUT_FILENAME);

    while (1) {
        // Trigger a 10 µs pulse
        gpio_write(pi, TRIG_PIN, 1);
        usleep(10);
        gpio_write(pi, TRIG_PIN, 0);

        // Wait for echo rising edge
        uint32_t start_tick = 0, end_tick = 0;
        double t0 = time_time();
        while (gpio_read(pi, ECHO_PIN) == 0) {
            if (time_time() - t0 > 0.1) break;
        }
        start_tick = get_current_tick(pi);

        // Wait for echo falling edge
        t0 = time_time();
        while (gpio_read(pi, ECHO_PIN) == 1) {
            if (time_time() - t0 > 0.1) break;
        }
        end_tick = get_current_tick(pi);

        // Write to file
        FILE *fp = fopen(OUTPUT_FILENAME, "w");
        if (!fp) {
            fprintf(stderr, "Error opening %s\n", OUTPUT_FILENAME);
        } else {
            if (end_tick > start_tick) {
                float pulse_us = (float)(end_tick - start_tick);
                float dist_cm  = (pulse_us / 1e6f) * 17150.0f;
                fprintf(fp, "%.2f\n", dist_cm);
            } else {
                fprintf(fp, "-1.0\n");
            }
            fclose(fp);
        }

        usleep(50000);  // 50 ms between measurements
    }

    pigpio_stop(pi);
    return 0;
}
