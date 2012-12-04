#ifndef H_GLOBAL_MAP
#define H_GLOBAL_MAP

/* Set up amount of joysticks here */
#define JOYCOUNT 2

/* Set up event to read from */
#define INPUT_PATH "/dev/input/by-path/platform-i8042-serio-0-event-kbd"

#endif

/* Now follows keymapping, do not touch ifdef */
#ifdef H_IN_CASE
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

/* HAT*/
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

