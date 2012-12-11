/*
 * Status:
 *
 * - Can map keys from some keyboard to keys on a joystick.
 * - Has programmable config format (see config.h)
 *
 * TODO:
 * - Allow multiple keymaps per input key event; currently we override previous
 *   values.
 * - Allow multiple inputs, modify config file to allow for mapping from
 *   specific inputs.
 *
 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <unistd.h>
#include <fcntl.h>

#include <signal.h>

#include <linux/input.h>
#include <linux/uinput.h>

#include <err.h>
#include <poll.h>
#include <errno.h>

#include "config.h"

#define UINPUT_PATH "/dev/uinput"

/* Reverse mapping, for later use */
static const struct _key_to_str {
    char *name;
    int num;
} key_map[] = {
#define DEF_KEY(NAME) \
    {#NAME,NAME},
    #include "def_keys.h"
    {NULL, -1}
};

static int get_key_num(char* name)
{
    int i = 0;

    while (key_map[i].name) {
        if (!strcmp(key_map[i].name, name))
            return key_map[i].num;

        i++;
    }

    return -1;
}

static int js[JOYCOUNT];

void free_js(int sig) {
    int j;

    (void) sig;
    for(j = 0; j < JOYCOUNT; j++) {
        printf("Freeing joystick: %d\n", j);
        if (ioctl(js[j], UI_DEV_DESTROY) < 0) {
            perror("Error freeing joystick");
        }
        close(js[j]);
    }
    exit(1);
}

int main(int argc, char** argv) {
    int j, nowrite, rfds, fdrr = 0;
    int in[INPUT_DEVICE_COUNT]; /* fds */
    struct pollfd pin[INPUT_DEVICE_COUNT];
    struct input_event e, je;
    struct uinput_user_dev uidev;


    (void)argc;
    (void)argv;

    (void)get_key_num;

    /* Open required input devices */
    #define H_CONFIGURE_EVENTS
    #include "config.h"

    /* Now setup poll structure */
    for (j = 0; j < INPUT_DEVICE_COUNT; j++)
    {
        pin[j].fd = in[j];
        pin[j].events = POLLIN;
    }

    if(signal(SIGINT, free_js) == SIG_ERR) {
        printf("SIGINT handler registration failed\n");
        return 1;
    }

    for(j = 0; j < JOYCOUNT; j++) {
        /* Memset because we are already setting the absmax/absmin */
        memset(&uidev, '\0', sizeof(struct uinput_user_dev));
        js[j] = open(UINPUT_PATH, O_WRONLY | O_NONBLOCK);
        if (js[j] < 0) {
            perror("Could not open:" UINPUT_PATH);
            return 1;
        }

        #define H_CONFIGURE_JOYSTICKS
        #include "config.h"

        /* Allocate device info */
        snprintf(uidev.name, UINPUT_MAX_NAME_SIZE, "key2joy:%d", j);

        uidev.id.bustype = BUS_USB;
        uidev.id.vendor  = 0x42;
        uidev.id.product = 0xbebe;
        uidev.id.version = 1;

        if (write(js[j], &uidev, sizeof(uidev)) < 0) {
            perror("write");
            return EXIT_FAILURE;
        }

        if (ioctl(js[j], UI_DEV_CREATE)) {
            perror("ioctl create");
            return EXIT_FAILURE;
        }
    }

    /* Do it! */
    while (1) {
        printf("Entering poll..\n");
        /* Any data available? */
        if ((rfds = poll(pin, INPUT_DEVICE_COUNT, -1)) < 0) {
            /* Interrupted by signal */
            if (errno == EINTR)
                continue;
            perror("poll");
            return EXIT_FAILURE;
        }
        printf("Leaving poll..\n");

        /* Round-robin check readers */
        while (rfds) {
            if (pin[fdrr].revents & POLLIN) {
                printf("Device %d has input\n", fdrr);
                /* XXX: Need checking for complete read? */
                if (read(in[fdrr], &e, sizeof(struct input_event)) < 0) {
                    /* Interrupted by singal? Retry */
                    if (errno == EINTR)
                        continue;

#if 0
                    if (errno == EWOULDBLOCK || errno == EAGAIN) {
                        printf("poll tells us device %d is readable.. it is not\n", fdrr);
                        rfds -= 1;
                        fdrr = (fdrr + 1) % INPUT_DEVICE_COUNT;
                        continue;
                    }
#endif

                    err(EXIT_FAILURE, "reading input device nr. %d failed", fdrr);
                }

                printf("Event: (Type: %d, Code: %d, Value %d)\n", e.type, e.code, e.value);
            }

            /* Now handle received event */
            memset(&je, '\0', sizeof(struct input_event));
            nowrite = 1;
            j = 0;

            #define H_JOYMAP
            #include "config.h"

            /* Update poll read mechanism */
            fdrr = (fdrr + 1) % INPUT_DEVICE_COUNT;
            rfds -= 1;

            if (nowrite == 0) {
                printf("Writing %d to %d\n", e.code, j);
                if(write(js[j], &je, sizeof(struct input_event)) < 0) {
                    perror("Event write event");
                    return EXIT_FAILURE;
                }
            }

            /* Synchronisation events */
            if (e.type == EV_SYN) {
                memset(&je, '\0', sizeof(struct input_event));
                printf("SYN event\n");

                je.type = EV_SYN;
                je.code = 0;
                je.value = 0;

                if (write(js[j], &je, sizeof(struct input_event)) < 0) {
                    perror("SYN write event");
                    return EXIT_FAILURE;
                }
            }

        } /* End reader check loop */

    } /* End main loop */

    return 0;
}
