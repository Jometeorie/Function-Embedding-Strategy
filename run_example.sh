# Sometimes you may receive the warning of "MatplotlibDeprecationWarning", 
# which is not important here. So we can add -W ignore
echo "Processing Fat Tree: "
for((i = 0; i < 10; i++));
do
	python -W ignore combine_fat_tree.py \
		--num_of_pod=4 \
		--times=1 \
		--display_all=True \
		--N=3
done

echo "Processing Normal Net: "
for((i = 0; i < 10; i++));
do
	python -W ignore combine_normal_net.py \
		--num_of_nodes=40 \
		--times=1 \
		--degrees=4 \
		--display_all=True \
		--N=3 \
		--load_file=Topo/test2.pkl
done

echo "Processing Normal Tree: "
for((i = 0; i < 10; i++));
do
	python -W ignore combine_normal_tree.py \
		--num_of_nodes=40 \
		--degrees=3 \
		--times=1 \
		--display_all=True \
		--N=3 
done