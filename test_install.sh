SITE_PATH="`python3 -m site --user-site`"

mkdir -p $SITE_PATH
rm $SITE_PATH/gcraft -r
cp ./gcraft $SITE_PATH -r

echo "done ..."