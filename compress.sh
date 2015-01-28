#!/bin/bash
. /etc/profile
. /etc/bashrc
. ~/.bash_profile
. ~/.bashrc

secs=`date -u '+%s'`
#asec=`date -u -d "1 hours ago" '+%s'`
secs=$((secs+8*3600))
sec1h=$((secs-1*3600))
sec2h=$((secs-2*3600))
sec3h=$((secs-3*3600))
sec4h=$((secs-4*3600))
sec5h=$((secs-5*3600))

YMDH=`date -u -d @$secs "+%Y.%m.%d.%H"`
AGO1=`date -u -d @$sec1h "+%Y.%m.%d.%H"`
AGO2=`date -u -d @$sec2h "+%Y.%m.%d.%H"`
AGO3=`date -u -d @$sec3h "+%Y.%m.%d.%H"`
AGO4=`date -u -d @$sec4h "+%Y.%m.%d.%H"`
AGO5=`date -u -d @$sec5h "+%Y.%m.%d.%H"`

echo "Now: $YMDH"
echo "$AGO1" "$AGO2" "$AGO3" "$AGO4" "$AGO5"
exit

csv_dir="$HOME/amazon/items"
comp_dir="$csv_dir/comp_list"
last_files=`find $HOME/amazon/logs -type f -name '*' -mmin -180`

if [ ! -e "$comp_dir" ]; then
    mkdir "$comp_dir"
fi

for f in $last_files; do
    finished=`tail -1 $f | grep 'Spider closed (finished)'`
    if [ -n "$finished" ]; then
        name=`basename $f`

        touch $comp_dir/compressed.{$YMDH,$AGO1}
        comed=`grep $name $comp_dir/compressed.{$YMDH,$AGO1}`
        if [ -n "$comed" ]; then
            continue
        fi

        echo $name

        gzip -c $csv_dir/${name}.csv > $csv_dir/${name}.csv.gz
        if [ $? -eq 0 ]; then
            echo "${name}.csv.gz" >> $comp_dir/compressed.$YMDH
        fi
    fi
done
