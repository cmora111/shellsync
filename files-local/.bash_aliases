#
# Start: APT
#
alias agr='sudo apt-get -y remove '
alias ags='apt-cache search'
# see agi in th .bash_function file
alias agf='sudo apt -y --fix-broken install'
alias agudt='sudo apt-get update'
alias agugd='sudo apt-get upgrade'
alias agu='sudo apt-get update && sudo apt-get -y upgrade'
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
alias lsU='lsg /dev/ttyU*'
alias lst='lsg /dev/tty*'
alias egrep='egrep --color=auto'
alias fgrep='fgrep --color=auto'
alias grep='grep --color=auto'
#
# End: General
#
#
# Start: Applications
#
alias lw='/home/mora/bin/librewolf > /dev/null 2>&1 &'
alias vi='/usr/bin/vim'
alias vs="sudo vi "
alias shotwell='gpicview'
alias mp4tomp3='echo fmpeg -i "$f" -vn -ar 44100 -ac 2 -ab 192k -f mp3 "$name.mp3"'
#
# End: Applications
#
#
# Start: Systemctl
#
alias sr='sudo systemctl restart '
alias ss='sudo systemctl status '
alias st='sudo systemctl stop '
alias sl='systemctl list-unit-files | grep enabled'
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
alias mutt="getm; mutt;getm"
alias getm='mbsync gmail'
#
# End: Email
#
# Start: Printing
#
alias print='aeson-pretty'
alias sshf='ssh pi@10.0.0.3 -L 5900:localhost:5900 "vncserver :0 -clean"'
#
# End: Printing
# 
#
# Start: sudo commands
#
alias smkdir='sudo mkdir'
alias smv='sudo mv'
alias SCP='sudo cp'
alias vs='sudo vi'
alias schdir='sudo chdir'
alias scd='sudo cd'
alias ss='sudo -Es'
#
# End: Printing
# 
#
# Start: Admin
#
alias dmesg='sudo dmesg -T'
alias nc='network_check'
alias release='lsb_release -a'
alias wm='wmctrl -m | grep "Name" | cut -c7-'
alias acd='cd /etc/apache2'
alias wmmc='dd if="$1" of=/dev/mmcblk1 bs=1M status=progress'
alias brn="sudo ddrescue -D --force "
alias ns='netstat -tlnp'
alias NS='nmcli dev show wlp13s0b1|grep IP4\.DNS'
alias t25='tail -25'
alias license='cp ~/.LICENSE ./LICENSE'
alias si="~/bin/system_information.py"
alias netscan="nmap -sP 192.168.1.0/24"
#
# End: Admin
#
#
# Start: Remote Connections
#
alias r="ssh -X pi@r400"
alias s="ssh -X mora@spectrix"
alias g="ssh gemini@192.168.68.124"
alias v="ssh -X mora@vw"
alias ve="ssh -X mora@vwe"
alias o="ssh -X pi@octopi"
alias c='ssh -X mora@crowpi'
#
# End: Remote Connections
#

#
# alias vi='/usr/bin/vim +PluginInstall +qall'
alias nutty="sudo /usr/bin/com.github.babluboy.nutty"
alias heyu="heyu -c /etc/heyu/x10config "
alias cd3d='cd ~/3D_Print/'
alias cd3df='cd ~/3D_Print/ForTheLab'
alias mk3d="mkdir -p /media/mora/79C0-64B7/" 
alias cd3dm="cp `pwd` /media/mora/79C0-64B7/"
alias cdC="cd /media/mora/CIRCUITPY"
#
# Aliases for Miscellaneous stuff
#
alias todo='todo-txt'

alias raudio='killall pulseaudio; pulseaudio -k  ; rm -r ~/.config/pulse/* ; rm -r ~/.pulse*'
#
# Start: Python
#
alias python='python3 '
alias pyp='python -c "import sys;print(sys.path)"'
alias pms='paster create -t modern_package'
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
alias mcs='.manage.py createsuperuser'
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
# StartSub: Projects: Grocery
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
# Aliases for pmaster create -t modern_package <Project_Name>
#

alias vw='xtigervncviewer -geometry 1080x1920 -SecurityTypes VncAuth,TLSVnc -passwd /home/mora/.vnc/passwd 192.168.68.136:0'
#alias vw='xtigervncviewer -geometry 1080x1920 -AcceptSetDesktopSize -SecurityTypes VncAuth,TLSVnc -passwd /home/mora/.vnc/passwd 192.168.68.136:0'
alias vnc='x0tigervncserver -localhost=0 -SecurityTypes VncAuth,TLSVnc -geometry 1920x1080 -display=:0'
alias psa='ps -axwwl | grep -i '

#
#
#
alias baud='sudo stty -F /dev/ttyUSB1 115200'

#
# Mysql stuff
#
alias msq='mysql -u root -p'
alias xpdf='gv '
