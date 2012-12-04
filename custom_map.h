#ifndef H_GLOBAL_MAP
#define H_GLOBAL_MAP

/* Set up amount of joysticks here */
#define JOYCOUNT 2

/* Set up event to read from */
#define INPUT_PATH "/dev/input/by-path/platform-i8042-serio-0-event-kbd"

#endif


#ifdef H_CONFIGURE_JOYSTICKS
#ifndef H_CONFIGURE_JOYSTICKS_SEEN
#define H_CONFIGURE_JOYSTICKS_SEEN

#define JOYSTICK_ADD_KEY(key, bit, device) \
    if (device == j) { \
        if(ioctl(js[device], bit, key) < 0) { \
            perror("Error in JOYSTICK_ADD_KEY"); \
            fprintf(stderr, "ERROR: JOYSTICK_ADD_KEY for device %d, key %s, bit: %s\n", device, #key, #bit); \
            return 1; \
        } else { \
            printf("JOYSTICK_ADD_KEY for device %d, key %s, bit: %s\n", device, #key, #bit); \
        } \
    }


#define JOYSTICK_SET_LIM(lim, val, key) \
    uidev.lim[key] = val;

/* Configure first joystick.
 *
 * Here we just tell the program what keys we want to use.
 * If a key is not enabled here, it will never be passed.
 */

/* Hats.
 *
 * We set the absmax and absmin; otherwise the hats make no sense.
 */
JOYSTICK_ADD_KEY(ABS_HAT0X, UI_SET_ABSBIT, 0)
JOYSTICK_SET_LIM(absmax, 1, ABS_HAT0X)
JOYSTICK_SET_LIM(absmin, -1, ABS_HAT0X)
JOYSTICK_ADD_KEY(ABS_HAT0Y, UI_SET_ABSBIT, 0)
JOYSTICK_SET_LIM(absmax, 1, ABS_HAT0Y)
JOYSTICK_SET_LIM(absmin, -1, ABS_HAT0Y)

/* Buttons. */
JOYSTICK_ADD_KEY(BTN_JOYSTICK, UI_SET_KEYBIT, 0)
JOYSTICK_ADD_KEY(BTN_0, UI_SET_KEYBIT, 0)
JOYSTICK_ADD_KEY(BTN_1, UI_SET_KEYBIT, 0)
JOYSTICK_ADD_KEY(BTN_2, UI_SET_KEYBIT, 0)
JOYSTICK_ADD_KEY(BTN_3, UI_SET_KEYBIT, 0)

/* Second joystick ; same comments as first one */
JOYSTICK_ADD_KEY(ABS_HAT0X, UI_SET_ABSBIT, 1)
JOYSTICK_SET_LIM(absmax, 1, ABS_HAT0X)
JOYSTICK_SET_LIM(absmin, -1, ABS_HAT0X)

JOYSTICK_ADD_KEY(ABS_HAT0Y, UI_SET_ABSBIT, 1)
JOYSTICK_SET_LIM(absmax, 1, ABS_HAT0X)
JOYSTICK_SET_LIM(absmin, -1, ABS_HAT0X)

JOYSTICK_ADD_KEY(BTN_JOYSTICK, UI_SET_KEYBIT, 1)
JOYSTICK_ADD_KEY(BTN_0, UI_SET_KEYBIT, 1)
JOYSTICK_ADD_KEY(BTN_1, UI_SET_KEYBIT, 1)
JOYSTICK_ADD_KEY(BTN_2, UI_SET_KEYBIT, 1)
JOYSTICK_ADD_KEY(BTN_3, UI_SET_KEYBIT, 1)
#endif
#endif

/* Now follows keymapping, do not touch ifdef */
#ifdef H_IN_CASE
#ifndef H_IN_CASE_SEEN
#define H_IN_CASE_SEEN
#define KEYMAP(in_key, out_key, out_type, device, val) \
    case in_key: \
        je.type = out_type; \
        je.code = out_key; \
        je.value = val(e.value); \
        j = device; \
        break;

/* First joystick */

/* HAT */
KEYMAP(KEY_UP, ABS_HAT0Y, EV_ABS, 0, -)
KEYMAP(KEY_DOWN, ABS_HAT0Y, EV_ABS, 0, +)
KEYMAP(KEY_LEFT, ABS_HAT0X, EV_ABS, 0, -)
KEYMAP(KEY_RIGHT, ABS_HAT0X, EV_ABS, 0, +)

/* Red buttons */
KEYMAP(KEY_LEFTCTRL, BTN_0, EV_KEY, 0, +)
KEYMAP(KEY_LEFTALT, BTN_1, EV_KEY, 0, +)
KEYMAP(KEY_SPACE, BTN_2, EV_KEY, 0, +)

/* Yellow button */
KEYMAP(KEY_1, BTN_3, EV_KEY, 0, +)

/* Second joystick */

/* HAT */
KEYMAP(KEY_R, ABS_HAT0Y, EV_ABS, 1, -)
KEYMAP(KEY_F, ABS_HAT0Y, EV_ABS, 1, +)
KEYMAP(KEY_D, ABS_HAT0X, EV_ABS, 1, -)
KEYMAP(KEY_G, ABS_HAT0X, EV_ABS, 1, +)

/* Red buttons */
KEYMAP(KEY_A, BTN_0, EV_KEY, 1, +)
KEYMAP(KEY_S, BTN_1, EV_KEY, 1, +)
KEYMAP(KEY_Q, BTN_2, EV_KEY, 1, +)

/* Yellow button */
KEYMAP(KEY_2, BTN_3, EV_KEY, 1, +)
#endif
#endif
