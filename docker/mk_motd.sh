#!/bin/bash
# Discription : convert dot image to motd
# Author      : hasegit
# Notes       : install imagemagick before

# for replace transparent color
transparent_before="190;179;145"

# convert image to ppm and output to stdout
ppm=$(convert ${1:-a} -compress none ppm:- 2>/dev/null)

# convert error check
if [ -z "${ppm}" ] ; then
    echo -e "Convert Error or Imagemagick is not installed.\nUsage: ${0} <any dot image>"
    exit 1
fi

# set ppm data to positional parameter,
# get cols, then discard ppm parameters
set ${ppm}
cols=${2}
shift 4

{
    # get three each values (rgb) from ppm
    for i in $(eval echo {1..${#}..3})
    do
        j=$((i+1))
        k=$((i+2))

        rgb="${!i};${!j};${!k}"
        # rgb -> 216 r 6 x g 6 x b 6 
        c=$((${!i} / 43 * 36 + ${!j} / 43 * 6 + ${!k} / 43 + 16)) 
        # start a new line when reach cols
        if [ $(( (${i} + 2) / 3 % ${cols} )) -eq 0 ] ; then
          if [ ${rgb} == ${transparent_before} ] ; then
            echo -e "  "
          else
            #echo -e "\033[48;2;${rgb}m  \033[m"
            echo -e "\033[48;5;${c}m  \033[m"
          fi
        else
          if [ ${rgb} == ${transparent_before} ] ; then
            echo -en "  "
          else
            #echo -en "\033[48;2;${rgb}m  \033[m"
            echo -en "\033[48;5;${c}m  \033[m"
          fi
        fi
    done
} > /etc/motd

exit 0