cd labs

for i in $(ls); do
    cd $i
    FILES=(*)
    LENGTH=${#FILES[@]} 
    LAST_POSITION=$((LENGTH - 1))
    FIRST_FILE=${FILES[@]:0:1}
    LAST_FILE=${FILES[@]:${LAST_POSITION}:1}
    #echo item: $i
    #echo "${FILES[@]:0:1}"
    #echo "${FIRST_FILE::${#FIRST_FILE}-4}"
    #echo "${LAST_FILE::${#LAST_FILE}-4}"
    cd ../
    echo $i "${FIRST_FILE::${#FIRST_FILE}-4}" "${LAST_FILE::${#LAST_FILE}-4}" >> spis
done
