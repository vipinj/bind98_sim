
set terminal png enhanced size 2048,1024
set output 'plot.png'
set multiplot layout 2,1 title " monitor rate based on num of queries(4000)"
set xlabel 'monitor thread per k queries'
set ylabel 'total query time'
set title 'total query time vs k'
set style data histograms
set boxwidth 1.0 relative
set style fill solid 1.0 border -1
plot 'final_op' using 2:xticlabels(1) lt rgb 'green'
set xlabel 'monitor thread per k queries'
set ylabel 'real time (msec)'
set style data histograms
set boxwidth 1.0 relative
set style fill solid 1.0 border -1
plot 'final_op' using 3:xticlabels(1) lt rgb 'red'

