
# DEST_DIR='../results/1_11_09/'
DEST_DIR=$1
echo $DEST_DIR

# continue by letting user set dir
for f in `find . -name gammaCRanking.pickl`; do cp --parents $f $DEST_DIR; done;
for i in `find . -name withCheck`; do cp -r --parents $i $DEST_DIR; done
for i in `find . -name withoutCheck`; do cp -r --parents $i $DEST_DIR; done
