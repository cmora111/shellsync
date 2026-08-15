# Applications specific to spectrix
alias lw='$HOME/bin/librewolf >/dev/null 2>&1 &'

# Hardware/network specific to spectrix
alias NS='nmcli dev show wlp13s0b1 | grep "IP4\.DNS"'
alias netscan='sudo nmap -sn 192.168.1.0/24'

# Local development
alias cd3d='cd ~/3D_Print/'
alias cd3df='cd ~/3D_Print/ForTheLab'

# Hardware
alias baud='sudo stty -F /dev/ttyUSB1 115200'

# Remote shortcuts originating from spectrix
alias o='ssh -X pi@octopi'
