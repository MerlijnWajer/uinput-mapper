#include "config_functions.h"

#ifndef H_GLOBAL_MAP
#define H_GLOBAL_MAP

/* Set up amount of joysticks here */
#define JOYCOUNT 1

/* Set up event to read from */
#define INPUT_PATH "/dev/input/by-path/platform-i8042-serio-0-event-kbd"

#endif

/* -------------------------------------------------------------------------- */
/* ----------------------------- SECOND SECTION ----------------------------- */
/* -------------------------------------------------------------------------- */

#ifdef H_CONFIGURE_JOYSTICKS
#ifndef H_CONFIGURE_JOYSTICKS_SEEN
#define H_CONFIGURE_JOYSTICKS_SEEN

/* Configure first joystick.
 *
 * Here we just tell the program what keys event we will expose and what
 * keys we want to use.
 *
 * If a key is not enabled here, it will never be passed.
 */

/* Mouse */
JOYSTICK_SET_OPT(EV_KEY, UI_SET_EVBIT, 0)
JOYSTICK_SET_OPT(EV_REL, UI_SET_EVBIT, 0)
JOYSTICK_ADD_KEY(BTN_LEFT, UI_SET_KEYBIT, 0)
JOYSTICK_ADD_KEY(REL_X, UI_SET_RELBIT, 0)
JOYSTICK_ADD_KEY(REL_Y, UI_SET_RELBIT, 0)
#endif
#endif

/* -------------------------------------------------------------------------- */
/* ----------------------------- THIRD SECTION ----------------------------- */
/* -------------------------------------------------------------------------- */

#ifdef H_JOYMAP
#ifndef H_JOYMAP_SEEN
#define H_JOYMAP_SEEN

KEYMAP(EV_KEY, KEY_3, BTN_LEFT, EV_KEY, 0, +)
KEYMAP(EV_KEY, KEY_M, REL_X, EV_REL, 0, 10*)
KEYMAP(EV_KEY, KEY_N, REL_X, EV_REL, 0, -10*)
KEYMAP(EV_KEY, KEY_J, REL_Y, EV_REL, 0, 10*)
KEYMAP(EV_KEY, KEY_K, REL_Y, EV_REL, 0, -10*)

#endif
#endif
