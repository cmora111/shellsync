#
# Start: CSR
#
alias csrandkey='openssl req -new -newkey rsa:2048 -nodes -keyout spectrix.com.key -out spectrix.com.csr'
alias csrkey='openssl genrsa -out spectrix.com.key 2048'
alias csr='openssl req -new -key spectrix.com.key -out spectrix.com.csr'
#
# End: CSR
#
#
# Start: APT
#
alias agi='sudo apt-get install -y '
alias agr='sudo apt-get -y remove '
alias ags='apt-cache search'
# see agi in th .bash_function file
alias agf='sudo apt -y --fix-broken install'
alias agudt='sudo apt-get update'
alias agugd='sudo apt-get upgrade'
alias agu='sudo apt-get update && sudo apt-get -y upgrade'
alias agarm='sudo apt autoremove -y'
#
# End: APT
#
#
# Start: General
#
alias l='ls -CF'
alias la='ls -A'
alias ll='ls -alF'
alias ls='ls --color=auto'
alias lsg='ls -gailtr'
alias lsn='ls --color=no -F'
alias lsp='ls -lt patches'
alias lsU='lsg /dev/ttyU*'
alias lst='lsg /dev/tty*'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias grep='grep --color=auto'
alias galaxy='cd /run/user/1000'
alias kgvfd='killall gvfs-mtp-volume-monitor'
#
# End: General
#
#
# Start: Applications
#
alias vi='/usr/bin/vim'
#
# End: Applications
#
#
# Start: Systemctl
#
alias sr='sudo systemctl restart '
alias ss='sudo systemctl status '
alias st='sudo systemctl stop '
alias sctld='sudo systemctl disable'
alias sl='systemctl list-unit-files | grep enabled'
alias srl='sudo systemctl daemon-reload'
#
# Start: Logs
#
alias cdlg='cd /var/log ; lsg '
alias lsm='less /var/log/mail.log'
alias lsy='less /var/log/syslog'
alias ldm='less /var/log/daemon.log'
alias lae='less /var/log/apache2/error.log'
alias t='tail -f -n 20 '
#
# End: Logs
#
#
# Start: Email
#
alias srp='sr postfix'
alias ssp='ss postfix'
#
# End: Email
#
#
# Start: Printing
#
alias print='aeson-pretty'
#
# End: Printing
# 
#
# Start: sudo commands
#
alias smkdir='sudo mkdir'
alias smv='sudo mv'
alias SCP='sudo cp'
alias schdir='sudo chdir'
alias scd='sudo cd'
#
# End: sudo commands
#
#
# StartSubL: sudo commands: LVM
#
alias spvcreate='sudo pvcreate'
alias spvscan='sudo pvscan'
alias spvdisplay='sudo pvdisplay'
alias spvs='sudo pvs'
alias spvremove='sudo pvremove'
alias svgcreate='sudo vgcreate'
alias svgscan='sudo vgscan'
alias svgdisplay='sudo vgdisplay'
alias svgs='sudo vgs'
alias svgremove='sudo vgremove'
alias slvcreate='sudo lvcreate'
alias slvscan='sudo lvscan'
alias slvdisplay='sudo lvdisplay'
alias slvs='sudo lvs'
alias slvremove='sudo lvremove'
alias dmesg='sudo dmesg -e|grep -v "audit: "|grep -v "kauditd"'
#
# EndSub: sudo commands: LVM
#
#
# End: sudo 
# 
#
# Start: Admin
#
alias dmesg='sudo dmesg -T'
alias nc='network_check'
alias release='lsb_release -a'
alias wm='wmctrl -m | grep "Name" | cut -c7-'
alias wt='echo $XDG_SESSION_TYPE'
alias acd='cd /etc/apache2'
alias brn="sudo ddrescue -D --force "
alias ns='sudo netstat -tlnp'
alias NS='nmcli dev show wlp13s0b1|grep IP4\.DNS'
alias t25='tail -25'
alias license='cp ~/.LICENSE ./LICENSE'
alias si="~/bin/system_information.py"
alias netscan="nmap -sP 192.168.1.0/24"
alias netscan2="sudo nmap -sV -sC -O -T5 "
alias netscan3="sudo nmap -O "
alias netscan4="nmap -sP 192.168.1.0/24 | awk '/is up/ {print up}; {gsub (/\(|\)/,\"\"); up = \$NF}'"
alias extip="dig +short myip.opendns.com @resolver1.opendns.com"
alias xhost+="xhost +si:localuser:root"
#
# End: Admin
#
#
# Start: Remote Connections
#
# alias s="ssh -X <user>@<host>"
# alias o="ssh -X <user>@<host>"
#
# End: Remote Connections
#
#
# Start: Vim
#
# alias vi='/usr/bin/vim +PluginInstall +qall'
#
# End: Vim
#
# Start: 3d Printer
#
alias cd3d='cd ~/3D_Print/'
alias cd3df='cd ~/3D_Print/ForTheLab'
#
# End: 3d Printer
#
#
# Start: Miscellaneous
#
alias todo='todo-txt'
alias raudio='killall pulseaudio; pulseaudio -k  ; rm -r ~/.config/pulse/* ; rm -r ~/.pulse*'
#
# End: Miscellaneous
#
#
# Start: Python
#
alias python='python3 '
alias pyp='python -c "import sys;print(sys.path)"'
alias pms='paster create -t modern_package'
#
#
#
#
# StartSub: Python: Virtual Environments
#
alias venv='python3 -m venv .venv && . ./.venv/bin/activate'
alias v='. .venv/bin/activate'
alias dvenv='deactivate'
alias mve='python3 -m venv .venv'
#
# EndSub: Python: Virtual Environments
#
#
# StartSub: Python: PIP
#
alias pr='pip install -r requirements.txt'
alias pfdd='pip freeze -r ../requirements.txt'
alias pf='pip freeze > requirements.txt'
alias pi='pip install '
#
# EndSub: Python: PIP
#
#
# StartSub: Python: Django
#
alias rs='./manage.py runserver'
alias mmm='./manage.py makemigrations'
alias mm='./manage.py migrate'
alias msp='./manage.py startapp '
alias mcs='./manage.py createsuperuser'
#
# EndSub: Python: Django
#
#
# End: Python
#
#
# Start: Projects
#
alias pgc='ProjectConfig'
alias pgt='ProjectGoto'
alias pgx='ProjectGoto X10;vi -S Session.vim'
alias pgp="ProjectGoto Python"
alias pgl="ProjectList | less"
#
#
#
#
# StartSub: Projects: Grocery
#
alias pw='cd ~/public_html/Grocery'
alias mys='mysql -u root -p Grocery'
#
# EndSub: Projects: Grocery
#
#
# StartSub: Project: Coop 
#
alias scpb='scp ~/.bash_aliases pi@coop:/home/pi'
alias scpdb='scp ./Coop.db ./Coop.sql pi@coop:/home/pi/Src/Coop'
#
# EndSub: Projects: Coop
#
#
# End: Projects
#
#
# Start: VNC
#
alias vnc='x0tigervncserver -localhost=0 -SecurityTypes VncAuth,TLSVnc -geometry 1920x1080 -display=:0'
alias psa='ps -axwwl | grep -i '
#
# End: VNC
#
#
# Start: Baud
#
alias baud='sudo stty -F /dev/ttyUSB1 115200'
#
# End: Baud
#
#
# Start: Sql
#
alias msq='mysql -u root -p'
alias xpdf='gv '
#
#  End: Sql
#
