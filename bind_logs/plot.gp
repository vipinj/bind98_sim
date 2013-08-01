set ylabel 'queries'
set xlabel 'rtts'
set terminal png enhanced size 2048,1024
set output 'mplot.png'
set multiplot layout 4,2
#set size 0.5,0.5
set style data histograms
set boxwidth 1.0 relative
set style fill solid 1.0 border -1 
plot 'bind.log.1_d_u' using 2:xticlabels(1) lt rgb 'green'
plot 'bind.log.2_d_u' using 2:xticlabels(1) lt rgb 'green'
plot 'bind.log.3_d_u' using 2:xticlabels(1) lt rgb 'green'
plot 'bind.log.4_d_u' using 2:xticlabels(1) lt rgb 'green'
plot 'bind.log.5_d_u' using 2:xticlabels(1) lt rgb 'green'
plot 'bind.log.6_d_u' using 2:xticlabels(1) lt rgb 'green'
plot 'bind.log.7_d_u' using 2:xticlabels(1) lt rgb 'green'
plot 'bind.log.8_d_u' using 2:xticlabels(1) lt rgb 'green'

