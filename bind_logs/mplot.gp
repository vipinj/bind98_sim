set ytics nomirror
set y2tics
set key autotitle columnhead
set ylabel 'rtt(secs)'
set y2label 'queries/sec'
set xlabel 'time'
set terminal png enhanced size 2048,1024
set output 'mplot.png'
set multiplot layout 5,3
#set size 0.5,0.5
set style line 5 lt rgb 'green' lw 3 pt 6
set title 'a.gtld-servers.net'
plot '1_ns.log' using 1:2 with linespoints, '1_ns.log_hist' using 1:2 smooth csplines axes x1y2 ls 5
#set size 0.5,0.5
set title 'b.gtld-servers.net'
plot '2_ns.log' using 1:2 with linespoints, '2_ns.log_hist' using 1:2 smooth csplines axes x1y2 ls 5
#set size 0.5,0.5
set title 'c.gtld-servers.net'
plot '3_ns.log' using 1:2 with linespoints, '3_ns.log_hist' using 1:2 smooth csplines axes x1y2 ls 5
#set size 0.5,0.5
set title 'd.gtld-servers.net'
plot '4_ns.log' using 1:2 with linespoints, '4_ns.log_hist' using 1:2 smooth csplines axes x1y2 ls 5
#set size 0.5,0.5
set title 'e.gtld-servers.net'
plot '5_ns.log' using 1:2 with linespoints, '5_ns.log_hist' using 1:2 smooth csplines axes x1y2 ls 5
#set size 0.5,0.5
set title 'f.gtld-servers.net'
plot '6_ns.log' using 1:2 with linespoints, '6_ns.log_hist' using 1:2 smooth csplines axes x1y2 ls 5
#set size 0.5,0.5
set title 'g.gtld-servers.net'
plot '7_ns.log' using 1:2 with linespoints, '7_ns.log_hist' using 1:2 smooth csplines axes x1y2 ls 5
#set size 0.5,0.5
set title 'h.gtld-servers.net'
plot '8_ns.log' using 1:2 with linespoints, '8_ns.log_hist' using 1:2 smooth csplines axes x1y2 ls 5
#set size 0.5,0.5
set title 'i.gtld-servers.net'
plot '9_ns.log' using 1:2 with linespoints, '9_ns.log_hist' using 1:2 smooth csplines axes x1y2 ls 5
#set size 0.5,0.5
set title 'j.gtld-servers.net'
plot '10_ns.log' using 1:2 with linespoints, '10_ns.log_hist' using 1:2 smooth csplines axes x1y2 ls 5
#set size 0.5,0.5
set title 'k.gtld-servers.net'
plot '11_ns.log' using 1:2 with linespoints, '11_ns.log_hist' using 1:2 smooth csplines axes x1y2 ls 5
#set size 0.5,0.5
set title 'l.gtld-servers.net'
plot '12_ns.log' using 1:2 with linespoints, '12_ns.log_hist' using 1:2 smooth csplines axes x1y2 ls 5
#set size 0.5,0.5
set title 'm.gtld-servers.net'
plot '13_ns.log' using 1:2 with linespoints, '13_ns.log_hist' using 1:2 smooth csplines axes x1y2 ls 5



