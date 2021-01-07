import colorama
#For Windows Termcolor
colorama.init()

#RESETS
RESET = '\033[0m' # Works on Windows
#Special  (might not work on windows)
BOLD = '\033[1m'
DIM = '\033[2m'
UNDERLINE = '\033[4m'
BLINK = '\033[5m'
INVERTED = '\033[7m'
HIDDEN = '\033[8m'
#~~~~~~~~~~~~#
#Background Colors #
BDEFAULT = '\033[49m'
BWHITE = '\033[107m'
BLIGHTCYAN = '\033[106m'
BLIGHTMAGENTA = '\033[105m'
BLIGHTBLUE = '\033[104m'
BLIGHTYELLOW = '\033[103m'
BLIGHTGREEN = '\033[102m'
BLIGHTRED = '\033[101m'
BDARKGREY = '\033[100m'
BLIGHTGREY = '\033[47m'
BCYAN = '\033[46m'
BMAGENTA = '\033[45'
BBLUE = '\033[44m'
BYELLOW = '\033[43m'
BGREEN = '\033[42m'
BBLACK = '\033[40m'
BRED = '\033[41m'
#~~~~~~~~~~~~#
#Text Colors #
CLEAR_SCREEN = '\033[2J'
WHITE = '\033[97m'
LIGHTCYAN = '\033[96m'
LIGHTMAGENTA = '\033[95m'
LIGHTBLUE = '\033[94m'
LIGHTYELLOW = '\033[93m'
LIGHTGREEN = '\033[92m'
LIGHTRED = '\033[91m'
DARKGREY = '\033[90m'
LIGHTGREY = '\033[37m'
CYAN = '\033[36m'
MAGENTA = '\033[35m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
GREEN = '\033[32m'
BLACK = '\033[30m'
DEFAULT = '\033[39m'
RED = '\033[31m'
#~~~~~~~~~~~~#
#Symbols
OK = CYAN + "[" + GREEN + "✓" + CYAN + "]" + WHITE + " "
PROCESSING = CYAN + "[" + YELLOW + "~" + CYAN + "]" + WHITE  + " "
ERROR = CYAN + "[" + RED + "!" + CYAN + "]" + WHITE + " "
ARROWRIGHT = CYAN + "==> " + WHITE + " "
#~~~~~~~~~~~~#