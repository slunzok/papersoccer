cd labs

for i in $(ls); do
    tar -xzf $i
    rm $i
done
