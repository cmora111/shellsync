function via {
    vi ~/.bash_aliases ; source ~/.bash_aliases
}
function agi {

    sudo apt-get -y install $1 && echo $1 >> ~/README.installed
}
function bkp {
    cp $1 $1.bkp
}
function fnd {
    find .  -type f -name $1 -print
}

function fndg {
    find . -type f -exec grep -i "$1" {} \; -print
}

function los() {
  img="$1"
  dev="$(sudo losetup --show -f -P "$img")"
  echo "$dev"
  for part in "$dev"?*; do
    if [ "$part" = "${dev}p*" ]; then
      part="${dev}"
    fi
    dst="/mnt/$(basename "$part")"
    echo "$dst"
    sudo mkdir -p "$dst"
    sudo mount "$part" "$dst"
  done
}

function losd() {
  dev="/dev/loop$1"
  for part in "$dev"?*; do
    if [ "$part" = "${dev}p*" ]; then
      part="${dev}"
    fi
    dst="/mnt/$(basename "$part")"
    sudo umount "$dst"
  done
  sudo losetup -d "$dev"
}

function png2ico () {
    local i="${1}" o="${2:-${1:r}.ico}" s="${png2ico_size:-256}"
    convert -resize x${s} -gravity center -crop ${s}x${s}+0+0 "$i" -flatten -colors 256 -background transparent "$o"
}

wmmc() {
    sudo dd if="$1" of=/dev/mmcblk1 bs=1M status=progress
}

mp4() {
   ffmpeg -i "$f" -vn -ar 44100 -ac 2 -ab 192k -f mp3 "$name.mp3"
}
